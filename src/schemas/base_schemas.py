from typing import Optional
from uuid import UUID
from pydantic import BaseModel
import orjson


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()

class BaseOrjsonModel(BaseModel):
    model_config = {"model_validate": orjson.loads, "model_dump": orjson_dumps}


class BaseView(BaseOrjsonModel):
    id: UUID

    creator: Optional[str] = None
    modifier: Optional[str] = None
    creator_id: Optional[str | UUID] = None
    modifier_id: Optional[str | UUID] = None