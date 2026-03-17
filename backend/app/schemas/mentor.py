from pydantic import BaseModel, field_serializer
from typing import Optional
from uuid import UUID
from app.services.storage_service import resolve_image_url


class MentorBase(BaseModel):
    name: str
    photo_url: Optional[str] = None
    specialization: Optional[str] = None


class MentorCreate(MentorBase):
     name: str
     photo_url: Optional[str] = None


class MentorUpdate(MentorBase):
     name: Optional[str] = None
     photo_url: Optional[str] = None

class MentorResponse(MentorBase):
    id: UUID

    @field_serializer('photo_url')
    def resolve_photo(self, value):
        return resolve_image_url(value) if value else ""

    class Config:
        from_attributes = True
