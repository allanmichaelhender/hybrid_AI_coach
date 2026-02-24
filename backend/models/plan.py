import uuid
from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB 
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base_class import Base

class UserPlan(Base):
    __tablename__ = "user_plans"

    # Creating the id attribute, default creates a new uuid if needed
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # user_id attribute, set a a foreignkey from the user model
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("users.id", ondelete="CASCADE"), 
        index=True, 
        nullable=False
    )
    
    plan_name: Mapped[str] = mapped_column(String, nullable=True)
    user_goal: Mapped[str] = mapped_column(String, nullable=False)
    
    calendar_data: Mapped[list[dict]] = mapped_column(JSONB, nullable=False)
    
    coach_reasoning: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # Allows us to access the user object associated with a user plan, e.g. user_plan.user will be the user object
    user = relationship("User", back_populates="plans")

## Mapped tells python that we are mapping the folloing datatype onto a column of the same type
