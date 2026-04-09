from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class ComplaintStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"

class ComplaintPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class ComplaintCategory(str, Enum):
    ROAD = "road"
    WATER = "water"
    ELECTRICITY = "electricity"
    SANITATION = "sanitation"
    OTHER = "other"

class Complaint(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    category: Optional[ComplaintCategory] = None
    priority: Optional[ComplaintPriority] = None
    status: ComplaintStatus = ComplaintStatus.PENDING
    citizen_id: str
    assigned_officer_id: Optional[str] = None
    location: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class ComplaintCreate(BaseModel):
    title: str
    description: str
    location: Optional[str] = None

class ComplaintUpdate(BaseModel):
    status: Optional[ComplaintStatus] = None
    assigned_officer_id: Optional[str] = None

class ComplaintAIResult(BaseModel):
    category: ComplaintCategory
    priority: ComplaintPriority