from typing import List, Optional
from pydantic import BaseModel, Field, field_serializer
from enum import Enum
from datetime import datetime
from uuid import UUID
from app.services.storage_service import resolve_image_url


class DiscountType(str, Enum):
    PERCENTAGE = "PERCENTAGE"
    AMOUNT = "AMOUNT"


class MentorInput(BaseModel):
    name: str
    photo_url: Optional[str]


class TrainingCreate(BaseModel):
    title: str
    description: Optional[str]
    photo_url: Optional[str]

    base_price: float
    enroll_from_price: Optional[float]
    discount_type: Optional[DiscountType]
    discount_value: Optional[float]

    benefits: List[str]
    mentor_ids: List[UUID] = Field(default_factory=list)


class TrainingUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    photo_url: Optional[str]

    base_price: Optional[float]
    enroll_from_price: Optional[float]
    discount_type: Optional[DiscountType]
    discount_value: Optional[float]

    benefits: Optional[List[str]]
    mentor_ids: Optional[List[UUID]]


class MentorResponse(BaseModel):
    name: str
    photo_url: Optional[str]

    @field_serializer('photo_url')
    def resolve_photo(self, value):
        return resolve_image_url(value) if value else ""


class TrainingResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    photo_url: Optional[str]

    base_price: float
    enroll_from_price: Optional[float]
    effective_price: float

    benefits: List[str]
    mentors: List[MentorResponse]
    created_at: datetime
    updated_at: Optional[datetime]

    @field_serializer('photo_url')
    def resolve_photo(self, value):
        return resolve_image_url(value) if value else ""

    @field_serializer('photo_url')
    def resolve_photo(self, value):
        return resolve_image_url(value) if value else ""
