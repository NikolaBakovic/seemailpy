from datetime import datetime

from pydantic import BaseModel, Field


class TrackerCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    recipient: str = Field(default="", max_length=120)
    subject: str = Field(default="", max_length=200)


class ViewDB(BaseModel):
    id: str
    ip: str
    country: str
    user_agent: str
    created_at: datetime
    request_headers: dict[str, str]


class ContentDB(TrackerCreate):
    id: str
    link: str
    user: int
    views: list[ViewDB]
    created_at: datetime
