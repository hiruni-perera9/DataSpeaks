# Script to populate the database with demo data.

from app.database import SessionLocal, create_tables, engine
from app.utils.data_generator import seed_database
from app.models.customer import Base


def main():
    print("Creating database tables...")
    create_tables()
    
    print("\nSeeding database with customer data...")
    db = SessionLocal()
    
    try:
        # Check if already seeded
        from app.models.customer import Customer
        existing_count = db.query(Customer).count()
        
        if existing_count > 0:
            response = input(f"Database already has {existing_count} customers. Delete and reseed? (y/n): ")
            if response.lower() == 'y':
                print("Deleting existing data...")
                db.query(Customer).delete()
                db.commit()
            else:
                print("Cancelled.")
                return
        
        # Seed with 200 customers
        seed_database(db, count=200)
        
        print("\n✅ Database setup complete!")
        print("You can now run the API server with: uvicorn app.main:app --reload")
        
    finally:
        db.close()


if __name__ == "__main__":
    main()