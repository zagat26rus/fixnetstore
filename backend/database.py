from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional
import os
import logging

logger = logging.getLogger(__name__)

class Database:
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None

db_instance = Database()

async def connect_to_mongo():
    """Create database connection."""
    try:
        mongo_url = os.environ['MONGO_URL']
        db_name = os.environ.get('DB_NAME', 'fixnet')
        
        db_instance.client = AsyncIOMotorClient(mongo_url)
        db_instance.db = db_instance.client[db_name]
        
        # Test the connection
        await db_instance.client.admin.command('ismaster')
        logger.info(f"Connected to MongoDB database: {db_name}")
        
        # Create indexes for better performance
        await create_indexes()
        
    except Exception as e:
        logger.error(f"Could not connect to MongoDB: {e}")
        raise

async def close_mongo_connection():
    """Close database connection."""
    if db_instance.client:
        db_instance.client.close()
        logger.info("Disconnected from MongoDB")

async def get_database() -> AsyncIOMotorDatabase:
    """Get database instance."""
    if db_instance.db is None:
        await connect_to_mongo()
    return db_instance.db

async def create_indexes():
    """Create database indexes for better performance."""
    try:
        if db_instance.db:
            # Repair requests indexes
            await db_instance.db.repair_requests.create_index("ticket_id", unique=True)
            await db_instance.db.repair_requests.create_index("customerEmail")
            await db_instance.db.repair_requests.create_index("customerPhone")
            await db_instance.db.repair_requests.create_index("status")
            await db_instance.db.repair_requests.create_index("createdAt")
            await db_instance.db.repair_requests.create_index([
                ("customerName", "text"),
                ("customerEmail", "text"),
                ("deviceBrand", "text"),
                ("deviceModel", "text"),
                ("specificIssue", "text")
            ])
            
            # Admin users indexes
            await db_instance.db.admin_users.create_index("email", unique=True)
            
            # Contact messages indexes
            await db_instance.db.contact_messages.create_index("email")
            await db_instance.db.contact_messages.create_index("created_at")
            
            logger.info("Database indexes created successfully")
    except Exception as e:
        logger.warning(f"Could not create indexes: {e}")