from datetime import datetime
from uuid import UUID
from typing import Annotated

from pydantic import BaseModel, ConfigDict, AfterValidator

from domain.validators.hex_color import validate_hex_color


class CreateSubjectInput(BaseModel):
    name: str
    color: Annotated[str, AfterValidator(validate_hex_color)] # TODO: add validations

class UpdateSubjectInput(BaseModel):
    name: str | None = None
    color: Annotated[str, AfterValidator(validate_hex_color)] | None = None # TODO: add validations

class SubjectOutput(BaseModel):
    id: UUID
    name: str
    color: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PaginatedSubjectOutput(BaseModel):
    results: list[SubjectOutput]
    total: int
    per_page: int

    model_config = ConfigDict(from_attributes=True)
