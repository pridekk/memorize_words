from datetime import datetime
from typing import Any, Optional, List

from pydantic import BaseModel, Field


class Meaning(BaseModel):
    m_id: str
    meaning: str
    verb: str
    s_count: int
    d_count: int
    created_at: datetime
    updated_at: datetime
    priority: int

    def __eq__(self, other):
        return self.priority == other.priority and self.s_count == other.s_count

    def __lt__(self, other):
        return self.priority > other.priority or self.s_count < other.s_count


class Word(BaseModel):
    _id: str
    word: Optional[str] = Field(alias="_id")
    s_count: int
    priority: int
    meanings: List[Meaning]

    def __eq__(self, other):
        return self.priority == other.priority and self.s_count == other.s_count

    def __lt__(self, other):
        return self.priority > other.priority or self.s_count < other.s_count


class WordRequest(BaseModel):
    word: str
    meanings: List[str]
