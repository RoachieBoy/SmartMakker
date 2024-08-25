try:
    import generative_ai.generators.zero_to_fp32 as deepspeed_checkpoint
except ImportError as e:
    if "deepspeed" not in e.msg:
        raise

from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM, AutoConfig


class HuggingFaceGenerator:
    """
    A class used to generate text using the HuggingFace pipeline.
    """
    def __init__(self, model_path: str, deepspeed: bool = False) -> None:
        """
        Initializes the HuggingFaceGenerator class.

        :param model_path: path to the model to use for generation.
        :param deepspeed: whether to use deepspeed or not. Automatically converts the model to fp32. Defaults to False.
        """

        config = AutoConfig.from_pretrained(
            f"{model_path}/../output" if deepspeed else model_path
        )

        tokenizer = AutoTokenizer.from_pretrained(
            f"{model_path}/../output" if deepspeed else model_path, config=config
        )

        model = AutoModelForCausalLM.from_pretrained(
            f"{model_path}/../../org_model" if deepspeed else model_path, config=config
        )

        if deepspeed:
            model = deepspeed_checkpoint.load_state_dict_from_zero_checkpoint(model=model, checkpoint_dir=model_path)

        model = model.to_bettertransformer()

        self.generator = pipeline(
            'text-generation',
            model,
            tokenizer=tokenizer,
            config=config
        )

    def generate_single_prompt(
            self,
            prompt: str,
            max_length: int,
            min_length: int,
            temperature: float,
            top_k: int,
            top_p: float,
            repetition_penalty: float,
            no_repeat_ngram_size: int,
    ) -> str:
        """
        Generates a single prompt using the built-in HuggingFace pipeline.

        :param prompt: the prompt from which to generate from.
        :param max_length: the maximum length of the generated text.
        :param min_length: the minimum length of the generated text.
        :param temperature: controls the randomness/craziness of the text.
        :param top_k: controls diversity of generated text by limiting number of next words.
        :param top_p: controls diversity of generated text by limiting the cumulative probability of next words.
        :param repetition_penalty: controls the likelihood of words being repeated in the generated text.
        :param no_repeat_ngram_size: controls the size of the n-grams that should not be repeated in the generated text.
        :return: the generated text as a string.
        """
        return self.generator(
            prompt,
            max_length=max_length,
            min_length=min_length,
            temperature=float(temperature),
            top_k=top_k,
            top_p=float(top_p),
            repetition_penalty=float(repetition_penalty),
            no_repeat_ngram_size=no_repeat_ngram_size,
        )[0]['generated_text']
