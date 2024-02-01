from pydantic import BaseModel, Field
from typing import Optional

class Wallets (BaseModel):
    name: str = Field(max_length=30, min_length=4)
    description: Optional[str] = None
    balance: Optional[float] = None
    user_id: Optional[int] = None
    team_id: Optional[int] = None
    

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Bank",
                "description": "Bank account",
                "balance": 10.00,
            }
        }

