from enum import Enum
from typing import Optional, List
from pydantic import BaseModel


class ShopUnitType(Enum):
    offer = 1
    category = 2


class ShopUnitChildren:
    id: str
    name: str
    date: str
    parentId: str
    type: ShopUnitType
    price: Optional[int]
    children: Optional[List["ShopUnitChildren"]]


class ShopUnit(BaseModel):
    id: str
    name: str
    date: str
    parentId: str
    type: ShopUnitType
    price: Optional[int]
    children: Optional[List["ShopUnit"]]


class ShopUnitImport(BaseModel):
    id: str
    name: str
    parentId: Optional[str]
    price: Optional[int]
    type: str


class ShopUnitRequest(BaseModel):
    items: List["ShopUnitImport"]
    updateDate: str


# ShopUnitStatisticUnit
# ShopUnitStatisticResponse

class Error(BaseModel):
    code: Optional[int]
    message: Optional[str]
