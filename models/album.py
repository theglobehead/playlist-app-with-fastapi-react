from dataclasses_json import dataclass_json
from pydantic.dataclasses import dataclass
from datetime import datetime
from dataclasses import field
from typing import List

from models.artist import Artist
from models.song import Song
from models.tag import Tag

@dataclass_json
@dataclass
class Album:
    songs: List[Song] = field(default_factory=list)
    tags: List[Tag] = field(default_factory=list)
    artist: Artist = field(default_factory=Artist)

    album_id: int = 0
    album_name: str = ""
    modified: datetime = datetime.utcnow()
    created: datetime = datetime.utcnow()
    is_deleted: bool = False