import re

from lingua import Language, LanguageDetectorBuilder


def replace_regex_pattern(
        input_string: str,
        to_replace: str,
        replace_with: str,
        flags: re.RegexFlag = 0
) -> str:
    """
    Used to execute a regular expression on the string.

    :param input_string: The string to manipulate.
    :param replace_with: string to replace pattern with.
    :param to_replace: the pattern to replace.
    :param flags: the flags to apply in the regular expression. Default is 0,
    which means no flags are applied.
    :return: The manipulated string.
    """
    return re.sub(pattern=to_replace, repl=replace_with, string=input_string, flags=flags)


def replace_string(
        to_manipulate: str,
        to_replace: str,
        replace_with: str
) -> str:
    """
    Replace a string with a new cleaned string.

    :param to_manipulate: text to clean.
    :param to_replace: specific text you wish to replace
    :param replace_with: text you wish to replace the old text with.
    :return: a string containing the new text.
    """
    return to_manipulate.replace(to_replace, replace_with)


def to_lowercase(input_string: str) -> str:
    """
    Lower the case of the text in the input string.

    :param input_string: text to change to lowercase.
    :return: the lowercase string.
    """
    return input_string.lower()


def remove_non_alphanumeric(input_string: str) -> str:
    """
    Remove all non-alphanumeric characters from the string,
    keeping a set of characters that are commonly used in text.

    :param input_string: string to manipulate.
    :return: input string containing only alphanumeric characters.
    """
    return re.sub(
        pattern=r"[^a-zA-z0-9 .,\'\"?!; \n]",
        repl="",
        string=input_string
    )

def remove_text_between_brackets(input_string: str, to_replace_with: str) -> str:
    """
    Remove all text from between brackets -- both () and []

    :param input_string: string to manipulate.
    :param to_replace_with: string to replace the text between brackets with.
    :return: input string with all text between brackets removed.
    """
    # Remove text between parentheses ()
    input_string = re.sub(r'\([^()]*\)', '', input_string)

    # Remove text between square brackets []
    input_string = re.sub(r'\[[^\[\]]*]', '', input_string)

    # Remove excessive spaces caused by the removal of text between brackets
    input_string = re.sub(r'\s{2,}', to_replace_with, input_string)

    return input_string.strip()


def each_sentence_on_new_line(input_string: str) -> str:
    """
    Puts each sentence on a new line

    :param input_string: string to manipulate.
    :return: input string with each sentence on a new line.
    """
    new_line_characters = r"(?<=[.!?])(\s)*"

    input_string = re.sub(new_line_characters, "\n", input_string)

    return input_string


def remove_excessive_newlines(input_string: str) -> str:
    """
    Removes all newlines that occur more than twice in a row.

    :param input_string: string to manipulate.
    :return: input string with excessive newlines removed.
    """
    return re.sub(r"\n{3,}", "\n\n", input_string)


def remove_tab_characters(input_string: str) -> str:
    """
    Removes all tab characters from the input string.

    :param input_string: string to manipulate.
    :return: input string with tabs removed.
    """
    cleaned_string = input_string.replace('\t', '')
    return cleaned_string


def filter_out_non_dutch(input_string: str) -> str:
    """
    Check the language of the input_text.

    :param input_string: the text to check the language of.
    :return: the input string if it is in Dutch, otherwise an empty string
    that will be removed from the list later.
    """
    language_detector = LanguageDetectorBuilder.from_all_languages(). \
        with_preloaded_language_models().build()

    language = language_detector.detect_language_of(input_string)

    if language != Language.DUTCH:
        return ""
    else:
        return input_string


def remove_first_sentence(input_string: str) -> str:
    """
    Remove the first sentence of a given input string.

    :param input_string: string to manipulate.
    :return: input string containing all but the first sentence.
    """
    # Remove any newlines before the first sentence
    input_string = re.sub(r'^\s*\n', '', input_string)

    # Remove the first sentence
    input_string = re.sub(r'^.*?\n', '', input_string)

    # Remove any newlines after the first sentence
    input_string = re.sub(r'^\s*\n', '', input_string)

    return input_string


def remove_last_sentence(input_string: str) -> str:
    """
    Removes the last sentence from the input string.

    :param input_string: text to manipulate.
    :return: input string containing all but the last sentence.
    """
    # Remove all newlines at the end of a text
    input_string = input_string.rstrip()

    # Split into an array of lines
    lines = input_string.split('\n')

    if len(lines) > 1:
        lines.pop()

    input_string = '\n'.join(lines)

    # Remove spaces at the end of the text
    input_string = input_string.rstrip()

    return input_string


def remove_special_unicode_character(input_string: str) -> str:
    """
    Removes the '\x9d' character from the input string using sub.

    :param input_string: text to manipulate.
    :return: input string with the '\x9d' character removed.
    """
    return input_string.replace('\x9d', '')


def remove_quotation_marks(text: str) -> str:
    """
    Removes all quotation marks and single quotes from the input text.

    :param text: The text to manipulate.
    :return: Text with quotation marks and single quotes removed.
    """
    cleaned_text = text.replace('"', '').replace("'", '').replace('’', '')
    return cleaned_text


def remove_multiple_dots(text: str) -> str:
    """
    Removes all instances of '.' that occur more than once consecutively in the input text.

    :param text: The text to manipulate.
    :return: Text with multiple consecutive dots removed.
    """
    return re.sub(r'\.+', '.', text)


def remove_punctuation_if_not_preceded_by_text(input_string: str) -> str:
    """
    Remove punctuation marks if they are not preceded by
    other text in the input string.

    :param input_string: string to manipulate.
    :return: input string with punctuation marks removed
    if they are not preceded by other text.
    """
    no_letter_behind = r'(?<![a-zA-Z])'
    single_punctuation = r'[^\w\s]'
    consecutive_punctuation = r'(?<![a-zA-Z])[^\w\s](?![a-zA-Z])'

    pattern = no_letter_behind + single_punctuation + '|' + consecutive_punctuation
    return re.sub(pattern, '', input_string)
