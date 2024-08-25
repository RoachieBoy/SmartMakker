import pandas
import generative_ai.trainers as trainers
import torch
import os


def main():
    cwd = os.getcwd()

    trainings_data = pandas.read_csv(f"{cwd}/local_trainer/trainings_data/genius_2956.csv").astype("string")
    trainings_data = trainings_data["genius_smart_collector"].tolist()

    checkpoint_path = f"{cwd}/local_trainer/output"

    torch.set_float32_matmul_precision('medium')

    trainers.fine_tune_gpt_with_lightning(
        model_path=checkpoint_path,
        output_path=checkpoint_path,
        train_data=trainings_data,
        epochs=400,
        batch_size=1
    )


if __name__ == "__main__":
    main()