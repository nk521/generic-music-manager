from __future__ import annotations
import dataclasses
import json
from uuid import UUID
from queue import Queue
from typing import Any, Protocol


@dataclasses.dataclass
class HandlersProtocol(Protocol):
    url: str

    def __post_init__(self) -> None:
        ...

    @staticmethod
    def url_regex() -> str:
        ...

    def gen_music_class(self) -> Music:
        ...


class CustomUUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        elif dataclasses.is_dataclass(obj):
            ret: dict[str, Any] = obj.__dict__.copy()

            for k in obj.__dict__.keys():
                if k.startswith("_"):
                    ret.pop(k)
            return ret
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
    track_name: str
    track_artist: str
    track_album: str
    track_duration: int
    url: str

    def __post_init__(self) -> None:
        self._parent_class: HandlersProtocol | None = None
        self._download_url: str | None = None
        self._extracted_info: dict[str, Any] | None = None

    def refresh(self) -> None:
        self = self._parent_class.gen_music_class()


@dataclasses.dataclass
class Playlist(Base):
    tracks: Queue[Music] = Queue()

    def get_all_tracks(self, style: str = "python"):
        ...

    def add(self, music: Music) -> None:
        self.tracks.put_nowait(music)
