#!/usr/bin/env python3
"""
Seed script to populate the database with sample data for testing.
Run this after starting the backend server.
"""

import asyncio
import motor.motor_asyncio
from datetime import datetime
from auth.auth import get_password_hash

async def seed_database():
    # Connect to MongoDB
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.complaint_system

    # Clear existing data
    await db.users.delete_many({})
    await db.complaints.delete_many({}

    # Create sample users
    users = [
        {
            "email": "citizen@example.com",
            "hashed_password": get_password_hash("password123"),
            "full_name": "John Citizen",
            "role": "citizen",
            "created_at": datetime.utcnow()
        },
        {
            "email": "officer@example.com",
            "hashed_password": get_password_hash("password123"),
            "full_name": "Jane Officer",
            "role": "officer",
            "created_at": datetime.utcnow()
        },
        {
            "email": "admin@example.com",
            "hashed_password": get_password_hash("password123"),
            "full_name": "Bob Admin",
            "role": "admin",
            "created_at": datetime.utcnow()
        }
    ]

    # Insert users
    user_results = await db.users.insert_many(users)
    user_ids = user_results.inserted_ids

    # Create sample complaints
    complaints = [
        {
            "title": "Pothole on Main Street",
            "description": "There's a large pothole on Main Street near the intersection with Oak Avenue. It's causing damage to vehicles and is a safety hazard.",
            "category": "road",
            "priority": "high",
            "status": "pending",
            "citizen_id": str(user_ids[0]),  # John Citizen
            "location": "Main Street and Oak Avenue",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "title": "Street Light Not Working",
            "description": "The street light at the corner of Elm Street and Maple Drive has been out for three days. It's very dark at night and unsafe.",
            "category": "electricity",
            "priority": "medium",
            "status": "in_progress",
            "citizen_id": str(user_ids[0]),  # John Citizen
            "assigned_officer_id": str(user_ids[1]),  # Jane Officer
            "location": "Elm Street and Maple Drive",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "title": "Garbage Collection Missed",
            "description": "The garbage was not collected from our neighborhood this week. There are overflowing bins and it's creating an unpleasant smell.",
            "category": "sanitation",
            "priority": "medium",
            "status": "resolved",
            "citizen_id": str(user_ids[0]),  # John Citizen
            "assigned_officer_id": str(user_ids[1]),  # Jane Officer
            "location": "Oakwood Neighborhood",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "title": "Water Leak in Park",
            "description": "There's a water leak from the public fountain in Central Park. Water is wasting and the area is getting muddy.",
            "category": "water",
            "priority": "low",
            "status": "pending",
            "citizen_id": str(user_ids[0]),  # John Citizen
            "location": "Central Park Fountain",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]

    # Insert complaints
    await db.complaints.insert_many(complaints)

    print("Database seeded successfully!")
    print("\nSample users created:")
    print("- Citizen: citizen@example.com / password123")
    print("- Officer: officer@example.com / password123")
    print("- Admin: admin@example.com / password123")

    # Close connection
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_database())