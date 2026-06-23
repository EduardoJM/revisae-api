from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class RegisterUserRequest(BaseModel):
    email: EmailStr = Field(examples=["alice@example.com"])
    password: str = Field(min_length=8, examples=["s3cur3P@ss"])
    full_name: str = Field(min_length=2, max_length=200, examples=["Alice Silva"])

class UserResponse(BaseModel):
    id: UUID
    email: str
    full_name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
