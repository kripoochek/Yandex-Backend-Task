from datetime import datetime
from enum import Enum
from typing import Optional, List, Union
from uuid import UUID

from pydantic import BaseModel, Field, validator

from app.exceptions import ValidationError


class ShopUnitType(str, Enum):
    """
    Represents shop unit types
    """
    OFFER = "OFFER"
    CATEGORY = "CATEGORY"


class AppBaseModel(BaseModel):
    def json(self, **kwargs):
        kwargs.setdefault("by_alias", True)
        kwargs.setdefault("exclude_unset", True)
        return super().json(exclude_none=False, **kwargs)


class DateRequest(BaseModel):
    date: datetime


class ShopUnit(AppBaseModel):
    """
    Common shop unit model.
    Represents either category or offer.
    """
    id: UUID
    name: str
    date: Union[str, datetime]
    parent_id: Optional[UUID] = Field(None, alias="parentId")
    type: ShopUnitType
    price: Optional[int]
    children: Optional[List["ShopUnit"]]


class ShopUnitImport(AppBaseModel):
    """
    One shop unit import data.
    """
    id: UUID
    name: str
    parent_id: Optional[UUID] = Field(None, alias="parentId")
    price: Optional[int]
    type: ShopUnitType

    @validator("type")
    def valid_unit(cls, v, values: dict):
        if v == ShopUnitType.CATEGORY and values["price"] is not None:
            raise ValidationError("category must have null price")

        if v == ShopUnitType.OFFER and (values["price"] is None or values["price"] < 0):
            raise ValidationError("offer price must be greater or equal to zero")
        return v


class ShopUnitStatisticUnit(AppBaseModel):
    """
    Common shop unit model statistic.
    Represents either category or offer.
    """
    id: UUID
    name: str
    date: Union[str, datetime]
    parent_id: Optional[UUID] = Field(None, alias="parentId")
    type: ShopUnitType
    price: Optional[int]


class ShopUnitStatisticResponse(AppBaseModel):
    items: List[ShopUnitStatisticUnit]


class ShopUnitRequest(AppBaseModel):
    """
    Request for import many shop units.
    """
    update_date: datetime = Field(None, alias="updateDate")
    items: List[ShopUnitImport]


class Error(BaseModel):
    """
    Base error response model
    """
    code: Optional[int]
    message: Optional[str]
