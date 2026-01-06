from typing import List, Optional
from pydantic import BaseModel
from enum import Enum


class DiscountType(str, Enum):
    PERCENTAGE = "PERCENTAGE"
    AMOUNT = "AMOUNT"


class ServiceCreate(BaseModel):
    title: str
    description: Optional[str] = None
    photo_url: Optional[str] = None

    tech_stack: List[str]
    offerings: List[str]

    base_price: float
    discount_type: Optional[DiscountType] = None
    discount_value: Optional[float] = None


class ServiceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    photo_url: Optional[str] = None

    tech_stack: Optional[List[str]] = None
    offerings: Optional[List[str]] = None

    base_price: Optional[float] = None
    discount_type: Optional[DiscountType] = None
    discount_value: Optional[float] = None


class ServiceResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    photo_url: Optional[str]

    tech_stack: List[str]
    offerings: List[str]

    base_price: float
    effective_price: float
