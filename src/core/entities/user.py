from pydantic import BaseModel

class User(BaseModel):
    UserId: int
    FirstName: str
    LastName: str
    Email: str