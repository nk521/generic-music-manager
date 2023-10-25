import dataclasses
import json
from uuid import UUID, uuid4
from queue import Queue
from typing import TYPE_CHECKING, Any
import yt_dlp

class CustomUUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        elif dataclasses.is_dataclass(obj):
                return obj.__dict__
        return json.JSONEncoder.default(self, obj)

@dataclasses.dataclass
class Base:
    def to_json(self) -> None:
        return json.dumps(self, cls=CustomUUIDEncoder)
    
    @classmethod
    def from_json(cls, json_data: dict[str, Any] | str) -> dict[str, Any]:
        if isinstance(json_data, str):
            json_data = json.loads(json_data)

        return cls(**json_data)

@dataclasses.dataclass
class Music(Base):
    url: str
    track_name: str | None = None
    track_artist: str | None = None
    track_album: str | None = None
    track_duration: int | None = None

    def __post_init__(self) -> None:
        self.extracted_info: dict[str, Any] | None = None
        self.__download_url: str | None = None
        self.__youtube_dlp_options = {
            "quiet":    True,
            "no_warnings": True,
            "simulate": True,
            "format": "bestaudio/best",
        }
        self.extract_info()
    
    # extractions should be under classmethod
    def extract_info(self) -> None:
        with yt_dlp.YoutubeDL(self.__youtube_dlp_options) as yt:
            self.extracted_info = yt.extract_info(self.url, download=False)
            self.track_name = self.extracted_info["title"]
            self.track_artist = self.extracted_info["artist"]
            self.track_album = self.extracted_info["album"]
            self.track_duration = self.extracted_info["duration"]
            self.__download_url = self.extracted_info["url"]
    
    @classmethod
    def from_youtube(cls, url: str, add_download_url: bool = True):
        return cls(url=url)
    
    @property
    def download_url(self) -> str:
        if not self.__download_url:
            self.extract_info()

        return self.__download_url

@dataclasses.dataclass
class Playlist(Base):
    tracks: Queue[Music] = Queue()
    
    def get_all_tracks(self, style: str = "python"):
        ...
    
    def add(self, music: Music) -> None:
        self.tracks.put_nowait(music)

    

some = Music.from_youtube(url="https://music.youtube.com/watch?v=tPEt7pJ1zMs&si=Lx_BIo9QcjpxxarV")
breakpoint()