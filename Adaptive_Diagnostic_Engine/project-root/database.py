import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

# Use Environment Variables for security
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client.adaptive_testing_db

async def seed_questions():
    """Run this once to populate your DB with GRE-style questions"""
    questions_collection = db.get_collection("questions")
    
    # Check if already seeded
    count = await questions_collection.count_documents({})
    if count > 0:
        return

    sample_data = [
        {"text": "Find x: 2x + 10 = 20", "options": ["5", "10", "15", "2"], "correct_answer": "5", "difficulty": 0.2, "topic": "Algebra", "tags": ["basic", "math"]},
        {"text": "If a triangle has sides 3 and 4, the hypotenuse is?", "options": ["5", "6", "7", "8"], "correct_answer": "5", "difficulty": 0.4, "topic": "Geometry", "tags": ["pythagoras"]},
        # Add 18 more varied difficulty questions here...
    ]
    await questions_collection.insert_many(sample_data)
    print("Database Seeded Successfully!")