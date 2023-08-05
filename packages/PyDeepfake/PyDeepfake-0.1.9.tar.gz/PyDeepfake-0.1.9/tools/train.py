'''
Copyright 2022 fvl

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
import pprint

import numpy as np
import torch
from torch.utils.tensorboard import SummaryWriter

import PyDeepfake.utils.checkpoint as cu
import PyDeepfake.utils.distributed as du
import PyDeepfake.utils.logging as logging
from PyDeepfake.utils.build_helper import (
    build_dataloader,
    build_dataset,
    build_loss_fun,
    build_model,
)
from PyDeepfake.utils.meters import EpochTimer, MetricLogger, SmoothedValue
from PyDeepfake.utils.optimizer import build_optimizer
from PyDeepfake.utils.scheduler import build_scheduler
from tools.test import perform_test

logger = logging.get_logger(__name__)


def train_epoch(
    train_loader, model, criterion, optimizer, cfg, cur_epoch, cur_iter, writer
):
    model.train()
    train_meter = MetricLogger(delimiter="  ")
    train_meter.add_meter('lr', SmoothedValue(window_size=1, fmt='{value:.8f}'))
    header = 'Epoch: [{}]'.format(cur_epoch)
    print_freq = 10

    for samples in train_meter.log_every(train_loader, print_freq, header):
        samples = dict(
            zip(
                samples,
                map(
                    lambda sample: sample.cuda(non_blocking=True),
                    samples.values(),
                ),
            )
        )

        with torch.cuda.amp.autocast(enabled=cfg['AMP_ENABLE']):
            outputs = model(samples)
            loss = criterion(outputs, samples)

        loss_value = loss.item()

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        torch.cuda.synchronize()

        if 'CLIP_GRAD_L2NORM' in cfg['TRAIN']:  # TODO
            torch.nn.utils.clip_grad_norm_(
                model.parameters(), cfg['TRAIN']['CLIP_GRAD_L2NORM']
            )

        if writer:
            writer.add_scalar('train loss', loss_value, global_step=cur_iter)
            writer.add_scalar(
                'lr', optimizer.param_groups[0]["lr"], global_step=cur_iter
            )
        train_meter.update(loss=loss_value)
        train_meter.update(lr=optimizer.param_groups[0]["lr"])
        cur_iter = cur_iter + 1

    train_meter.synchronize_between_processes()
    logger.info("Averaged stats:" + str(train_meter))
    return {
        k: meter.global_avg for k, meter in train_meter.meters.items()
    }, cur_iter


def train(
    local_rank, num_proc, init_method, shard_id, num_shards, backend, cfg
):
    world_size = num_proc * num_shards
    rank = shard_id * num_proc + local_rank
    torch.distributed.init_process_group(
        backend=backend,
        init_method=init_method,
        world_size=world_size,
        rank=rank,
    )
    torch.cuda.set_device(local_rank)
    du.init_distributed_training(cfg)
    np.random.seed(cfg['RNG_SEED'])
    torch.manual_seed(cfg['RNG_SEED'])

    logging.setup_logging(cfg)
    logger.info(pprint.pformat(cfg))
    if du.is_master_proc(du.get_world_size()):
        writer = SummaryWriter(cfg['LOG_FILE_PATH'])
    else:
        writer = None

    model = build_model(cfg)
    optimizer = build_optimizer(model.parameters(), cfg)
    scheduler, _ = build_scheduler(optimizer, cfg)  # TODO _?
    loss_fun = build_loss_fun(cfg)
    train_dataset = build_dataset('train', cfg)
    train_loader = build_dataloader(train_dataset, 'train', cfg)
    val_dataset = build_dataset('val', cfg)
    val_loader = build_dataloader(val_dataset, 'val', cfg)

    start_epoch = cu.load_train_checkpoint(model, optimizer, scheduler, cfg)

    logger.info("Start epoch: {}".format(start_epoch + 1))
    epoch_timer = EpochTimer()

    cur_iter = 0

    for cur_epoch in range(start_epoch, cfg['TRAIN']['MAX_EPOCH']):
        logger.info('========================================================')
        train_loader.sampler.set_epoch(cur_epoch)
        val_loader.sampler.set_epoch(cur_epoch)
        epoch_timer.epoch_tic()
        _, cur_iter = train_epoch(
            train_loader,
            model,
            loss_fun,
            optimizer,
            cfg,
            cur_epoch,
            cur_iter,
            writer,
        )
        epoch_timer.epoch_toc()
        perform_test(val_loader, model, cfg, cur_epoch, writer, mode='Val')
        logger.info(
            f"Epoch {cur_epoch} takes {epoch_timer.last_epoch_time():.2f}s. Epochs "
            f"from {start_epoch} to {cur_epoch} take "
            f"{epoch_timer.avg_epoch_time():.2f}s in average and "
            f"{epoch_timer.median_epoch_time():.2f}s in median."
        )
        logger.info(
            f"For epoch {cur_epoch}, each iteraction takes "
            f"{epoch_timer.last_epoch_time()/len(train_loader):.2f}s in average. "
            f"From epoch {start_epoch} to {cur_epoch}, each iteraction takes "
            f"{epoch_timer.avg_epoch_time()/len(train_loader):.2f}s in average."
        )

        scheduler.step(cur_epoch)

        is_checkp_epoch = cu.is_checkpoint_epoch(cfg, cur_epoch)

        if is_checkp_epoch:
            cu.save_checkpoint(model, optimizer, scheduler, cur_epoch, cfg)

    if writer:
        writer.flush()
        writer.close()
