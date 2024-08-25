import json
import requests

from bs4 import BeautifulSoup as bs4
from data_collector.text_computing.text_manipulation_pipeline import TextManipulationPipeline
from ftfy import fix_text
from data_collector.backends.backend_registery import ScraperBackend, register_backend

from data_collector.text_computing.text_manipulation_passes import (
    remove_non_alphanumeric,
    remove_text_between_brackets,
    filter_out_non_dutch,
    each_sentence_on_new_line,
    remove_excessive_newlines,
    remove_last_sentence,
    remove_special_unicode_character,
    remove_quotation_marks,
    remove_multiple_dots,
    remove_punctuation_if_not_preceded_by_text,
)


@register_backend("1001_stories")
class ThousandAndOneStories(ScraperBackend):
    """
    This class is a wrapper for the short stories website
    """

    def __init__(self) -> None:
        super().__init__()

        self.base_url = ""
        # What should come after the base url to get to the correct page with the wildcard {} for the number
        self.page_url = ""
        self.amount = 0
        self.genres = []

    def initialise(self, initialisation_arguments: (str, str)) -> None:
        super().initialise(initialisation_arguments)

        config = json.loads(initialisation_arguments[1])

        self.base_url = config['base_url']
        self.page_url = config['page_url']
        self.amount = config['amount']
        self.genres = config['genres']

    def run(self) -> list[str]:
        texts: list[str] = []

        for genre in self.genres:
            texts += scroll_trough_pages(
                genre=genre,
                base_url=self.base_url,
                addpage=self.page_url,
                songs=self.amount
            )

        preprocess_text(texts)

        return texts


def get_text_from_page(base_url, url) -> str:
    """
    Get the actual text content from the website

    :param url: url to get the story from
    :param base_url: base url of the website
    :return: texts on page
    """
    s = bs4(requests.get(base_url + url).content, 'html.parser')

    story_html = s.find(
        'div',
        {
            'style': "padding-left: 20px; margin: 10px 0px;"
        }
    )

    return fix_text(story_html.find('p').get_text())


def get_start_page(url: str, base_url, limit=0) -> list[str]:
    """
    Get page with list of stories and get the texts of these stories
    :param url: complete url of page to scrape
    :param base_url: base url of website
    :param limit: how many items to return per this page
    :return: list of all texts of page
    """

    print(f"{limit} left")

    s = bs4(requests.get(url).content, 'html.parser')
    stories_html = s.find('div', attrs={'class': 'categoryBox'})
    articles = stories_html.find_all('ul')
    texts: list[str] = []

    for i in articles:
        for j in i.find_all('a'):
            if len(texts) >= limit:
                break

            link = j['href']

            texts.append(get_text_from_page(base_url, link))

    return texts


def scroll_trough_pages(genre, base_url, addpage, songs: 40) -> list[str]:
    """
    Go through amount of necessary pages to get the amount of specified songs

    :param songs: amount of songs to get
    :param genre: The genre (and subsequent page) to scrape
    :param base_url: the base url of the website
    :param addpage: the format to get the paginated url
    :return: list of texts got from the website
    """

    url = base_url + genre + '/'
    counter = 0
    startpage = 1
    lyrics: list[str] = []

    while counter < songs:
        # Get the appropriate urls to scrape whilst keeping under a counter.
        # Give a limit so that the method will only get the appropriate amount of songs instead of everything on a page
        lyrics += get_start_page(url, base_url, songs - counter)
        if len(lyrics) - counter != 50:
            # Assume that if the difference between the new and old counter isn't fifty
            # it's because there aren't enough stories and stop looking to avoid duplicates
            break
        counter = len(lyrics)
        startpage += 1
        url = base_url + genre + '/' + str.format(addpage, startpage)

    return lyrics


def preprocess_text(lyrics: list[str]) -> None:
    """
    Preprocesses the text using the text_manipulation_pipeline.

    :param lyrics: the lyrics to preprocess.
    """
    pipeline = TextManipulationPipeline(
        {
            "check_language_dutch": (
                filter_out_non_dutch,
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
            "remove_last_sentence": (
                remove_last_sentence,
                None
            ),
            "set_every_sentence_on_new_line": (
                each_sentence_on_new_line,
                None
            ),
            "remove_excessive_newlines": (
                remove_excessive_newlines,
                None
            ),
            "remove_non_alphanumeric": (
                remove_non_alphanumeric,
                None
            ),
            "remove_multiple_dots": (
                remove_multiple_dots,
                None
            ),
            "remove_text_in_brackets": (
                remove_text_between_brackets,
                [
                    " "
                ]
            ),
            "remove_punctuation_if_not_preceded_by_text": (
                remove_punctuation_if_not_preceded_by_text,
                None
            ),
        }
    )

    pipeline.run_pipeline(lyrics)
