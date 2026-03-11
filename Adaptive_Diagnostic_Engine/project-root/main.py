from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import List, Optional
import uuid
from engine import update_ability

app = FastAPI()

# MongoDB Setup
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.adaptive_test_db

# Pydantic Models
class Question(BaseModel):
    id: str
    text: str
    options: List[str]
    difficulty: float
    topic: str
    correct_answer: str

class UserSession(BaseModel):
    session_id: str
    ability_score: float = 0.5
    answered_questions: List[str] = []

@app.post("/start")
async def start_test():
    session_id = str(uuid.uuid4())
    session = {"session_id": session_id, "ability_score": 0.5, "answered_questions": []}
    await db.sessions.insert_one(session)
    
    # Get initial question closest to 0.5
    first_q = await db.questions.find_one({"difficulty": {"$gte": 0.4, "$lte": 0.6}})
    return {"session_id": session_id, "first_question": first_q}

@app.post("/submit")
async def submit_answer(session_id: str, question_id: str, user_answer: str):
    session = await db.sessions.find_one({"session_id": session_id})
    question = await db.questions.find_one({"_id": question_id})
    
    if not session or not question:
        raise HTTPException(status_code=404, detail="Session or Question not found")

    is_correct = (user_answer == question["correct_answer"])
    
    # 1. Update Ability Score
    new_theta = update_ability(session["ability_score"], question["difficulty"], is_correct)
    
    # 2. Update Session in DB
    await db.sessions.update_one(
        {"session_id": session_id},
        {"$set": {"ability_score": new_theta}, "$push": {"answered_questions": question_id}}
    )
    
    # 3. Find Next Question (Closest to new theta, not already answered)
    next_q = await db.questions.find({
        "_id": {"$nin": session["answered_questions"] + [question_id]}
    }).sort([("difficulty", 1)]).to_list(length=20)
    
    # Simple logic: pick the one with the smallest difference to new_theta
    best_next = min(next_q, key=lambda x: abs(x["difficulty"] - new_theta))
    
    return {
        "is_correct": is_correct,
        "new_ability": round(new_theta, 2),
        "next_question": best_next
    }