# Customer CRUM Endpoints

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from app.database import get_db
from app.models.customer import Customer, PlanType
from app.models.schemas import(
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
    CustomerListResponse
)

router = APIRouter()

@router.get("/customers", response_model = CustomerListResponse)
async def get_customers(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Max records to return"),
    plan: Optional[PlanType] = Query(None, description="Filter by plan type"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: Session = Depends(get_db)
):
    # Get paginated list of customers with optional filters.
    
    # Build query
    query = db.query(Customer)
    
    # Apply filters
    if plan:
        query = query.filter(Customer.plan == plan)
    if is_active is not None:
        query = query.filter(Customer.is_active == is_active)
    
    # Get total count (before pagination)
    total = query.count()
    
    # Apply pagination
    customers = query.order_by(Customer.signup_date.desc()).offset(skip).limit(limit).all()
    
    # Calculate page number
    page = (skip // limit) + 1 if limit > 0 else 1
    
    return CustomerListResponse(
        total=total,
        customers=customers,
        page=page,
        page_size=limit
    )

@router.get("/customers/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    # Get customer by ID
    customer = db.query(Customer).filter(Customer.id == customer_id) .first()

    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found")
    
    return customer

@router.post("/customers", response_model = CustomerResponse, status_code=201)
async def create_customer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db)
):
    # Create a new customer

    # Create SQLAlchemy model from Pydantic schema
    customer = Customer(**customer_data.model_dump())

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer

@router.patch("/customers/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    db: Session = Depends(get_db)
):
    # Update existing customer (partial update)

    customer = db.query(Customer).filter(Customer.id == customer_id).first()

    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found")
    
    # Ipdate only provided fields
    update_data = customer_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(customer, field, value)

    db.commit()
    db.refresh(customer)

    return customer

@router.delete("/customers/{customer_id}", status_code=204)
async def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db)
): 
    # Delete Customer
    customer = db.query(Customer).filter(Customer.id == customer_id).first()

    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found")
    
    db.delete(customer)
    db.commit()

    return None

@router.get("/customer/stats/summary")
async def get_customer_summary(db: Session = Depends(get_db)):
    # Get high level customer statistics

    # Total customers
    total = db.query(Customer).count()
    active = db.query(Customer).filter(Customer.is_active == True).count()
    churned = total - active

    # MRR (Monthly Recurring Revenue) 
    total_mrr = db.query(func.sum(Customer.mrr)).filter(Customer.is_active == True).scalar() or 0

    # Average MRR per customer
    avg_mrr = total_mrr / active if active > 0 else 0

    # Plan distribution
    plan_distribution = {}

    for plan in PlanType:
        count = db.query(Customer).filter(Customer.plan == plan, Customer.is_active == True).count()
        plan_distribution[plan.value] = count

    return {
        "total_customers": total,
        "active_customers": active,
        "churned_customers": churned,
        "churn_rate": (churned / total * 100) if total > 0 else 0,
        "total_mrr": round(total_mrr, 2),
        "average_mrr": round(avg_mrr, 2),
        "plan_distribution": plan_distribution
    }