import lightning as pl

from generative_ai.lightning_modules.gpt_data_module import GPTDataModule
from generative_ai.lightning_modules.gpt_fine_tuner import GPTFineTuner
from lightning.pytorch.strategies import DeepSpeedStrategy
from lightning.pytorch.tuner.tuning import Tuner
from lightning.pytorch.callbacks import LearningRateMonitor, DeviceStatsMonitor
from torch.optim.lr_scheduler import LRScheduler
from torch.optim import Optimizer
from typing import List, Type

try:
    from deepspeed.ops.adam.cpu_adam import DeepSpeedCPUAdam
except ImportError as e:
    if "deepspeed" not in e.msg:
        raise


def fine_tune_gpt_with_lightning(
        model_path: str,
        output_path: str,
        train_data: List[str] | str,
        epochs: int,
        batch_size: int = 1,
        learning_rate: float | str | None = "auto",
        layers_to_freeze: int = 0,
        column: str | None = None,
        scheduler: Type[LRScheduler] | None = None,
        scheduler_kwargs: dict[str, any] | None = None,
        scheduler_interval: str | None = None,
        optimizer: Type[Optimizer] | None = None,
        optimizer_kwargs: dict[str, any] | None = None
) -> None:
    """
    Fine-tunes a GPT model with PyTorch Lightning.

    :param model_path: Path to the model to fine-tune.
    :param output_path: Path to save the fine-tuned model.
    :param train_data: List of texts or csv path to fine-tune the model on.
    :param epochs: Number of epochs to fine-tune the model. Defaults to 1.
    :param batch_size: Batch size to use during fine-tuning. Defaults to 1.
    :param learning_rate: Learning rate to use during fine-tuning. If set to "auto", the learning rate will be found using the PyTorch Lightning lr finder. Defaults to "auto".
    :param layers_to_freeze: Number of layers to freeze during the fine-tuning process. Defaults to 0.
    :param column: Column of dataset to use for training.
    :param scheduler: The learning rate scheduler to use during fine-tuning. There are out of the box options: OneCycleLR and CosineAnnealingLR.
    :param scheduler_kwargs: Keyword arguments to pass to the scheduler.
    :param scheduler_interval: The interval to use for the scheduler. Defaults to "step".
    :param optimizer: The optimizer to use during fine-tuning. Defaults to AdamW.
    :param optimizer_kwargs: Keyword arguments to pass to the optimizer.
    """
    fine_tuner_module = GPTFineTuner(
        layers_to_freeze=layers_to_freeze,
        model_or_path=model_path,
        learning_rate=1e-5 if learning_rate == "auto" else learning_rate,
        scheduler=scheduler,
        scheduler_kwargs=scheduler_kwargs,
        scheduler_interval=scheduler_interval,
        optimizer=optimizer,
        optimizer_kwargs=optimizer_kwargs
    )

    precision = __get_precision__(fine_tuner_module.config)

    trainer = pl.Trainer(
        max_epochs=epochs,
        enable_progress_bar=True,
        precision=precision,
        callbacks=[
            LearningRateMonitor(logging_interval="step"),
            DeviceStatsMonitor()
        ],
        log_every_n_steps=25
    )

    data_module = GPTDataModule(
        data=train_data,
        fine_tuning_module=fine_tuner_module,
        column=column,
        batch_size=batch_size
    )

    if learning_rate == "auto":
        tuner = Tuner(trainer)

        tuner.lr_find(
            model=fine_tuner_module,
            datamodule=data_module
        )

    print(f"Initial learning rate set to: {fine_tuner_module.learning_rate}")

    trainer.fit(
        model=fine_tuner_module,
        datamodule=data_module
    )

    fine_tuner_module.model.save_pretrained(output_path)
    fine_tuner_module.tokenizer.save_pretrained(output_path)
    fine_tuner_module.config.save_pretrained(output_path)


def fine_tune_gpt_with_lightning_deepspeed(
        model_path: str,
        output_path: str,
        train_data: List[str] | str,
        epochs: int,
        batch_size: int = 1,
        learning_rate: float = 1e-5,
        layers_to_freeze: int = 0,
        column: str | None = None
) -> None:
    """
    Fine-tunes a GPT model with PyTorch Lightning and DeepSpeed.

    :param model_path: The path to the model to fine-tune.
    :param output_path: The path to save the fine-tuned model.
    :param train_data: List of texts or csv path to fine-tune the model on.
    :param epochs: Number of epochs to fine-tune the model. Defaults to 1.
    :param batch_size: Batch size to use during fine-tuning. Defaults to 1.
    :param learning_rate: Learning rate to use during fine-tuning. Defaults to 1e-5.
    :param layers_to_freeze: Number of layers to freeze during the fine-tuning process. Defaults to 0.
    :param column: Column of dataset to use for training.
    """
    fine_tuner_module = GPTFineTuner(
        layers_to_freeze=layers_to_freeze,
        model_or_path=model_path,
        optimizer=DeepSpeedCPUAdam,
        learning_rate=learning_rate
    )

    precision = __get_precision__(fine_tuner_module.config, deepspeed=True)

    strategy = DeepSpeedStrategy(
        stage=3,
        offload_optimizer=True,
        offload_parameters=True,
    )

    trainer = pl.Trainer(
        strategy=strategy,
        max_epochs=epochs,
        enable_progress_bar=True,
        precision=precision,
        callbacks=[
            DeviceStatsMonitor(cpu_stats=True),
            LearningRateMonitor(logging_interval="step")
        ],
        log_every_n_steps=25
    )

    data_module = GPTDataModule(
        data=train_data,
        fine_tuning_module=fine_tuner_module,
        column=column,
        batch_size=batch_size
    )

    trainer.fit(
        model=fine_tuner_module,
        datamodule=data_module
    )

    trainer.save_checkpoint(f"{output_path}/checkpoint")
    fine_tuner_module.tokenizer.save_pretrained(f"{output_path}/output")
    fine_tuner_module.config.save_pretrained(f"{output_path}/output")


def __get_precision__(config, deepspeed: bool = False) -> str | int:
    """
    Gets the precision to use during fine-tuning.

    :param config: The model config.
    :param deepspeed: Whether to use deepspeed or not. Defaults to False.
    :return: The precision to use during fine-tuning.
    """
    precision_returned: str | int = "Precision not set!"
    data_type = str(config.torch_dtype).lower() if config.torch_dtype else "No config set"

    if not data_type:
        precision_returned = 32 if not deepspeed else 'bf16-mixed'

    if 'float64' in data_type:
        precision_returned = 64 if not deepspeed else 'bf16-mixed'

    if 'float32' in data_type:
        precision_returned = 32 if not deepspeed else 'bf16-mixed'

    if 'bfloat16' in data_type:
        precision_returned = 'bf16-mixed'

    if 'float16' in data_type:
        precision_returned = '16-mixed'

    print(f"Precision set to {precision_returned}, config precision: {data_type}")

    return precision_returned
