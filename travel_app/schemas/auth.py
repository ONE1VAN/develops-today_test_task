from pydantic import BaseModel


class LoginRequest(BaseModel):
    nick: str
    password: str


class UserCreateModel(BaseModel):
    nick: str
    password: str


class UserResponseModel(BaseModel):
    id: int
    nick: str

    model_config = {"from_attributes": True}
