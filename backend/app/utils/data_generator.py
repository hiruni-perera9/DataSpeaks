# Fake Data Generator

from faker import Faker
from datetime import datetime, timedelta
import random
from app.models.customer import Customer, PlanType
from sqlalchemy.orm import Session
from sqlalchemy import func

fake = Faker()


class CustomerDataGenerator:
    """
    Generates realistic customer data

    - Growth trajectory (customers increase over time)
    - Churn patterns 
    - Revenue distribution (enterprise, growth, starter)
    - Activity patterns (recent activity)
    """
    
    INDUSTRIES = [
        "Technology", "Healthcare", "Finance", "Education",
        "E-commerce", "Manufacturing", "Real Estate", "Legal",
        "Marketing", "Consulting", "Retail", "Media"
    ]
    
    # MRR ranges by plan type (in USD)
    MRR_RANGES = {
        PlanType.STARTER: (49, 199),
        PlanType.GROWTH: (199, 999),
        PlanType.ENTERPRISE: (999, 5000)
    }
    
    # Plan distribution (weights for random choice)
    PLAN_WEIGHTS = {
        PlanType.STARTER: 0.5,      # 50% starter
        PlanType.GROWTH: 0.35,       # 35% growth
        PlanType.ENTERPRISE: 0.15    # 15% enterprise
    }
    
    def __init__(self, start_date: datetime = None):
        # Initialize Generator
        self.start_date = start_date or (datetime.utcnow() - timedelta(days=730))
    
    def generate_customer(self, signup_date: datetime = None) -> dict:
        # Generate single realistic cusotmer

        # Determine plan (using weighted random choice)
        plan = random.choices(
            list(self.PLAN_WEIGHTS.keys()),
            weights=list(self.PLAN_WEIGHTS.values())
        )[0]
        
        # Generate MRR based on plan
        mrr_min, mrr_max = self.MRR_RANGES[plan]
        mrr = round(random.uniform(mrr_min, mrr_max), 2)
        
        # Employee count correlates with plan
        if plan == PlanType.STARTER:
            employee_count = random.randint(1, 20)
        elif plan == PlanType.GROWTH:
            employee_count = random.randint(20, 200)
        else:  # ENTERPRISE
            employee_count = random.randint(200, 10000)
        
        # Signup date 
        if not signup_date:
            days_since_start = (datetime.utcnow() - self.start_date).days
            random_days = random.randint(0, days_since_start)
            signup_date = self.start_date + timedelta(days=random_days)
        
        # Last activity
        days_since_signup = (datetime.utcnow() - signup_date).days
        if days_since_signup > 0:
            # 80% chance of activity in last 30 days for active customers
            if random.random() < 0.8:
                activity_days_ago = random.randint(0, 30)
            else:
                activity_days_ago = random.randint(0, days_since_signup)
            
            last_activity = datetime.utcnow() - timedelta(days=activity_days_ago)
        else:
            last_activity = signup_date
        
        return {
            "company_name": fake.company(),
            "industry": random.choice(self.INDUSTRIES),
            "employee_count": employee_count,
            "plan": plan,
            "mrr": mrr,
            "signup_date": signup_date,
            "last_activity": last_activity,
            "is_active": True  
        }
    
    def add_churn(self, customer_data: dict, churn_probability: float = 0.15) -> dict:
        # Randonly churn some customers for realistic data
        
        # Adjust churn probability based on plan
        if customer_data["plan"] == PlanType.STARTER:
            churn_probability *= 1.5
        elif customer_data["plan"] == PlanType.ENTERPRISE:
            churn_probability *= 0.5
        
        # Adjust based on engagement
        days_since_activity = (datetime.utcnow() - customer_data["last_activity"]).days
        if days_since_activity > 90:
            churn_probability *= 2
        
        # Apply churn
        if random.random() < churn_probability:
            # Churned sometime between signup and now
            signup = customer_data["signup_date"]
            days_active = random.randint(30, (datetime.utcnow() - signup).days)
            churned_date = signup + timedelta(days=days_active)
            
            customer_data["is_active"] = False
            customer_data["churned_date"] = churned_date
        
        return customer_data
    
    def generate_customers(self, count: int = 150) -> list[dict]:
        # Generate realistic customers
        customers = []
        
        # Calculate days between start and now
        total_days = (datetime.utcnow() - self.start_date).days
        
        # Generate signups with growth curve
        for i in range(count):
            # Progress through time (0 to 1)
            progress = i / count
            
            # Apply S-curve for realistic growth
            # Early days: slow growth
            # Middle: rapid growth
            # Recent: steady state
            days_offset = int(total_days * (progress ** 1.5))
            signup_date = self.start_date + timedelta(days=days_offset)
            
            customer = self.generate_customer(signup_date)
            customer = self.add_churn(customer)
            customers.append(customer)
        
        return customers


def seed_database(db: Session, count: int = 150):
    # Populate database with customers
    
    print(f"Generating {count} customers...")
    
    generator = CustomerDataGenerator()
    customers_data = generator.generate_customers(count)
    
    print("Inserting into database...")
    for customer_data in customers_data:
        customer = Customer(**customer_data)
        db.add(customer)
    
    db.commit()
    print(f"✅ Successfully created {count} customers!")
    
    # Print some stats
    active_count = db.query(Customer).filter(Customer.is_active == True).count()
    churned_count = count - active_count
    total_mrr = db.query(func.sum(Customer.mrr)).filter(Customer.is_active == True).scalar()
    
    print(f"\nStats:")
    print(f"  Active: {active_count}")
    print(f"  Churned: {churned_count}")
    print(f"  Total MRR: ${total_mrr:,.2f}")