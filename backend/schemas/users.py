from pydantic import BaseModel, Field

class User (BaseModel):
    name: str = Field(max_length=15, min_length=4,)
    password: str = Field(min_length=8)

    class Config:
            orm_mode = True
            schema_extra = {
                "example": {
                    "name": "ImPablo",
                    "password": "verysecurepassword"
                }
            }