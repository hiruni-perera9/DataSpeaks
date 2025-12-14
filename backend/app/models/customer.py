# Customer data models using SQLAlchemy ORM

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Enum
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from datetime import datetime
import enum

Base = declarative_base()

class PlanType(str, enum.Enum):
    # Enum for subscription plans

    STARTER = "starter"
    GROWTH = "growth"
    ENTERPRISE = "enterprise"

class Customer(Base):
    # Customer table model
    
    __tablename__ = "customers"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Company information
    company_name = Column(String, nullable=False, index=True)
    industry = Column(String, nullable=True)
    employee_count = Column(Integer, nullable=True)

    # Subscription details
    plan = Column(Enum(PlanType, name="plan_type_enum"), nullable=False, default=PlanType.STARTER)
    mrr = Column(Float, nullable=False, default=0.0) 

    # Status
    is_active = Column(Boolean, default=True, index=True)

    # Timestamps
    signup_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_activity = Column(DateTime, nullable=True)
    churned_date = Column(DateTime, nullable=True) #Cancelled Date

    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Customer(id={self.id}, company={self.company_name}, plan={self.plan})>"
    
    @property
    def is_churned(self) -> bool:
        # Helper property to check if the customer has churned
        return not self.is_active and self.churned_date is not None
    
    @property
    def lifetime_months(self) -> int:
        # How many months the customer has been active
        end_date = self.churned_date if self.is_churned else datetime.utcnow()
        delta = end_date - self.signup_date
        return max(1, delta.days // 30)
    
    @property
    def lifetime_value(self) -> float:
        # Total revenue per customer
        return self.mrr * self.lifetime_months
        


