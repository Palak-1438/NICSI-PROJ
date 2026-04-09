from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from datetime import datetime
from typing import List, Optional
from models.user import User, UserInDB, UserCreate
from models.complaint import Complaint, ComplaintCreate, ComplaintUpdate, ComplaintStatus
from auth.auth import get_password_hash

class DatabaseService:
    def __init__(self, mongodb_url: str = "mongodb://localhost:27017"):
        self.client: AsyncIOMotorClient = None
        self.db: AsyncIOMotorDatabase = None
        self.mongodb_url = mongodb_url

    async def connect(self):
        self.client = AsyncIOMotorClient(self.mongodb_url)
        self.db = self.client.complaint_system
        # Create indexes
        await self.db.users.create_index("email", unique=True)
        await self.db.complaints.create_index("citizen_id")
        await self.db.complaints.create_index("assigned_officer_id")
        await self.db.complaints.create_index("status")

    async def disconnect(self):
        if self.client:
            self.client.close()

    # User operations
    async def create_user(self, user: UserCreate) -> User:
        user_dict = user.dict()
        user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
        user_dict["created_at"] = datetime.utcnow()

        result = await self.db.users.insert_one(user_dict)
        user_dict["id"] = str(result.inserted_id)
        return User(**user_dict)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        user_dict = await self.db.users.find_one({"email": email})
        if user_dict:
            return User(**user_dict)
        return None

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        from bson import ObjectId
        user_dict = await self.db.users.find_one({"_id": ObjectId(user_id)})
        if user_dict:
            user_dict["id"] = str(user_dict["_id"])
            return User(**user_dict)
        return None

    async def get_officers(self) -> List[User]:
        officers = []
        async for user_dict in self.db.users.find({"role": "officer"}):
            user_dict["id"] = str(user_dict["_id"])
            officers.append(User(**user_dict))
        return officers

    # Complaint operations
    async def create_complaint(self, complaint: ComplaintCreate, citizen_id: str,
                              category: str, priority: str) -> Complaint:
        complaint_dict = complaint.dict()
        complaint_dict["citizen_id"] = citizen_id
        complaint_dict["category"] = category
        complaint_dict["priority"] = priority
        complaint_dict["created_at"] = datetime.utcnow()
        complaint_dict["updated_at"] = datetime.utcnow()

        result = await self.db.complaints.insert_one(complaint_dict)
        complaint_dict["id"] = str(result.inserted_id)
        return Complaint(**complaint_dict)

    async def get_complaints_by_citizen(self, citizen_id: str) -> List[Complaint]:
        complaints = []
        async for complaint_dict in self.db.complaints.find({"citizen_id": citizen_id}):
            complaint_dict["id"] = str(complaint_dict["_id"])
            complaints.append(Complaint(**complaint_dict))
        return complaints

    async def get_complaints_by_officer(self, officer_id: str) -> List[Complaint]:
        complaints = []
        async for complaint_dict in self.db.complaints.find({"assigned_officer_id": officer_id}):
            complaint_dict["id"] = str(complaint_dict["_id"])
            complaints.append(Complaint(**complaint_dict))
        return complaints

    async def get_all_complaints(self) -> List[Complaint]:
        complaints = []
        async for complaint_dict in self.db.complaints.find({}):
            complaint_dict["id"] = str(complaint_dict["_id"])
            complaints.append(Complaint(**complaint_dict))
        return complaints

    async def get_complaint_by_id(self, complaint_id: str) -> Optional[Complaint]:
        from bson import ObjectId
        complaint_dict = await self.db.complaints.find_one({"_id": ObjectId(complaint_id)})
        if complaint_dict:
            complaint_dict["id"] = str(complaint_dict["_id"])
            return Complaint(**complaint_dict)
        return None

    async def update_complaint(self, complaint_id: str, update_data: ComplaintUpdate) -> Optional[Complaint]:
        from bson import ObjectId
        update_dict = update_data.dict(exclude_unset=True)
        update_dict["updated_at"] = datetime.utcnow()

        result = await self.db.complaints.update_one(
            {"_id": ObjectId(complaint_id)},
            {"$set": update_dict}
        )

        if result.modified_count > 0:
            return await self.get_complaint_by_id(complaint_id)
        return None