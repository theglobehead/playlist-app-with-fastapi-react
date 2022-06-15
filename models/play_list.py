from typing import List
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from modules.models.song import Song
from modules.models.query_object import QueryObject


@dataclass_json
@dataclass
class PlayList(QueryObject):
    name: str
    tags: List[str]
    songs: List[Song]