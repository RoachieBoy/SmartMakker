import json
import re
import lyricsgenius

from lyricsgenius.types.artist import Artist
from data_collector.backends.backend_registery import ScraperBackend, register_backend
from data_collector.text_computing.text_manipulation_pipeline import TextManipulationPipeline

from data_collector.text_computing.text_manipulation_passes import (
    replace_regex_pattern,
    remove_non_alphanumeric,
    remove_text_between_brackets,
    filter_out_non_dutch,
    remove_excessive_newlines,
    remove_first_sentence,
    remove_special_unicode_character,
    remove_punctuation_if_not_preceded_by_text
)


@register_backend("genius")
class GeniusBackend(ScraperBackend):
    """
    This class is a wrapper for the lyricsgenius API
    """

    def __init__(self):
        super().__init__()

        self.artists: list[str] = []
        self.geniusApi = None
        self.max_number_of_songs: int = 0
        self.sort: str = ""
        self.albums: list[any] = []  # List can be list of lists if artist and album name is given, string if only album name

    def initialise(self, initialisation_arguments: (str, str)) -> None:
        super().initialise(initialisation_arguments)

        config = json.loads(initialisation_arguments[1])
        token: str = config['genius_token']

        if "artists" in config:
            self.artists = config['artists']
        self.max_number_of_songs = config['max_songs_pr_artists']
        self.sort = config['sort']
        self.geniusApi = lyricsgenius.Genius(token, timeout=5, sleep_time=0.2, retries=5)
        if "albums" in config:
            self.albums = config['albums']

    def get_artist_songs(self, artist_name: str) -> list:
        """
        This function returns a list of songs from the genius API.

        :param artist_name: name of the artist to search for.
        :return: list of songs.
        """
        if self.max_number_of_songs < 0:
            raise ValueError("Negative amount of songs selected, this is not allowed")

        counter = 0
        max_attempts = 5
        while counter <= max_attempts:
            try:
                temp = self.geniusApi.search_artist(artist_name, 1, self.sort)
                if not temp or temp.name.lower() != artist_name.replace('\n', '').lower():
                    return []
                artist = self.geniusApi.search_artist(artist_name, self.max_number_of_songs, self.sort)

                if type(artist) != Artist:
                    return []
                elif artist.name.lower() != artist_name.replace('\n', '').lower():
                    return []
                return artist.songs

            except TimeoutError as e:
                print(f"Timeout error: {e}\n\nTrying {max_attempts - counter} more time(s)")
                counter += 1

                continue

        return []

    def get_artist_lyrics(self, artist_name: str) -> list[str]:
        """
        This function returns a list of lyrics from the genius API.

        :param artist_name: name of the artist
        :return: list of lyrics
        """
        if not isinstance(artist_name, str):
            raise TypeError("name should be string")

        if not isinstance(self.max_number_of_songs, int):
            raise TypeError("songs should be int")

        if not isinstance(self.sort, str):
            raise TypeError("sort should be string")

        songs = self.get_artist_songs(artist_name)

        return_value = [i.lyrics for i in songs]

        return return_value

    def get_album_lyrics(self, album_name: str, artist_name: str = "") -> list[str]:
        album = self.geniusApi.search_album(album_name, artist_name)

        if album:
            album_lyrics = [track.song.lyrics for track in album.tracks]

            return album_lyrics

        return []

    def run(self) -> list[str]:
        lyrics: list[str] = []

        for artist in self.artists:
            lyrics += self.get_artist_lyrics(artist)

        if self.albums:
            for i in self.albums:
                if type(i) == tuple or type(i) == list:
                    lyrics += self.get_album_lyrics(i[0], i[1])
                else:
                    lyrics += self.get_album_lyrics(i)
        preprocess_text(lyrics)

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
            "remove_first_line": (
                remove_first_sentence,
                None
            ),
            "remove_special_unicode_character": (
                remove_special_unicode_character,
                None
            ),
            "remove_excess_newlines": (
                remove_excessive_newlines,
                None
            ),
            "remove_non_alphanumeric": (
                remove_non_alphanumeric,
                None
            ),
            "replace_embed_text": (
                replace_regex_pattern,
                [
                    r"\s*embe\w*|You might also l\w*|",
                    "",
                    re.IGNORECASE
                ]
            ),
            "replace_refrein_text": (
                replace_regex_pattern,
                [
                    r"\s*Refr(\.|:|\.:|\.\:|\(x\)|ain|ein)?|\(refrein 2x\)|",
                    "",
                    re.IGNORECASE
                ]
            ),
            "remove_text_in_brackets": (
                remove_text_between_brackets,
                [
                    r'\n\n'
                ]
            ),
            "remove_punctuation_if_not_preceded_by_text": (
                remove_punctuation_if_not_preceded_by_text,
                None
            ),
        }
    )

    pipeline.run_pipeline(lyrics)
