import uuid
from datetime import datetime
from sqlalchemy import Column, String, Numeric, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.db.base import Base
from app.models.pricing.enums import DiscountType

class Service(Base):
    """
    Represents a service offered by the company.
    Similar to Training, but without mentors or benefits.
    """

    __tablename__ = "services"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # UUID used for security and scalability

    photo_url = Column(String)
    # Service image

    title = Column(String, nullable=False)
    # Required: service must have a name

    description = Column(String)
    # Detailed explanation of service

    tech_stack = Column(JSONB)
    # Stored as JSON because it is a simple list of strings

    offerings = Column(JSONB)
    # Same reason: simple list, no ordering logic needed now

    base_price = Column(Numeric(10, 2), nullable=False)
    # Main pricing value

    discount_type = Column(Enum(DiscountType))
    # Optional discount

    discount_value = Column(Numeric(10, 2))
    # Discount amount or percentage

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    @property
    def effective_price(self):
        """
        Calculated dynamically to avoid inconsistent data.
        """
        if not self.discount_type or not self.discount_value:
            return self.base_price

        if self.discount_type == DiscountType.PERCENTAGE:
            return self.base_price * (1 - self.discount_value / 100)

        return self.base_price - self.discount_value
