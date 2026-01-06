import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base

class ProjectFeedback(Base):
    """
    Represents feedback given by a client for a project.
    Stored separately for validation and moderation.
    """

    __tablename__ = "project_feedbacks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    project_id = Column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False
    )
    # Feedback belongs to a project

    client_name = Column(String, nullable=False)
    # Name of the client

    client_photo = Column(String)
    # Client image

    feedback_description = Column(String)
    # Actual feedback text

    rating = Column(Integer, nullable=False)
    # Rating between 1 and 5 (validated in logic)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
