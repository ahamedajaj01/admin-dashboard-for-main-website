# placeholder
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
from sqlalchemy.orm import relationship  # needed for ORM navigation


class TrainingMentor(Base):
    """
    Many-to-many relationship between trainings and mentors.
    """

    __tablename__ = "training_mentors"

    training_id = Column(
        UUID(as_uuid=True),
        ForeignKey("trainings.id", ondelete="CASCADE"),
        primary_key=True
    )

    mentor_id = Column(
        UUID(as_uuid=True),
        ForeignKey("mentors.id", ondelete="CASCADE"),
        primary_key=True
    )

    order = Column(Integer)
    # Controls mentor display order per training

     # ---------- ORM RELATIONSHIPS ----------
    # allows: training_mentor.training
    training = relationship(
        "Training",
        back_populates="training_mentors",
    )

    # allows: training_mentor.mentor
    mentor = relationship("Mentor")
