from dataclasses_json import dataclass_json
from pydantic.dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import List

from models.song import Song
from models.tag import Tag
# from models.user import User

@dataclass_json
@dataclass
class Playlist:
    songs: List[Song] = field(default_factory=list)
    tags: List[Tag] = field(default_factory=list)
    # owner: User = field(default_factory=User)

    id: int = 0
    uuid: str = ""
    name: str = ""
    owner_user_id: str = ""
    modified: datetime = datetime.utcnow()
    created: datetime = datetime.utcnow()
    is_deleted: bool = False