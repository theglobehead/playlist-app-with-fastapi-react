from dataclasses_json import dataclass_json
from pydantic.dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import List

from models.playlist import Playlist

@dataclass_json
@dataclass
class User:
    playlists: List[Playlist] = field(default_factory=list)

    id: int = 0
    uuid: str = ""
    name: str = ""
    hashed_password: str = ""
    password_salt: str = ""
    modified: datetime = datetime.utcnow()
    created: datetime = datetime.utcnow()
    is_deleted: bool = False