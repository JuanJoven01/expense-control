from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Expenses (BaseModel):
    name: str = Field(max_length=30, min_length=4)
    description: Optional[str] = Field(max_length=300, min_length=4, default=None)
    date: Optional[datetime] = Field(default=datetime.now()) 
    amount: float = Field(gt=0)
    wallet_id: int
    category_id: int
    

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "FAC",
                "description": "Office income",
                "date": "2021-01-01",
                "amount": 101.00
            }
        }

class ExpensesUpdate (BaseModel):
    name: str = Field(max_length=30, min_length=4)
    description: Optional[str] = Field(max_length=300, min_length=4, default=None)
    date: Optional[datetime] = Field(default=datetime.now()) 
    amount: float = Field(gt=0)
    wallet_id: int
    category_id: int
    expense_id: int
    

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "FAC",
                "description": "Office income",
                "date": "2021-01-01",
                "amount": 101.00
            }
        }