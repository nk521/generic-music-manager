import dataclasses
import json
from uuid import UUID, uuid4
from queue import Queue
from typing import TYPE_CHECKING, Any
import random
import dacite

class CustomUUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        elif dataclasses.is_dataclass(obj):
                return obj.__dict__
        return json.JSONEncoder.default(self, obj)

@dataclasses.dataclass
class Base:
    def __post_init__(self) -> None:
        self.id = uuid4()

    def to_json(self) -> None:
        return json.dumps(self, cls=CustomUUIDEncoder)
    
    @classmethod
    def from_object(cls, json_data: dict[str, Any] | str) -> dict[str, Any]:
        if isinstance(json_data, str):
            json_data = json.loads(json_data)
        
        id = json_data.pop("id")
        
        temp_cls = cls(**json_data)
        temp_cls.id = UUID(id)
        return temp_cls

@dataclasses.dataclass
class Music(Base):
    track_name: str
    track_artist: str
    track_album: str
    track_duration: int

@dataclasses.dataclass
class Playlist(Base):
    tracks: Queue[Music] = Queue()
    
    def get_all_tracks(self, style: str = "python"):
        ...
    
    def add(self, music: Music) -> None:
        self.tracks.put_nowait(music)

    

