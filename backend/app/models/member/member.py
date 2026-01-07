import uuid
from datetime import datetime
from sqlalchemy import Column, String, Date, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.db.base import Base
from .enums import MemberRole

class Member(Base):
    """
    Represents both Team members and Interns.
    Docs say they share the same structure,
    so we store them in one table with a role.
    """

    __tablename__ = "members"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # UUID for safety and scalability

    photo_url = Column(String)
    # Profile image

    name = Column(String, nullable=False)
    # Required: every person has a name

    position = Column(String)
    # Job title or intern role

    start_date = Column(Date)
    end_date = Column(Date, nullable=True)
    # End date optional for current members

    social_media = Column(JSONB)
    # Stored as JSON because platform → URL mapping is flexible

    contact_email = Column(String)
    # Official company email

    personal_email = Column(String)
    # Personal email

    contact_number = Column(String)
    # Stored as string to support country codes

    is_visible = Column(Boolean, default=True)
    # Controls visibility on public website

    role = Column(Enum(MemberRole), nullable=False)
    # Differentiates TEAM vs INTERN

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
