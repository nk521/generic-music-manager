import dataclasses
import json
from uuid import UUID
# from queue import Queue
from typing import Any

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
    track_name: str
    track_artist: str
    track_album: str
    track_duration: int
    url: str
    _download_url: str | None = None
    _extracted_info: dict[str, Any] | None = None

# @dataclasses.dataclass
# class Playlist(Base):
#     tracks: Queue[Music] = Queue()
    
#     def get_all_tracks(self, style: str = "python"):
#         ...
    
#     def add(self, music: Music) -> None:
#         self.tracks.put_nowait(music)

    

# some = Music.from_youtube(url="https://music.youtube.com/watch?v=tPEt7pJ1zMs&si=Lx_BIo9QcjpxxarV")
# breakpoint()