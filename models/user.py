from dataclasses import dataclass
from typing import List
from dataclasses_json import dataclass_json
from models.play_list import PlayList

from models.query_object import QueryObject


@dataclass_json
@dataclass
class User(QueryObject):
    user_name: str
    password_salt: str
    hashed_password: str
    play_lists: List[PlayList]