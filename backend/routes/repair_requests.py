from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from datetime import datetime, timedelta
import logging
from motor.motor_asyncio import AsyncIOMotorDatabase

from ..models import (
    RepairRequestCreate, RepairRequest, RepairRequestUpdate, 
    RepairRequestResponse, RepairRequestListResponse, StatusUpdateRequest,
    RepairStatus, PriorityLevel
)
from ..database import get_database
from ..auth import get_current_admin
from ..telegram_bot import telegram_bot

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/repair-requests", tags=["Repair Requests"])

@router.post("/", response_model=RepairRequestResponse)
async def create_repair_request(
    request_data: RepairRequestCreate,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Create a new repair request."""
    try:
        # Set priority based on urgency
        priority = PriorityLevel.HIGH if request_data.urgency == "urgent" else PriorityLevel.MEDIUM
        
        # Calculate estimated completion
        days_to_add = 1 if request_data.urgency == "urgent" else 3
        estimated_completion = datetime.utcnow() + timedelta(days=days_to_add)
        
        # Create repair request
        repair_request = RepairRequest(
            **request_data.dict(),
            priority=priority,
            estimatedCompletion=estimated_completion
        )
        
        # Insert into database
        result = await db.repair_requests.insert_one(repair_request.dict())
        
        if result.inserted_id:
            # Send Telegram notification
            try:
                await telegram_bot.send_new_ticket_notification(repair_request.dict())
            except Exception as e:
                logger.warning(f"Failed to send Telegram notification: {e}")
            
            return RepairRequestResponse(
                success=True,
                message="Repair request submitted successfully!",
                ticket_id=repair_request.ticket_id,
                data=repair_request
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to create repair request")
            
    except Exception as e:
        logger.error(f"Error creating repair request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=RepairRequestListResponse)
async def get_repair_requests(
    status: Optional[str] = Query(None, description="Filter by status"),
    search: Optional[str] = Query(None, description="Search by customer name, email, phone, or ticket ID"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=100, description="Items per page"),
    admin_email: str = Depends(get_current_admin),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get all repair requests with optional filtering."""
    try:
        # Build query
        query = {}
        
        if status and status != "all":
            query["status"] = status
        
        if search:
            # Search across multiple fields
            query["$or"] = [
                {"customerName": {"$regex": search, "$options": "i"}},
                {"customerEmail": {"$regex": search, "$options": "i"}},
                {"customerPhone": {"$regex": search, "$options": "i"}},
                {"ticket_id": {"$regex": search, "$options": "i"}},
                {"deviceBrand": {"$regex": search, "$options": "i"}},
                {"deviceModel": {"$regex": search, "$options": "i"}},
                {"specificIssue": {"$regex": search, "$options": "i"}}
            ]
        
        # Get total count
        total = await db.repair_requests.count_documents(query)
        
        # Get paginated results
        skip = (page - 1) * limit
        cursor = db.repair_requests.find(query).sort("createdAt", -1).skip(skip).limit(limit)
        requests_data = await cursor.to_list(length=limit)
        
        # Convert to RepairRequest objects
        requests = [RepairRequest(**req) for req in requests_data]
        
        return RepairRequestListResponse(
            success=True,
            total=total,
            requests=requests
        )
        
    except Exception as e:
        logger.error(f"Error fetching repair requests: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{ticket_id}", response_model=RepairRequest)
async def get_repair_request(
    ticket_id: str,
    admin_email: str = Depends(get_current_admin),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get a specific repair request by ticket ID."""
    try:
        request_data = await db.repair_requests.find_one({"ticket_id": ticket_id})
        
        if not request_data:
            raise HTTPException(status_code=404, detail="Repair request not found")
        
        return RepairRequest(**request_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching repair request {ticket_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{ticket_id}/status")
async def update_repair_status(
    ticket_id: str,
    status_update: StatusUpdateRequest,
    admin_email: str = Depends(get_current_admin),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Update the status of a repair request."""
    try:
        # Get current request
        current_request = await db.repair_requests.find_one({"ticket_id": ticket_id})
        if not current_request:
            raise HTTPException(status_code=404, detail="Repair request not found")
        
        old_status = current_request.get("status")
        
        # Prepare update data
        update_data = {
            "status": status_update.status,
            "updatedAt": datetime.utcnow()
        }
        
        if status_update.notes:
            update_data["notes"] = status_update.notes
        
        if status_update.status == RepairStatus.COMPLETED:
            update_data["completedAt"] = datetime.utcnow()
        
        # Update in database
        result = await db.repair_requests.update_one(
            {"ticket_id": ticket_id},
            {"$set": update_data}
        )
        
        if result.modified_count > 0:
            # Send Telegram notification for status change
            try:
                await telegram_bot.send_status_update_notification(
                    ticket_id=ticket_id,
                    old_status=old_status,
                    new_status=status_update.status,
                    customer_name=current_request.get("customerName", "Unknown")
                )
            except Exception as e:
                logger.warning(f"Failed to send Telegram notification: {e}")
            
            return {"success": True, "message": "Status updated successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to update status")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating repair request {ticket_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{ticket_id}")
async def update_repair_request(
    ticket_id: str,
    update_data: RepairRequestUpdate,
    admin_email: str = Depends(get_current_admin),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Update a repair request."""
    try:
        # Get current request
        current_request = await db.repair_requests.find_one({"ticket_id": ticket_id})
        if not current_request:
            raise HTTPException(status_code=404, detail="Repair request not found")
        
        # Prepare update data
        update_dict = {k: v for k, v in update_data.dict().items() if v is not None}
        update_dict["updatedAt"] = datetime.utcnow()
        
        if update_data.status == RepairStatus.COMPLETED:
            update_dict["completedAt"] = datetime.utcnow()
        
        # Update in database
        result = await db.repair_requests.update_one(
            {"ticket_id": ticket_id},
            {"$set": update_dict}
        )
        
        if result.modified_count > 0:
            return {"success": True, "message": "Repair request updated successfully"}
        else:
            return {"success": False, "message": "No changes made"}
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating repair request {ticket_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{ticket_id}")
async def delete_repair_request(
    ticket_id: str,
    admin_email: str = Depends(get_current_admin),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Delete a repair request."""
    try:
        result = await db.repair_requests.delete_one({"ticket_id": ticket_id})
        
        if result.deleted_count > 0:
            return {"success": True, "message": "Repair request deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Repair request not found")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting repair request {ticket_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/dashboard")
async def get_dashboard_stats(
    admin_email: str = Depends(get_current_admin),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get dashboard statistics."""
    try:
        # Get counts by status
        pipeline = [
            {"$group": {"_id": "$status", "count": {"$sum": 1}}}
        ]
        
        status_counts = {}
        async for result in db.repair_requests.aggregate(pipeline):
            status_counts[result["_id"]] = result["count"]
        
        # Get today's requests
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_count = await db.repair_requests.count_documents({
            "createdAt": {"$gte": today_start}
        })
        
        # Get this week's requests
        week_start = today_start - timedelta(days=7)
        week_count = await db.repair_requests.count_documents({
            "createdAt": {"$gte": week_start}
        })
        
        # Calculate total revenue (from completed requests)
        revenue_pipeline = [
            {"$match": {"status": "Completed", "actualCost": {"$exists": True}}},
            {"$group": {"_id": None, "total": {"$sum": "$actualCost"}}}
        ]
        
        total_revenue = 0
        async for result in db.repair_requests.aggregate(revenue_pipeline):
            total_revenue = result["total"]
        
        return {
            "total_requests": sum(status_counts.values()),
            "status_breakdown": status_counts,
            "today_requests": today_count,
            "week_requests": week_count,
            "total_revenue": total_revenue,
            "active_requests": status_counts.get("New", 0) + status_counts.get("In Progress", 0) + status_counts.get("Diagnosed", 0)
        }
        
    except Exception as e:
        logger.error(f"Error fetching dashboard stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))