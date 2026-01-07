from typing import List, Optional
from pydantic import BaseModel


class FeedbackCreate(BaseModel):
    client_name: str
    client_photo: Optional[str] = None
    feedback_description: str
    rating: int


class FeedbackResponse(BaseModel):
    client_name: str
    client_photo: Optional[str]
    feedback_description: str
    rating: int


class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None
    photo_url: Optional[str] = None

    tech_stack: List[str]
    project_link: Optional[str] = None

    feedbacks: Optional[List[FeedbackCreate]] = []


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    photo_url: Optional[str] = None

    tech_stack: Optional[List[str]] = None
    project_link: Optional[str] = None

    feedbacks: Optional[List[FeedbackCreate]] = None


class ProjectResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    photo_url: Optional[str]

    tech_stack: List[str]
    project_link: Optional[str]

    feedbacks: List[FeedbackResponse]
