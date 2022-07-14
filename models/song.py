from typing import List
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from models.query_object import QueryObject


@dataclass_json
@dataclass
class Song(QueryObject):
    name: str
    artist: str
    tags: List[str]
    audio: bytes