import json
import requests

from bs4 import BeautifulSoup as bs4
from data_collector.backends.backend_registery import ScraperBackend, register_backend
from data_collector.text_computing.text_manipulation_passes import (
    filter_out_non_dutch,
    remove_non_alphanumeric,
    remove_text_between_brackets,
    remove_first_sentence,
    remove_excessive_newlines,
    each_sentence_on_new_line,
    remove_special_unicode_character,
    remove_quotation_marks,
    remove_last_sentence,
    remove_multiple_dots,
    remove_punctuation_if_not_preceded_by_text,
)
from data_collector.text_computing.text_manipulation_pipeline import TextManipulationPipeline


@register_backend("short_stories")
class ShortStories(ScraperBackend):
    """
    This class is a wrapper for the short stories website
    """

    def __init__(self) -> None:
        super().__init__()

        self.base_url: str = ""
        # What should come after the base url to get to the correct page with the wildcard {} for the number
        self.page_url: str = ""
        self.amount: int = 0

    def initialise(self, initialisation_arguments: (str, str)) -> None:
        super().initialise(initialisation_arguments)

        config = json.loads(initialisation_arguments[1])

        self.base_url = config['base_url']
        self.page_url = config['page_url']
        self.amount = config['amount']

    def run(self) -> [str]:
        texts = scroll_trough_pages(
            self.base_url,
            self.page_url,
            self.amount
        )

        preprocess_text(texts)

        return texts


def get_text_from_page(url) -> str:
    """
    This function returns the text from a given url

    :param url: The url to get the text from
    :return: The text from the url
    """

    s = bs4(
        requests.get(url).content,
        'html.parser'
    )

    story_html = s.find(
        'div',
        {
            'class': "post-content single-post-content"
        }
    )

    return story_html.get_text()


def get_start_page(url: str, limit=0) -> list[str]:
    """
    This function returns the text from the start page of the website

    :param url: The url to get the text from
    :param limit: The amount of stories to get
    :return: The text from the start page
    """

    print(f"{limit} left")

    s = bs4(
        requests.get(url).content,
        'html.parser'
    )
    stories_html = s.find(
        'div',
        attrs={
            'id': 'content',
            'class': 'content content-home'
        }
    )
    articles = stories_html.find_all('article')
    texts: list[str] = []

    for i in articles:
        if len(texts) >= limit:
            break

        inner_post = i.find(
            'div',
            attrs=
            {
                'class': 'post-inner'
            }
        )

        a = inner_post.find('a')
        link = a['href']

        texts.append(get_text_from_page(link))

    return texts


def scroll_trough_pages(base_url, addpage, amount: 40) -> list[str]:
    """
    This function scrolls through the pages of the website and returns the text from the pages

    :param base_url: The base url of the website
    :param addpage: The url to add to the base url to get to the next page
    :param amount: The amount of stories to get
    :return: The text from the pages
    """

    url = base_url
    counter = 0
    startpage = 1
    lyrics: list[str] = []

    while counter < amount:
        # Get the appropriate urls to scrape whilst keeping under a counter.
        # Give a limit so that the method will only get the appropriate amount of songs instead of everything on a page
        lyrics += get_start_page(
            url,
            amount - counter
        )
        if len(lyrics) - counter != 6:
            # Assume that if the difference between the new and old counter isn't fifty
            # it's because there aren't enough stories and stop looking to avoid duplicates
            break
        counter = len(lyrics)
        startpage += 1
        url = base_url + str.format(addpage, startpage)

    return lyrics


def preprocess_text(lyrics: list[str]) -> None:
    pipeline = TextManipulationPipeline(
        {
            "filter_out_non_dutch": (
                filter_out_non_dutch,
                None
            ),
            "remove_first_sentence": (
                remove_first_sentence,
                None
            ),
            "remove_quotation_marks": (
                remove_quotation_marks,
                None
            ),
            "remove_special_unicode_character": (
                remove_special_unicode_character,
                None
            ),
            "remove_excessive_newlines": (
                remove_excessive_newlines,
                None
            ),
            "newline_after_punctuation": (
                each_sentence_on_new_line,
                None
            ),
            "remove_brackets": (
                remove_text_between_brackets,
                [
                    " "
                ]
            ),
            "remove_multiple_dots": (
                remove_multiple_dots,
                None
            ),
            "remove_special_characters": (
                remove_non_alphanumeric,
                None
            ),
            "remove_punctuation_if_not_preceded_by_text": (
                remove_punctuation_if_not_preceded_by_text,
                None
            ),
        }
    )

    pipeline.run_pipeline(lyrics)

