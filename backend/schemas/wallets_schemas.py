from pydantic import BaseModel, Field
from typing import Optional

class Wallets (BaseModel):
    name: str = Field(max_length=30, min_length=4)
    description: Optional[str] = Field(max_length=300, min_length=4)
    balance: float = Field(default=0)
    user_id: Optional[int]
    team_id: Optional[int]
    

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Bank",
                "description": "Bank account",
                "balance": 10.00,
            }
        }