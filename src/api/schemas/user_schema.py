from pydantic import BaseModel

class UserDTO(BaseModel):
    UserId: int
    FirstName: str
    LastName: str
    Email: str
