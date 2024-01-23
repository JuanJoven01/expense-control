from typing import Optional
from pydantic import BaseModel, Field

class Teams (BaseModel):
    name: Optional [str] = Field(max_length=15, min_length=4)
    admin: Optional [str] = Field(max_length=15, min_length=4  )

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "myfamily",
                "admin": "ImPablo"
            }
        }