from typing import List, Optional
from pydantic import BaseModel
from enum import Enum


class OpportunityType(str, Enum):
    JOB = "JOB"
    INTERNSHIP = "INTERNSHIP"


class OpportunityCreate(BaseModel):
    title: str
    description: Optional[str] = None
    duration: Optional[str] = None
    compensation: Optional[str] = None
    location: Optional[str] = None

    requirements: List[str]
    type: OpportunityType


class OpportunityUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[str] = None
    compensation: Optional[str] = None
    location: Optional[str] = None

    requirements: Optional[List[str]] = None
    type: Optional[OpportunityType] = None


class OpportunityResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    duration: Optional[str]
    compensation: Optional[str]
    location: Optional[str]

    requirements: List[str]
    type: OpportunityType
