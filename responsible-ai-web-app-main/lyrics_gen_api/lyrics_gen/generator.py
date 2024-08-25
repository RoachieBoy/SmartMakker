import re

from lingua import Language, LanguageDetectorBuilder
from typing import Callable

MINIMUM_PROMPT_LENGTH = 20


class LyricsGen:
    """
    The LyricsGen class is responsible for generating lyrics based on a given prompt
    The class is designed to be used in a pipeline, where each method is chained together to perform a specific task
    """

    def __init__(self, text_gen_backend: Callable[
        [
            str,
            int,
            int,
            float,
            int,
            float,
            float,
            int
        ],
        str
    ]) -> None:
        """
        Initializes the LyricsGen class
        :param text_gen_backend: The text generation backend to use
        """
        self.prompt = ""
        self.org_prompt = ""

        if text_gen_backend is None:
            raise Exception("The text generation backend is not set.")

        self.profanity = None

        try:
            self.profanity = open('profanity.txt', 'r').read().splitlines()
        except FileNotFoundError:
            raise print("The profanity file could not be found.")

        self.text_gen_backend = text_gen_backend

    def check_prompt_length(self):
        """
        Check for the prompt length
        """
        if len(self.prompt.split()) < MINIMUM_PROMPT_LENGTH:
            raise Exception("De prompt is de kort. De teskt kan noet goed worden gegenereerd.")

        return self

    def each_sentence_on_new_line(self):
        """
        Puts each sentence on a new line
        """
        # regex explanation: (?<=[.,!?]) - lookbehind for punctuation, (\s)* - zero or more spaces
        new_line_characters = r'(?<=[.!?])(\s)*'

        self.prompt = re.sub(new_line_characters, '\n', self.prompt)

        return self

    def remove_special_characters(self):
        """
        Removes punctuation from the prompt
        """
        # regex explanation: [^\w\s] - matches any character that is not a word character or a whitespace character
        self.prompt = re.sub(r'[^\w\s,!?]', '', self.prompt)

        return self

    def make_lowercase(self):
        """
        Makes the prompt lowercase
        """
        self.prompt = self.prompt.lower()

        return self

    def check_language(self):
        """
        Checks the language of the prompt
        If the language is not Dutch, an exception is raised and the lyrics cannot be generated
        """
        language_detector = LanguageDetectorBuilder.from_all_languages().with_preloaded_language_models().build()
        language = language_detector.detect_language_of(self.prompt)

        if language != Language.DUTCH:
            raise Exception(
                "De taal van de teskt is te ontduidelijk of heeft niet genoeg Nederlands om een goede tekst te genereren."
            )

        return self

    def feed_the_machine(
            self,
            temperature: float,
            top_k: int,
            top_p: float,
            repetition_penalty: float,
            n_gram: int
    ):
        """
        Feeds the prompt into the machine to generate lyrics

        :param temperature: The temperature of the text generation
        :param top_k: The top_k value
        :param top_p: The top_p value
        :param repetition_penalty: The repetition penalty value
        :param n_gram: The n-gram size
        :return: self
        """
        self.prompt = self.text_gen_backend(
            self.prompt,
            # Max length of the generated text
            len(self.org_prompt.split()) + 110,
            # Min length of the generated text
            len(self.org_prompt.split()) + 90,
            temperature,
            top_k,
            top_p,
            repetition_penalty,
            n_gram
        )

        return self

    def clean_output(self):
        """
        Cleans the output of the machine to ensure it is readable and formatted correctly
        """
        # removes <|endoftext|> from the output and any text that resembles it, e.g. <|> or <endoftext> etc
        # regex explanation: <[^>]*> - matches any character that is not a >, zero or more times
        self.prompt = re.sub(r"<[^>]*>", "", self.prompt)

        return self

    def capitalise_text(self):
        """
        Capitalizes the first letter of each line
        """
        self.prompt = self.prompt.capitalize()
        # split the input text into separate lines
        lines = self.prompt.splitlines()
        # capitalize the first letter of each line
        capitalized_lines = [line.capitalize() for line in lines]
        # join the capitalized lines back into a single string
        self.prompt = "\n".join(capitalized_lines)

        return self

    def check_profanity(self, nsfw: bool, replacement: str = "***"):
        """
        Checks the prompt for profanity and replaces it with a replacement string

        :param nsfw: True if the lyrics should be NSFW, False otherwise
        :param replacement: The string to replace the profanity with
        """
        if not nsfw and self.profanity is not None:
            reg = re.compile(' |'.join(map(re.escape, self.profanity)))

            self.prompt = reg.sub(replacement + " ", self.prompt)

        return self

    def remove_last_line(self):
        """
        Removes the last line of the prompt
        """
        self.prompt = self.prompt.rsplit('\n', 1)[0]

        return self

    def remove_first_line(self):
        """
        Removes the first line of the prompt
        """
        # Remove the original prompt from the generated lyrics by taking the difference between the two
        self.prompt = self.prompt[len(self.org_prompt):]
        # # Remove the first line of the prompt
        self.prompt = self.prompt.split('\n', 1)[1]
        # Add the original prompt back to the generated lyrics
        self.prompt = self.org_prompt + self.prompt

        return self

    def remove_excessive_new_lines(self):
        """
        Removes excessive new lines from the prompt
        """
        # Remove the original prompt from the generated lyrics by taking the difference between the two
        self.prompt = self.prompt[len(self.org_prompt):]
        # Remove excessive new lines from the prompt
        self.prompt = re.sub(r'\n{2,}', '\n', self.prompt)
        # Add the original prompt back to the generated lyrics
        self.prompt = self.org_prompt + self.prompt

        return self

    def get_lyrics(
            self,
            prompt: str,
            temperature: float,
            top_k: int,
            top_p: float,
            repetition_penalty: float,
            n_gram: int,
            nsfw: bool = False
    ):
        """
        Generates lyrics based on the given prompt

        :param prompt: String containing the prompt
        :param temperature: The temperature of the text generation
        :param top_k: The top_k value
        :param top_p: The top_p value
        :param repetition_penalty: The repetition penalty value
        :param n_gram: The n-gram size
        :param nsfw: True if the lyrics should be NSFW, False otherwise
        :return: The generated and processed lyrics
        """

        self.prompt = prompt
        self.org_prompt = prompt

        self.check_prompt_length() \
            .check_language() \
            .each_sentence_on_new_line() \
            .remove_special_characters() \
            .make_lowercase() \
            .feed_the_machine(temperature, top_k, top_p, repetition_penalty, n_gram) \
            .remove_first_line() \
            .remove_last_line() \
            .remove_special_characters() \
            .check_profanity(nsfw) \
            .remove_excessive_new_lines() \
            .capitalise_text()

        return self.prompt
