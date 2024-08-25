import unittest
import re

from data_collector.text_computing.text_manipulation_passes import (
    replace_regex_pattern,
    to_lowercase,
    replace_string,
    remove_non_alphanumeric,
    remove_text_between_brackets,
    filter_out_non_dutch,
    each_sentence_on_new_line,
    remove_excessive_newlines,
    remove_first_sentence,
    remove_last_sentence,
    remove_tab_characters,
    remove_special_unicode_character,
    remove_multiple_dots,
    remove_punctuation_if_not_preceded_by_text
)


class TestTextManipulationPasses(unittest.TestCase):
    """
    Test the various text manipulation passes to ensure they work as expected.
    """
    def test_replace_regex_pattern(self) -> None:
        """
        Test the replace regex function to ensure that it works as expected.
        """
        result = replace_regex_pattern(
            input_string="Hallo, Wereld!",
            to_replace=r"Hallo",
            replace_with="Hi",
            flags=re.IGNORECASE
        )

        self.assertEqual(result, "Hi, Wereld!")

    def test_to_lowercase(self) -> None:
        """
        Ensures the output of the to_lowercase function is indeed lowercase.
        """
        result = to_lowercase(input_string="Hallo, Wereld!")
        self.assertEqual(result, "hallo, wereld!")

    def test_remove_non_alphanumeric(self) -> None:
        """
        Ensures all non-alphanumeric characters specified are removed with the remove_non_alphanumeric
        function.
        """
        result = remove_non_alphanumeric(input_string="Hallo, Wereld! $#@")
        self.assertEqual(result, "Hallo, Wereld! ")

    def test_replace_string(self) -> None:
        """
        Check that the replace_string function works as expected.
        """
        result = replace_string(
            to_manipulate="Hallo, Wereld!",
            to_replace="Hallo",
            replace_with="Hi"
        )

        self.assertEqual(result, "Hi, Wereld!")

    def test_remove_text_between_brackets(self) -> None:
        """
        Ensure that the text between brackets is removed with the remove_text_between_brackets
        function.
        """
        result = remove_text_between_brackets(input_string="Hallo (Wereld) [CAPS] werkt dit?", to_replace_with=" ")
        self.assertEqual(result, "Hallo werkt dit?")

    def test_filter_out_non_dutch(self) -> None:
        """
        Check that all non-dutch text is filtered out with the filter_out_non_dutch
        function.
        """
        result_english = filter_out_non_dutch(input_string="Hello world this is a test sentence!")
        self.assertEqual(result_english, "")

        result_french = filter_out_non_dutch(input_string="Bonjour le monde, ceci est une phrase de test!")
        self.assertEqual(result_french, "")

        result_dutch = filter_out_non_dutch(input_string="Hallo wereld dit is een test zin!")
        self.assertEqual(result_dutch, "Hallo wereld dit is een test zin!")

    def test_remove_excess_newlines(self) -> None:
        """
        Check that all excess newlines get removed with the remove_excessive_newlines
        function.
        """
        result = remove_excessive_newlines("Hallo iedereen!\n\n\nIk check even of de newlines "
                                           "kloppen.\n\n")

        self.assertEqual(result, "Hallo iedereen!\n\nIk check even of de newlines kloppen.\n\n")

    def test_each_sentence_on_new_line(self) -> None:
        """
        Check that all sentences start on a new line.
        """
        result = each_sentence_on_new_line("Hallo mensen!Dit is een test. Ik hoop dat dit werkt?")

        self.assertEqual(result, "Hallo mensen!\nDit is een test.\nIk hoop dat dit werkt?\n")

    def test_remove_sentences(self) -> None:
        """
        Check if the correct sentences are removed.
        """
        result_first_sentence = remove_first_sentence("Dit moet weg.\nAls het goed is, blijft dit staan.")
        self.assertEqual(result_first_sentence, "Als het goed is, blijft dit staan.")

        result_last_sentence = remove_last_sentence("Dit moet niet weg.\nAls het goed is, blijft dit niet staan.")
        self.assertEqual(result_last_sentence, "Dit moet niet weg.")

    def test_remove_tab_characters(self) -> None:
        """
        Check that all tab characters are removed.
        """
        result = remove_tab_characters("Hallo\tiedereen!\t\t\t\tIk\thoop\tdat\tdit\twerkt.")

        self.assertEqual(result, "Halloiedereen!Ikhoopdatditwerkt.")

    def test_remove_special_unicode_character(self) -> None:
        """
        Check that all special unicode characters are removed.
        """
        result = remove_special_unicode_character("Ik hoop dat dit werkt.\x9d")

        self.assertEqual(result, "Ik hoop dat dit werkt.")

    def test_remove_multiple_dots(self) -> None:
        """
        Check that all multiple dots are removed and replaced with a single dot.
        """
        result = remove_multiple_dots("Hallo iedereen! Ik hoop dat dit werkt....")

        self.assertEqual(result, "Hallo iedereen! Ik hoop dat dit werkt.")

    def test_remove_punctuation_if_not_preceded_by_text(self) -> None:
        """
        Check that all punctuation is removed if not preceded by text.
        """
        result = remove_punctuation_if_not_preceded_by_text("...Dit is een test zin! Ik hoop dat het, werkt.")

        self.assertEqual(result, "Dit is een test zin! Ik hoop dat het, werkt.")


if __name__ == '__main__':
    unittest.main()

