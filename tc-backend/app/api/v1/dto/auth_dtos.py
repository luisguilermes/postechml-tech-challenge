from pydantic import BaseModel


class RefreshRequest(BaseModel):
    refresh_token: str


class LoginInput(BaseModel):
    username: str
    password: str


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
