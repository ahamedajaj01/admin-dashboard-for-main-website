import uuid
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base

class OpportunityRequirement(Base):
    """
    Represents a single requirement for a job or internship.
    Stored separately for easier editing and ordering.
    """

    __tablename__ = "opportunity_requirements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    opportunity_id = Column(
        UUID(as_uuid=True),
        ForeignKey("opportunities.id", ondelete="CASCADE"),
        nullable=False
    )
    # Automatically removed when opportunity is deleted

    text = Column(String, nullable=False)
    # Requirement text

    order = Column(Integer)
    # Display order
