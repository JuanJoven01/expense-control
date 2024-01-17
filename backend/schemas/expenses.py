from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Expenses (BaseModel):
    name: str = Field(max_length=30, min_length=4)
    description: Optional[str] = Field(max_length=300, min_length=4)
    date: Optional[datetime] = Field(default=datetime.now()) ##
    amount: float = Field(gt=0)
    user_id: Optional[int]
    team_id: Optional[int]
    wallet_id: int
    category_id: int
    

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Food",
                "description": "Food expenses",
                "date": "2021-01-01",
                "amount": 100.00
            }
        }