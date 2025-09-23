from pydantic import BaseModel, Field
from typing import Annotated


class Token(BaseModel):
    access_token: Annotated[str, Field(description="Token for getting access to API")]
    token_type: Annotated[str, Field(description="Token type")]

class TokenData(BaseModel):
    username: Annotated[str | None, Field(default=None, description="Username of user from database")]

class User(BaseModel):
    username: Annotated[str, Field(description="Username of user from database")]

class UserInDB(User):
    hashed_password: Annotated[str, Field(description="Hashed user password from database")]
