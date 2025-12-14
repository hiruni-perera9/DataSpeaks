# Main FastAPI application entry point

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import customers
import logging

# Configure logging
logging.basicConfig(
    level = settings.log_level,
    format = '%(asctime)s = %(name)s - %(levelname)s - %(message)s'
)

# Create FastAPI app
app = FastAPI(
    title = settings.app_name,
    description = "AI powered customer analytics dashboard API",
    version = "1.0.0",
    docs_url = "/docs",
    redoc_url = "/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000", "http://localhost:5173"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

# Include routers
app.include_router(customers.router, prefix="/api", tags=["customers"])

@app.get("/")
async def root():
    # Health check endpoint
    return { 
        "message": "Customer Insights Dashboard API",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    # Detailed health check for monitoring
    return {
        "status": "healthy",
        "database": "connected",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=settings.debug)