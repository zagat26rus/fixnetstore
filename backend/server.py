from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Import our modules
from .database import connect_to_mongo, close_mongo_connection
from .auth import create_default_admin, get_database
from .routes import repair_requests, auth, contact

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting FixNet Backend...")
    try:
        await connect_to_mongo()
        
        # Create default admin user
        db = await get_database()
        await create_default_admin(db)
        
        logger.info("FixNet Backend started successfully!")
    except Exception as e:
        logger.error(f"Failed to start backend: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down FixNet Backend...")
    await close_mongo_connection()

# Create the main app
app = FastAPI(
    title="FixNet API",
    description="Backend API for FixNet smartphone repair service",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(repair_requests.router)
app.include_router(auth.router)
app.include_router(contact.router)

# Root endpoint
@app.get("/api/")
async def root():
    return {
        "message": "Welcome to FixNet API",
        "version": "1.0.0",
        "status": "running"
    }

# Health check endpoint
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "FixNet Backend"}
