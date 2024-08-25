from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig
from generative_ai.trainers import fine_tune_gpt_with_lightning_deepspeed


def main():
    # Model repository
    model_repo = "yhavinga/gpt2-medium-dutch"

    print("Downloading the model...")

    # Download the models
    config = AutoConfig.from_pretrained(model_repo)
    tokenizer = AutoTokenizer.from_pretrained(model_repo, config=config)
    model = AutoModelForCausalLM.from_pretrained(model_repo, config=config)

    # set model padding tokens
    if config.pad_token_id is None:
        tokenizer.pad_token_id = config.eos_token_id
    else:
        tokenizer.pad_token_id = config.pad_token_id

    print("Saving the model...")

    # File path for saving
    save_model_path = "./output"

    # Save the original config, tokenizer and model
    config.save_pretrained(save_model_path)
    tokenizer.save_pretrained(save_model_path)
    model.save_pretrained(save_model_path)

    print("Fine-tuning the model...")

    fine_tune_gpt_with_lightning_deepspeed(
        model_path="./output",
        output_path="./output",
        train_data="./../train_data/genius_smart_collector_5312.csv",
        epochs=2,
        layers_to_freeze=30,
        column="genius_smart_collector",
        batch_size=2,
        learning_rate=1e-5,
    )

    print("Done!")


if __name__ == "__main__":
    main()
