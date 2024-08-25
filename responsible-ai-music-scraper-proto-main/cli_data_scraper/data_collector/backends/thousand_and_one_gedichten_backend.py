import json
import requests

from bs4 import BeautifulSoup as bs4
from data_collector.backends.backend_registery import ScraperBackend, register_backend

from data_collector.text_computing.text_manipulation_passes import (
    remove_non_alphanumeric,
    remove_text_between_brackets,
    filter_out_non_dutch,
    remove_tab_characters,
    remove_last_sentence,
    remove_special_unicode_character,
    remove_quotation_marks,
    remove_multiple_dots,
    replace_regex_pattern,
    remove_punctuation_if_not_preceded_by_text
)
from data_collector.text_computing.text_manipulation_pipeline import TextManipulationPipeline


@register_backend("1001_gedichten")
class ThousandAndOneGedichtenBackend(ScraperBackend):
    def __init__(self):
        super().__init__()

        self.base_url: str = ""
        self.page_url = ""
        self.page_amount = 0
        self.genres = []

    def initialise(self, initialisation_arguments: (str, str)) -> None:
        super().initialise(initialisation_arguments)

        config = json.loads(initialisation_arguments[1])

        self.base_url = config['base_url']
        self.page_url = config['page_url']
        self.page_amount = config['page_amount']
        self.genres = config['genres']

    def run(self) -> list[str]:
        texts: list[str] = []

        for genre in self.genres:
            for amount in range(self.page_amount + 1):
                texts += get_pages(genre=genre, base_url=self.base_url, page=amount)

        preprocess_text(texts)

        return texts


def get_poem(page_url: str):

    poem_page = bs4(requests.get(page_url).content, 'html.parser')
    poem = poem_page.find(
        'div',
        style='background: #fdfdfd; padding-left: 20px; margin: 10px 0px; border-right: 1px solid #fdfdfd;'
    )

    return poem


def get_pages(genre, base_url, page) -> list[str]:
    full_url = ""
    texts: list[str] = []

    if page > 1:
        full_url = base_url + genre + "/" + str(page) + "/"
    elif page == 1:
        full_url = base_url + genre + "/"
    elif page < 1:
        return texts

    s = bs4(requests.get(full_url).content, 'html.parser')

    page_check = s.find('div', attrs={'class': 'pages'}).find('a').find('strong')
    if page_check != None:
        page_check = page_check.get_text()

    if page_check == "1" and page != 1:
        print("Unable to obtain this page.")
        return texts
    
    stories_main_page = s.find('div', attrs={'class': 'categoryBox'})
    articles = stories_main_page.find_all('ul')

    for i in articles:
        for j in i.find_all('a'):
            link = j['href']
            poem = get_poem(page_url=base_url + link)

            if poem:
                poem = poem.find('p').get_text()
                texts.append(poem)

    return texts


def preprocess_text(lyrics: list[str]) -> None:
    """
    Preprocesses the input texts using the TextManipulationPipeline.

    :param lyrics: The texts to preprocess.
    :return: None.
    """
    pipeline = TextManipulationPipeline(
        {
            "check_language_dutch": (
                filter_out_non_dutch,
                None
            ),
            "remove_all_caps": (
                replace_regex_pattern,
                [
                    r'[A-Z]{2,}',
                    ""
                ]
            ),
            "remove_copyright_symbol": (
                replace_regex_pattern,
                [
                    r'©.*',
                    ""
                ]
            ),
            "remove_tab_characters": (
                remove_tab_characters,
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

