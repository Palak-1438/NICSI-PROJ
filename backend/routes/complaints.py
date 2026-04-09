from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
from models.user import User, UserRole
from models.complaint import Complaint, ComplaintCreate, ComplaintUpdate
from routes.auth import get_current_active_user, get_database
from services.database import DatabaseService
from services.ai_service import classify_complaint
from auth.auth import check_role_permission

router = APIRouter()

@router.post("/complaints", response_model=Complaint)
async def create_complaint(
    complaint: ComplaintCreate,
    current_user: User = Depends(get_current_active_user),
    db: DatabaseService = Depends(get_database)
):
    check_role_permission(current_user, [UserRole.CITIZEN])

    # Classify complaint using AI service
    ai_result = classify_complaint(f"{complaint.title} {complaint.description}")

    created_complaint = await db.create_complaint(
        complaint,
        current_user.id,
        ai_result.category.value,
        ai_result.priority.value
    )
    return created_complaint

@router.get("/complaints/me", response_model=List[Complaint])
async def get_my_complaints(
    current_user: User = Depends(get_current_active_user),
    db: DatabaseService = Depends(get_database)
):
    check_role_permission(current_user, [UserRole.CITIZEN])
    return await db.get_complaints_by_citizen(current_user.id)

@router.get("/complaints/assigned", response_model=List[Complaint])
async def get_assigned_complaints(
    current_user: User = Depends(get_current_active_user),
    db: DatabaseService = Depends(get_database)
):
    check_role_permission(current_user, [UserRole.OFFICER])
    return await db.get_complaints_by_officer(current_user.id)

@router.get("/complaints", response_model=List[Complaint])
async def get_all_complaints(
    current_user: User = Depends(get_current_active_user),
    db: DatabaseService = Depends(get_database)
):
    check_role_permission(current_user, [UserRole.ADMIN])
    return await db.get_all_complaints()

@router.put("/complaints/{complaint_id}/status", response_model=Complaint)
async def update_complaint_status(
    complaint_id: str,
    status_update: ComplaintUpdate,
    current_user: User = Depends(get_current_active_user),
    db: DatabaseService = Depends(get_database)
):
    check_role_permission(current_user, [UserRole.OFFICER])

    # Verify the complaint is assigned to this officer
    complaint = await db.get_complaint_by_id(complaint_id)
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    if complaint.assigned_officer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this complaint"
        )

    # Only allow status updates
    if status_update.assigned_officer_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change assignment through status update"
        )

    updated_complaint = await db.update_complaint(complaint_id, status_update)
    if not updated_complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return updated_complaint

@router.put("/complaints/{complaint_id}/assign", response_model=Complaint)
async def assign_complaint(
    complaint_id: str,
    assignment: ComplaintUpdate,
    current_user: User = Depends(get_current_active_user),
    db: DatabaseService = Depends(get_database)
):
    check_role_permission(current_user, [UserRole.ADMIN])

    if not assignment.assigned_officer_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Officer ID is required for assignment"
        )

    # Verify the officer exists
    officer = await db.get_user_by_id(assignment.assigned_officer_id)
    if not officer or officer.role != UserRole.OFFICER:
        raise HTTPException(status_code=404, detail="Officer not found")

    updated_complaint = await db.update_complaint(complaint_id, assignment)
    if not updated_complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return updated_complaint