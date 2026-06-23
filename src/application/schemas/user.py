from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class RegisterUserInput(BaseModel):
    email: str
    password: str
    full_name: str

class UserOutput(BaseModel):
    id: UUID
    email: str
    full_name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
