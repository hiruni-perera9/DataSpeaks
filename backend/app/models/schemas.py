# Pydantic schemas fr API request validation

from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
from app.models.customer import PlanType

class CustomerBase(BaseModel):
    # Base schema with common fields
    company_name: str = Field(..., min_length=1, max_length=200)
    industry: Optional[str] = None
    employee_count: Optional[int] = Field(None, ge=1)
    plan: PlanType
    mrr: float = Field(..., ge=0)
    
    @validator('company_name')
    def clean_company_name(cls, v):
        """Sanitize company name"""
        return v.strip()
    
class CustomerCreate(CustomerBase):
    # Create new customer
    signup_date: Optional[datetime] = None
    last_activity: Optional[datetime] = None

class CustomerUpdate(BaseModel):
    # Update existing customer
    company_name: Optional[str] = None
    industry: Optional[str] = None
    employee_count: Optional[int] = None
    plan: Optional[PlanType] = None
    mrr: Optional[float] = None
    is_active: Optional[bool] = None
    last_activity: Optional[datetime] = None

class CustomerResponse(CustomerBase):
    # Return customer data
    id: int
    is_active: bool
    signup_date: datetime
    last_activity: Optional[datetime]
    churned_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    # Calculated fields
    lifetime_months: int
    lifetime_value: float

    class Config:
        # Tell Pydantic to work with SQL Alchemy models
        from_attributes = True

class CustomerListResponse(BaseModel):
    # Paginated customer list
    total: int
    customers: list[CustomerResponse]
    page: int
    page_size: int
