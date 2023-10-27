import dataclasses

from GenericMusicManager.gmm import Music


@dataclasses.dataclass
class HandleSpotify:
    url: str

    def __post_init__(self) -> None:
        ...

    @staticmethod
    def url_regex() -> str:
        return "spotify"

    def gen_music_class(self) -> Music:
        # with yt_dlp.YoutubeDL(self.__youtube_dlp_options) as yt:
        #     extracted_info = yt.extract_info(self.url, download=False)

        # track_name = extracted_info["title"]
        # track_artist = extracted_info["artist"]
        # track_album = extracted_info["album"]
        # track_duration = extracted_info["duration"]
        # url = extracted_info["webpage_url"]

        # temp = Music(track_name, track_artist,
        #              track_album, track_duration, url)
        # temp._download_url = extracted_info["url"]
        # temp._extracted_info = extracted_info
        # temp._parent_class = self

        # return temp
        ...
