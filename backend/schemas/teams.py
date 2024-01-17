from pydantic import BaseModel, Field

class Teams (BaseModel):
    name: str = Field(max_length=15, min_length=4)
    admin: str = Field(max_length=15, min_length=4  )

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "myfamily",
                "admin": "ImPablo"
            }
        }