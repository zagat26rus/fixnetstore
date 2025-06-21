from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging

from ..models import ContactMessage, ContactMessageCreate
from ..database import get_database
from ..auth import get_current_admin
from ..telegram_bot import telegram_bot

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/contact", tags=["Contact"])

@router.post("/", response_model=dict)
async def create_contact_message(
    message_data: ContactMessageCreate,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Create a new contact message."""
    try:
        # Create contact message
        contact_message = ContactMessage(**message_data.dict())
        
        # Insert into database
        result = await db.contact_messages.insert_one(contact_message.dict())
        
        if result.inserted_id:
            # Send Telegram notification
            try:
                await telegram_bot.send_contact_message_notification(contact_message.dict())
            except Exception as e:
                logger.warning(f"Failed to send Telegram notification: {e}")
            
            return {
                "success": True,
                "message": "Message sent successfully! We'll get back to you within 24 hours.",
                "id": contact_message.id
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to send message")
            
    except Exception as e:
        logger.error(f"Error creating contact message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[ContactMessage])
async def get_contact_messages(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=100, description="Items per page"),
    unread_only: bool = Query(False, description="Show only unread messages"),
    admin_email: str = Depends(get_current_admin),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get all contact messages (admin only)."""
    try:
        # Build query
        query = {}
        if unread_only:
            query["is_read"] = False
        
        # Get paginated results
        skip = (page - 1) * limit
        cursor = db.contact_messages.find(query).sort("created_at", -1).skip(skip).limit(limit)
        messages_data = await cursor.to_list(length=limit)
        
        # Convert to ContactMessage objects
        messages = [ContactMessage(**msg) for msg in messages_data]
        
        return messages
        
    except Exception as e:
        logger.error(f"Error fetching contact messages: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{message_id}/read")
async def mark_message_as_read(
    message_id: str,
    admin_email: str = Depends(get_current_admin),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Mark a contact message as read."""
    try:
        result = await db.contact_messages.update_one(
            {"id": message_id},
            {"$set": {"is_read": True}}
        )
        
        if result.modified_count > 0:
            return {"success": True, "message": "Message marked as read"}
        else:
            raise HTTPException(status_code=404, detail="Message not found")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error marking message as read: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{message_id}")
async def delete_contact_message(
    message_id: str,
    admin_email: str = Depends(get_current_admin),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Delete a contact message."""
    try:
        result = await db.contact_messages.delete_one({"id": message_id})
        
        if result.deleted_count > 0:
            return {"success": True, "message": "Message deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Message not found")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting contact message: {e}")
        raise HTTPException(status_code=500, detail=str(e))