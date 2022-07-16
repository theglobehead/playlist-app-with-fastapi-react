from datetime import datetime
from typing import List
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

from models.song import Song
from models.tag import Tag
from models.user import User

@dataclass_json
@dataclass
class Playlist:
    songs: List[Song] = field(default_factory=list)
    tags: List[Tag] = field(default_factory=list)
    owner: User = field(default_factory=User)

    id: int = 0
    name: str = ""
    modified: datetime = datetime.utcnow()
    created: datetime = datetime.utcnow()
    is_deleted: bool = False