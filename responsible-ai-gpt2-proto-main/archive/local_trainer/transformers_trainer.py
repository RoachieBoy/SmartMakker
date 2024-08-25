from transformers import AutoTokenizer, AutoConfig, AutoModelForCausalLM, Trainer, TrainingArguments, pipeline
from datasets import load_dataset


def train_loop(files: str, key: str, tokenizer, model):
    trainings_data = load_dataset('csv', data_files=files)

    print(trainings_data)

    def tokenize_function(examples):
        return tokenizer(examples[key], padding="max_length", truncation=True, max_length=1024)

    tokenized_datasets = trainings_data.map(tokenize_function, batched=True)

    tokenized_datasets["train"] = \
        tokenized_datasets["train"].add_column("labels", tokenized_datasets["train"]["input_ids"])

    print(tokenized_datasets)

    training_args = TrainingArguments(
        output_dir="local_trainer/output_transformers",
        per_device_train_batch_size=2,
        label_names=["input_ids"],
        num_train_epochs=1,
        deepspeed="local_trainer/deepspeed_3.json",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"]
    )

    trainer.train()


def main():
    model_repo = "yhavinga/gpt-neo-125m-dutch"

    config = AutoConfig.from_pretrained(model_repo)
    tokenizer = AutoTokenizer.from_pretrained(model_repo, config=config)
    model = AutoModelForCausalLM.from_pretrained(model_repo, config=config)

    if config.pad_token_id is None:
        tokenizer.pad_token_id = config.eos_token_id
    else:
        tokenizer.pad_token_id = config.pad_token_id

    layers_to_freeze = 10

    for name, param in model.transformer.named_parameters():
        print(name)

        if layers_to_freeze:
            if "h." in name:
                # Extract the layer number from the parameter name
                layer_num = int(name.split(".")[1])
            else:
                layer_num = None
                to_freeze = layer_num and layer_num < layers_to_freeze
        else:
            # if no layers are being frozen, set to_freeze to false for all layers
            to_freeze = False

        # Freeze the current parameter if it belongs to the embedding layer
        # or if to_freeze is true for this layer
        if name == "wte.weight" or to_freeze:
            param.requires_grad = False

    train_loop("local_trainer/trainings_data/short_stories_1117.csv", "0", tokenizer, model)
    train_loop("local_trainer/trainings_data/genius_2956.csv", "genius_smart_collector", tokenizer, model)

    config.save_pretrained("local_trainer/output_transformers")
    tokenizer.save_pretrained("local_trainer/output_transformers")
    model.save_pretrained("local_trainer/output_transformers")


if __name__ == "__main__":
    main()
