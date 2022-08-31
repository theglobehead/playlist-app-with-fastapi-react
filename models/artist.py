from dataclasses_json import dataclass_json
from pydantic.dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import List

from models.song import Song


@dataclass_json
@dataclass
class Artist:
    songs: List[Song] = field(default_factory=list)
    child_artists_names: List[str] = field(default_factory=list)
    parent_artist_name: str = ""

    artist_id: int = 0
    artist_uuid: str = ""
    artist_name: str = ""
    modified: datetime = datetime.utcnow()
    created: datetime = datetime.utcnow()
    is_deleted: bool = False
