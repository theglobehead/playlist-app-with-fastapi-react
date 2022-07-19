from dataclasses_json import dataclass_json
from pydantic.dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import List

# from models.artist import Artist
from models.tag import Tag


@dataclass_json
@dataclass
class Song:
    tags: List[Tag] = field(default_factory=list)
    # artist: Artist = field(default_factory=Artist)

    id: int = 0
    name: str = ""
    artist = str = ""
    album: str = ""
    audio_path: str = ""
    modified: datetime = datetime.utcnow()
    created: datetime = datetime.utcnow()
    is_deleted: bool = False