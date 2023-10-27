import dataclasses
import yt_dlp

from GenericMusicManager.gmm import Music


@dataclasses.dataclass
class HandleYoutube:
    url: str

    def __post_init__(self) -> None:
        self.__youtube_dlp_options = {
            "quiet":    True,
            "no_warnings": True,
            "simulate": True,
            "format": "bestaudio/best",
        }

    @staticmethod
    def url_regex() -> str:
        return "youtube"

    def gen_music_class(self) -> Music:
        with yt_dlp.YoutubeDL(self.__youtube_dlp_options) as yt:
            extracted_info = yt.extract_info(self.url, download=False)

        track_name = extracted_info["title"]
        track_artist = extracted_info["artist"]
        track_album = extracted_info["album"]
        track_duration = extracted_info["duration"]
        url = extracted_info["webpage_url"]

        temp = Music(track_name, track_artist,
                     track_album, track_duration, url)
        temp._download_url = extracted_info["url"]
        temp._extracted_info = extracted_info
        temp._parent_class = self

        return temp
