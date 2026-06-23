from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class CreateSubjectRequest(BaseModel):
    name: str = Field(max_length=200, examples=["Math"])
    color: str = Field(examples=["#ffffff"]) # TODO: validate color


class SubjectResponse(BaseModel):
    id: UUID
    name: str
    color: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PaginatedSubjectResponse(BaseModel):
    results: list[SubjectResponse]
    total: int

    model_config = ConfigDict(from_attributes=True)
