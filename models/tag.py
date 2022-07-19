from dataclasses_json import dataclass_json
from pydantic.dataclasses import dataclass
from datetime import datetime


@dataclass_json
@dataclass
class Tag:
    id: int = 0
    name: str = ""
    modified: datetime = datetime.utcnow()
    created: datetime = datetime.utcnow()
    is_deleted: bool = False