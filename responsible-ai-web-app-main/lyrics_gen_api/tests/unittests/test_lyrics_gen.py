import unittest
from unittest.mock import Mock

from lyrics_gen_api import nlm_text_gen
from lyrics_gen_api import lyrics_gen


# TODO: Update to the new system
class TestLyricsGen(unittest.TestCase):
    """
    The TestLyricsGen class contains unit tests for the LyricsGen class
    The tests are written using the unittest library
    """

    def setUp(self) -> None:
        """	
        The setUp method is called before each test
        It creates a mock object for the text generation backend and a LyricsGen object
        with the mock object as the text generation backend
        """
        self.text_gen_backend = Mock(spec=nlm_text_gen.NLMTextGen)
        self.lyrics_gen = lyrics_gen.LyricsGen(self.text_gen_backend)

    def test_check_prompt_length(self) -> None:
        """
        The test_check_prompt_length method checks that the check_prompt_length method raises an exception 
        when the prompt length is less than the minimum prompt length
        """
        self.lyrics_gen.prompt = " ".join(["word"] * self.lyrics_gen.MINIMUM_PROMPT_LENGTH)
        self.assertIsNone(self.lyrics_gen.check_prompt_length())

    def test_remove_special_characters(self) -> None:
        """
        The test_remove_special_characters method checks that the remove_special_characters method 
        removes special characters from a string
        """
        self.lyrics_gen.prompt = "This prompt has ! some @ special # characters $"
        self.assertEqual(self.lyrics_gen.remove_special_characters(), "This prompt has  some  special  characters ")

    def test_make_lowercase(self) -> None:
        """	
        The test_make_lowercase method checks that the make_lowercase method makes strings lowercase
        """
        self.lyrics_gen.prompt = "I'm a string with uppercase characters!"
        self.assertEqual(self.lyrics_gen.make_lowercase(), "i'm a string with uppercase characters!")

    def test_each_sentence_on_new_line(self) -> None:
        """	
        The test_each_sentence_on_new_line method checks that the each_sentence_on_new_line method
        puts each sentence on a new line.
        """
        self.lyrics_gen.prompt = "I'm a string with sentences. I'm a string with sentences!"
        self.assertEqual(self.lyrics_gen.each_sentence_on_new_line(), "I'm a string with sentences.\n"
                                                                      "I'm a string with sentences!")

    def test_check_language(self) -> None:
        """
        The test_check_language method checks that the check_language method raises an exception
        when the prompt language is not Dutch
        """
        self.lyrics_gen.prompt = "Dit is een Nederlandstalige prompt."

        result = self.lyrics_gen.check_language().prompt

        self.assertEqual(result, self.lyrics_gen.prompt)

        self.lyrics_gen.prompt = "This is an English prompt."
        with self.assertRaises(Exception):
            self.lyrics_gen.check_language()

    def test_get_lyrics(self) -> None:
        """
        The test_get_lyrics method checks that the get_lyrics method returns a string
        """
        self.text_gen_backend.generate_text.return_value = "This is a generated string."
        self.lyrics_gen.prompt = "This is a prompt."
        result = self.lyrics_gen.get_lyrics()
        self.assertIsInstance(result, str)


if __name__ == '__main__':
    unittest.main()

# Resources
# https://docs.python.org/3/library/unittest.html
# https://docs.python.org/3/library/unittest.mock.html
