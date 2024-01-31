from typing import Optional
from pydantic import BaseModel, Field

class Teams (BaseModel):
    name: Optional [str] = Field(None, max_length=15, min_length=4)
    admin: Optional [str] = Field(None, max_length=15, min_length=4)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "myfamily",
                "admin": "ImPablo"
            }
        }

class Username_and_team_id(BaseModel):
      name: str = Field(max_length=15, min_length=4)
      team_id: int
      class Config:
            orm_mode = True
            schema_extra = {
                "example": {
                    "name": "ImPablo",
                    "team_id": 2
                }
            }

class TeamName (BaseModel):
    name: Optional [str] = Field(None, max_length=15, min_length=4)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "myfamily"
            }
        }

class TeamId (BaseModel):
    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "22"
            }
}