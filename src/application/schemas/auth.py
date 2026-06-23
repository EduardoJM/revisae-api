from pydantic import BaseModel

class LoginInput(BaseModel):
    email: str
    password: str

class TokenOutput(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshInput(BaseModel):
    refresh_token: str
