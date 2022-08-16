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

    user_id: int = 0
    user_uuid: str = ""
    user_name: str = ""
    session_token: str = ""
    hashed_password: str = ""
    password_salt: str = ""
    modified: datetime = datetime.utcnow()
    created: datetime = datetime.utcnow()
    is_deleted: bool = False
