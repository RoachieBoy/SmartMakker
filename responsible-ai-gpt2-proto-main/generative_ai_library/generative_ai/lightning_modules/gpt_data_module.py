import datasets
import lightning as pl

from generative_ai.lightning_modules.gpt_fine_tuner import GPTFineTuner
from typing import List
from torch.utils.data import DataLoader
from os import cpu_count
from transformers import BatchEncoding


class GPTDataModule(pl.LightningDataModule):
    """
    Data module for the GPT model that is used to prepare the data for training.
    """

    def __init__(
            self,
            data: str | List[str],
            fine_tuning_module: GPTFineTuner,
            batch_size: int,
            column: str | None = None,
    ) -> None:
        """
        Initializes the data module.

        :param data: The data to use for training. Can be a list of strings or a path to a CSV file.
        :param fine_tuning_module: The fine-tuning module to use for training.
        :param batch_size: The batch size to use for training.
        :param column: The column to use for training. Defaults to 'text'.
        """
        super().__init__()

        self.data = data
        self.dataset = None
        self.column = column if column else 'text'
        self.batch_size = batch_size
        self.fine_tuning_module = fine_tuning_module

    def prepare_sample(self, batch: dict[str, any]) -> BatchEncoding:
        """
        Tokenizes the given batch of samples.

        :param batch: Batch of samples to tokenize.
        """

        batch_encoding = self.fine_tuning_module.tokenizer(
            batch[self.column],
            truncation=True,
            padding='max_length',
            max_length=1024,
            return_tensors='pt'
        )

        return batch_encoding
    
    def setup(self, stage: str) -> None:
        self.dataset = datasets.load_from_disk('./tokenized_data')

        self.dataset.set_format(type='torch', columns=['input_ids', 'attention_mask', 'labels'])

    def train_dataloader(self) -> DataLoader:
        return DataLoader(
            self.dataset['train'],
            pin_memory=True,
            shuffle=True,
            batch_size=self.batch_size,
            num_workers=cpu_count()
        )

    def prepare_data(self) -> None:
        if isinstance(self.data, list):
            # Convert the list of strings to a dataset
            pre_tokenized_dataset = datasets.Dataset.from_dict({"text": self.data})
        else:
            # Load the CSV dataset
            pre_tokenized_dataset = datasets.load_dataset('csv', data_files=self.data)
        # Tokenize the dataset
        tokenized_dataset = pre_tokenized_dataset.map(
            self.prepare_sample,
            batched=True
        )
        # Add the labels column to the dataset
        tokenized_dataset["train"] = tokenized_dataset["train"].add_column(
            "labels",
            tokenized_dataset["train"]["input_ids"]
        )

        tokenized_dataset.save_to_disk('./tokenized_data')
