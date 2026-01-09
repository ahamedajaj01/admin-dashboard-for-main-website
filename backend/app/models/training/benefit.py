# placeholder
import uuid
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship  # needed for ORM navigation
from app.db.base import Base

class TrainingBenefit(Base):
    """
    Represents a single benefit of a training.
    Docs say 'array of strings', but DB stores them as rows
    so they can be edited, ordered, and searched.
    """

    __tablename__ = "training_benefits"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # If training is deleted, benefits are deleted automatically
    # Links benefit to its training
    training_id = Column(
        UUID(as_uuid=True),
        ForeignKey("trainings.id", ondelete="CASCADE"),
        nullable=False
    )

    # Actual benefit text shown in UI
    text = Column(String, nullable=False)

    # Used to control display order in UI
    order = Column(Integer)

     # ---------- ORM RELATIONSHIP ----------
    # allows: benefit.training
    # required for training.benefits to work
    training = relationship(
        "Training",
        back_populates="benefits",
    )
