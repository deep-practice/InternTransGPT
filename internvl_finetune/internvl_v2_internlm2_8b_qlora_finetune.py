accumulative_counts = 16
batch_size = 2
betas = (
    0.9,
    0.999,
)
custom_hooks = [
    dict(
        tokenizer=dict(
            pretrained_model_name_or_path='OpenGVLab/InternVL2-8B',
            trust_remote_code=True,
            type='transformers.AutoTokenizer.from_pretrained'),
        type='xtuner.engine.hooks.DatasetInfoHook'),
]
data_path = '/root/InternLM/datasets/TrafficSign/traffic_data_combined_newer.json'
data_root = '/root/InternLM/datasets/'
dataloader_num_workers = 4
default_hooks = dict(
    checkpoint=dict(
        by_epoch=False,
        interval=3000,
        max_keep_ckpts=6,
        save_optimizer=False,
        type='mmengine.hooks.CheckpointHook'),
    logger=dict(
        interval=10,
        log_metric_by_epoch=False,
        type='mmengine.hooks.LoggerHook'),
    param_scheduler=dict(type='mmengine.hooks.ParamSchedulerHook'),
    sampler_seed=dict(type='mmengine.hooks.DistSamplerSeedHook'),
    timer=dict(type='mmengine.hooks.IterTimerHook'))
env_cfg = dict(
    cudnn_benchmark=False,
    dist_cfg=dict(backend='nccl'),
    mp_cfg=dict(mp_start_method='fork', opencv_num_threads=0))
image_folder = '/root/InternLM/datasets/TrafficSign/'
launcher = 'none'
llava_dataset = dict(
    data_paths=[
        '/root/InternLM/datasets/TrafficSign/landmark_single_round_data.json',
        '/root/InternLM/datasets/TrafficSign/traffic_policy_QA_multi_round_data.json',
        '/root/InternLM/datasets/TrafficSign/trafficQA_single_round_data.json',
        '/root/InternLM/datasets/TrafficSign/trafficsign_single_round_data.json',
        '/root/InternLM/datasets/TrafficSign/trafficQA_multi_round_data.json',
    ],
    image_folders=[
        '/root/InternLM/datasets/TrafficSign/',
        '/root/InternLM/datasets/TrafficSign/',
        '/root/InternLM/datasets/TrafficSign/',
        '/root/InternLM/datasets/TrafficSign/',
        '/root/InternLM/datasets/TrafficSign/',
    ],
    max_length=6656,
    model_path='OpenGVLab/InternVL2-8B',
    repeat_times=[
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
    ],
    template='xtuner.utils.PROMPT_TEMPLATE.internlm2_chat',
    type='xtuner.dataset.InternVL_V1_5_Dataset')
load_from = None
log_level = 'INFO'
log_processor = dict(by_epoch=False)
lr = 2e-05
max_epochs = 3
max_length = 6656
max_norm = 1
model = dict(
    freeze_llm=True,
    freeze_visual_encoder=True,
    llm_lora=dict(
        lora_alpha=256,
        lora_dropout=0.05,
        r=128,
        target_modules=None,
        task_type='CAUSAL_LM',
        type='peft.LoraConfig'),
    model_path='OpenGVLab/InternVL2-8B',
    quantization_llm=True,
    quantization_vit=False,
    type='xtuner.model.InternVL_V1_5')
optim_type = 'torch.optim.AdamW'
optim_wrapper = dict(
    optimizer=dict(
        betas=(
            0.9,
            0.999,
        ),
        lr=2e-05,
        type='torch.optim.AdamW',
        weight_decay=0.05),
    type='DeepSpeedOptimWrapper')
param_scheduler = [
    dict(
        begin=0,
        by_epoch=True,
        convert_to_iter_based=True,
        end=0.09,
        start_factor=1e-05,
        type='mmengine.optim.LinearLR'),
    dict(
        begin=0.09,
        by_epoch=True,
        convert_to_iter_based=True,
        end=3,
        eta_min=0.0,
        type='mmengine.optim.CosineAnnealingLR'),
]
path = 'OpenGVLab/InternVL2-8B'
prompt_template = 'xtuner.utils.PROMPT_TEMPLATE.internlm2_chat'
randomness = dict(deterministic=False, seed=None)
resume = False
runner_type = 'FlexibleRunner'
save_steps = 3000
save_total_limit = 6
strategy = dict(
    config=dict(
        bf16=dict(enabled=True),
        fp16=dict(enabled=False, initial_scale_power=16),
        gradient_accumulation_steps='auto',
        gradient_clipping='auto',
        train_micro_batch_size_per_gpu='auto',
        zero_allow_untested_optimizer=True,
        zero_force_ds_cpu_optimizer=False,
        zero_optimization=dict(overlap_comm=True, stage=1)),
    exclude_frozen_parameters=True,
    gradient_accumulation_steps=16,
    gradient_clipping=1,
    sequence_parallel_size=1,
    train_micro_batch_size_per_gpu=2,
    type='xtuner.engine.DeepSpeedStrategy')
tokenizer = dict(
    pretrained_model_name_or_path='OpenGVLab/InternVL2-8B',
    trust_remote_code=True,
    type='transformers.AutoTokenizer.from_pretrained')
train_cfg = dict(max_epochs=3, type='xtuner.engine.runner.TrainLoop')
train_dataloader = dict(
    batch_size=2,
    collate_fn=dict(type='xtuner.dataset.collate_fns.default_collate_fn'),
    dataset=dict(
        data_paths=[
            '/root/InternLM/datasets/TrafficSign/landmark_single_round_data.json',
            '/root/InternLM/datasets/TrafficSign/traffic_policy_QA_multi_round_data.json',
            '/root/InternLM/datasets/TrafficSign/trafficQA_single_round_data.json',
            '/root/InternLM/datasets/TrafficSign/trafficsign_single_round_data.json',
            '/root/InternLM/datasets/TrafficSign/trafficQA_multi_round_data.json',
        ],
        image_folders=[
            '/root/InternLM/datasets/TrafficSign/',
            '/root/InternLM/datasets/TrafficSign/',
            '/root/InternLM/datasets/TrafficSign/',
            '/root/InternLM/datasets/TrafficSign/',
            '/root/InternLM/datasets/TrafficSign/',
        ],
        max_length=6656,
        model_path='OpenGVLab/InternVL2-8B',
        repeat_times=[
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
        ],
        template='xtuner.utils.PROMPT_TEMPLATE.internlm2_chat',
        type='xtuner.dataset.InternVL_V1_5_Dataset'),
    num_workers=4,
    sampler=dict(
        length_property='modality_length',
        per_device_batch_size=32,
        type='xtuner.dataset.samplers.LengthGroupedSampler'))
visualizer = None
warmup_ratio = 0.03
weight_decay = 0.05
work_dir = '/root/InternLM/work_dir/internvl_ft_trafficsign_multiround'
