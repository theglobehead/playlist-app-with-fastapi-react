from dataclasses_json import dataclass_json
from pydantic.dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import List

from controllers.constants import SONG_PATH
from models.tag import Tag


@dataclass_json
@dataclass
class Song:
    tags: List[Tag] = field(default_factory=list)

    song_id: int = 0
    song_uuid: str = ""
    song_name: str = ""
    audio_path: str = SONG_PATH[1:]
    file_type: str = ".mp3"
    artist = str = ""
    album: str = ""
    artist_id: int = 0
    modified: datetime = datetime.utcnow()
    created: datetime = datetime.utcnow()
    is_deleted: bool = False
