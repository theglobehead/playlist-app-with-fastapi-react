from dataclasses import dataclass
from datetime import datetime
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Tag:
    id: int = 0
    name: str = ""
    modified: datetime = datetime.utcnow()
    created: datetime = datetime.utcnow()
    is_deleted: bool = False