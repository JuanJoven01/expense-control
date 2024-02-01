from pydantic import BaseModel, Field
from typing import Optional

class Categories (BaseModel):
    name: str = Field(max_length=30, min_length=4)
    description: Optional[str] = Field(max_length=300, min_length=4, default=None)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Food",
                "description": "Food expenses"
            }
        }