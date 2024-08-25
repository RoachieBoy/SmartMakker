import lightning as pl
import torch

from typing import Type
from torch import optim, Tensor
from torch.optim import Optimizer
from torch.optim.adamw import AdamW
from torch.optim.lr_scheduler import LRScheduler
from transformers import AutoConfig, AutoTokenizer, AutoModelForCausalLM
from torchmetrics.text.perplexity import Perplexity


class GPTFineTuner(pl.LightningModule):
    """
    A PyTorch Lightning module used to fine-tune a GPT model.
    """

    def __init__(
            self,
            layers_to_freeze: int,
            model_or_path: str,
            learning_rate: float | None = None,
            optimizer: Type[Optimizer] | None = None,
            optimizer_kwargs: dict[str, any] | None = None,
            scheduler: Type[LRScheduler] | None = None,
            scheduler_kwargs: dict[str, any] | None = None,
            scheduler_interval: str | None = None
    ) -> None:
        """
        Initializes a new GPTFineTuner instance.

        :param layers_to_freeze: The number of layers to freeze.
        :param model_or_path: The model or path to the model to fine-tune.
        :param learning_rate: The learning rate to use for the optimizer. Defaults to None.
        :param optimizer: The optimizer to use for training. Defaults to AdamW.
        :param optimizer_kwargs: The keyword arguments to pass to the optimizer. Defaults to None.
        :param scheduler: The scheduler to use for training. Defaults to None.
        :param scheduler_kwargs: The keyword arguments to pass to the scheduler. Defaults to None.
        :param scheduler_interval: The interval to use for the scheduler. Defaults to "step".
        """
        super().__init__()

        self.scheduler = scheduler
        self.optimizer = optimizer if optimizer else AdamW
        self.learning_rate = learning_rate
        self.optimizer_kwargs = optimizer_kwargs if optimizer_kwargs else {}
        self.scheduler_kwargs = scheduler_kwargs if scheduler_kwargs else {}
        self.scheduler_interval = scheduler_interval if scheduler_interval else "step"

        self._config = AutoConfig.from_pretrained(
            model_or_path,
            output_hidden_states=True
        )

        self._tokenizer = AutoTokenizer.from_pretrained(
            model_or_path,
            config=self._config
        )
        self._model = AutoModelForCausalLM.from_pretrained(
            model_or_path,
            config=self._config
        )

        self._perplexity = Perplexity(ignore_index=self.config.pad_token_id)

        if layers_to_freeze > 0:
            self.__freeze__(layers_to_freeze)

    def __freeze__(self, layers_to_freeze: int) -> None:
        """
        Freezes the given number of layers of the model.

        :param layers_to_freeze: Number of layers to freeze.
        """

        # Iterate over all the parameters of the model
        for name, param in self._model.transformer.named_parameters():
            to_freeze = False
            layer_num = 0

            if "h." in name:
                # Extract the layer number from the parameter name
                layer_num = int(name.split(".")[1])

            to_freeze = layer_num < layers_to_freeze and layer_num is not 0
            # Freeze the current parameter if it belongs to the embedding layer
            # or if to_freeze is true for this layer
            if name == "wte.weight" or to_freeze:
                param.requires_grad = False

    @property
    def tokenizer(self) -> any:
        """
        Returns the tokenizer used by the fine-tuner.

        :return: the tokenizer used by the fine-tuner.
        """
        return self._tokenizer

    @property
    def model(self) -> any:
        """
        Returns the model used by the fine-tuner.

        :return: the model used by the fine-tuner.
        """
        return self._model

    @property
    def config(self) -> any:
        """
        Returns the model used by the fine-tuner.

        :return: the model used by the fine-tuner.
        """
        return self._config

    def forward(self, batch) -> any:
        return self.model(**batch)

    def training_step(self, batch, batch_num) -> Tensor:
        # Pass the input_ids and labels from the current batch to the model
        outputs = self.model(**batch)
        # Extract the loss value from the model outputs
        loss = outputs.loss
        # Log the loss metric to the logger and progress bar
        self.log("train_loss", loss, on_step=True, on_epoch=True, prog_bar=True, logger=True)
        # Extract the precision from the trainer
        precision = self.trainer.precision
        # Extract the logits from the model outputs
        predictions = outputs.logits
        # Convert the logits to the correct precision for perplexity calculation
        if not (precision.__contains__("32") or precision.__contains__("64")):
            predictions = predictions.to(torch.float32)
        # Calculate the perplexity of the predictions
        pp = self._perplexity(predictions, batch["labels"])
        # Log the perplexity metric to the logger and progress bar
        self.log("train_perplexity", pp, on_step=True, on_epoch=True, prog_bar=True, logger=True)

        return loss

    def configure_optimizers(self) -> any:
        # To support Adafactor, we need to only set the learning rate when directly passing it
        if self.learning_rate is not None:
            self.optimizer_kwargs['lr'] = self.learning_rate

        optimizer = self.optimizer(self.parameters(), **self.optimizer_kwargs)
        # Out of the box support for various schedulers
        if self.scheduler:
            if self.scheduler is optim.lr_scheduler.CosineAnnealingLR:
                self.scheduler_kwargs["T_max"] = self.trainer.estimated_stepping_batches

            if self.scheduler is optim.lr_scheduler.OneCycleLR:
                self.scheduler_kwargs["total_steps"] = self.trainer.estimated_stepping_batches
                self.scheduler_kwargs["max_lr"] = self.learning_rate

            scheduler = self.scheduler(optimizer, **self.scheduler_kwargs)

            return [optimizer], [{"scheduler": scheduler, "interval": self.scheduler_interval}]
        else:
            return optimizer
