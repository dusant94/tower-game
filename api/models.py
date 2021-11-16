from pydantic import BaseModel
from typing import Optional
from fastapi import Query


# ---- Example models for input request and output response
class SomeData(BaseModel):
    id: str
    name: str


class InputExample(BaseModel):
    example_int: int
    example_int_with_default: int = 0
    example_data: SomeData
    example_nullable_data: Optional[SomeData]


class OutputInteger(BaseModel):
    data: int


class OutputDefender(BaseModel):

    # Use this to return pydantic model from SQLAlchemy model
    class Config:
        orm_mode = True

class DefenderRequest(BaseModel):
    nickname: str = Query(None, min_length=1)

class DefenderResponse(BaseModel):
    id: int
    towerName: str
    towerHealth: int
    towerDefense: int
    towerDefenders: int
    enemyTowerName: str
    enemyTowerHealth: int
    serverUri: str

    class Config:
        orm_mode = True
 