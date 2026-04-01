from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field, field_serializer
from datetime import datetime
from app.services.storage_service import resolve_image_url


class FeedbackCreate(BaseModel):
    client_name: str
    client_photo: Optional[str] = None
    feedback_description: str
    rating: int = Field(..., ge=1, le=5)


class FeedbackResponse(BaseModel):
    id: UUID
    client_name: str
    client_photo: Optional[str]
    feedback_description: str
    rating: int

    @field_serializer('client_photo')
    def resolve_photo(self, value):
        return resolve_image_url(value) if value else ""



class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None
    photo_url: Optional[str] = None

    tech_ids: List[UUID]
    project_link: Optional[str] = None


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    photo_url: Optional[str] = None

    tech_ids: Optional[List[UUID]] = None
    project_link: Optional[str] = None


class ProjectResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    photo_url: Optional[str]

    techs: List[str]
    project_link: Optional[str]

    feedbacks: List[FeedbackResponse]
    created_at: datetime
    updated_at: Optional[datetime]

    @field_serializer('photo_url')
    def resolve_photo(self, value):
        return resolve_image_url(value) if value else ""  
    
