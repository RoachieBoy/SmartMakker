# Responsible AI - GPT-based NLP Research & Development

The following folders are explained below:

### generative_ai_library

This folder contains the source code to a training library for GPT-based models. 
It uses the pytorch-lightning, transformers and deepspeed libraries to train on a single GPU or multiple GPUs.
Most of the code is automated and the user only needs to provide a training dataset and a few parameters to start training.

It is inspired by [aitextgen](https://github.com/minimaxir/aitextgen).

### archive

This folder contains experiments and exploration of GPT-based models and applied training methods.

### script_trainer

This folder contains scripts to train a GPT-based model with or without [DeepSpeed](https://github.com/microsoft/DeepSpeed)

### notebook_trainer

This folder contains notebooks to train a GPT-based model. DeepSpeed is not supported when using notebooks.

### train_data

This folder contains training data for lyrics, poetry, and other text.