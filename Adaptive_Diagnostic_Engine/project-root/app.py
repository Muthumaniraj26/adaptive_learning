import os
import uuid
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from dotenv import load_dotenv
from engine import update_ability, calculate_probability
from openai import OpenAI
from flask import render_template
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

app = Flask(__name__)

# Database Setup
client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
db = client.adaptive_testing_db
questions_col = db.questions
sessions_col = db.sessions

# AI Setup
ai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/start', methods=['POST'])
def start_test():
    session_id = str(uuid.uuid4())
    # Initialize session with baseline ability 0.5
    session_data = {
        "session_id": session_id,
        "ability_score": 0.5,
        "history": [],
        "completed": False
    }
    sessions_col.insert_one(session_data)
    
    # Get first question closest to 0.5
    first_q = questions_col.find_one({"difficulty": {"$gte": 0.4, "$lte": 0.6}})
    
    return jsonify({
        "session_id": session_id,
        "question": {
            "id": str(first_q["_id"]),
            "text": first_q["text"],
            "options": first_q["options"],
            "topic": first_q["topic"]
        }
    })

@app.route('/submit', methods=['POST'])
def submit_answer():
    data = request.json
    sid = data.get("session_id")
    qid = data.get("question_id")
    user_ans = data.get("answer")

    session = sessions_col.find_one({"session_id": sid})
    # In a real app, convert qid to ObjectId if using Mongo IDs
    from bson.objectid import ObjectId
    question = questions_col.find_one({"_id": ObjectId(qid)})

    is_correct = (user_ans == question["correct_answer"])
    
    # Update Ability using IRT logic from engine.py
    new_theta = update_ability(session["ability_score"], question["difficulty"], is_correct)
    
    # Update Session
    sessions_col.update_one(
        {"session_id": sid},
        {
            "$set": {"ability_score": new_theta},
            "$push": {"history": {"topic": question["topic"], "is_correct": is_correct, "question_id": qid}}
        }
    )

    # If test ends (e.g., after 10 questions), trigger AI Plan
    if len(session["history"]) >= 9: # 9 + current 1 = 10
        return end_test(sid, new_theta)

    # Find next question closest to new_theta not already answered
    history_qids = [ObjectId(item["question_id"]) for item in session.get("history", []) if "question_id" in item]
    answered_ids = history_qids + [ObjectId(qid)]
    
    next_q = questions_col.find_one({
        "difficulty": {"$gte": new_theta - 0.2},
        "_id": {"$nin": answered_ids} 
    })
    
    # Fallback if no exact difficulty match found
    if not next_q:
        next_q = questions_col.find_one({"_id": {"$nin": answered_ids}})
        if not next_q:
            # Out of questions in the database entirely
            return end_test(sid, new_theta)

    return jsonify({
        "is_correct": is_correct,
        "correct_answer": question["correct_answer"],
        "new_score": round(new_theta, 2),
        "next_question": {
            "id": str(next_q["_id"]),
            "text": next_q["text"],
            "options": next_q["options"]
        }
    })

def end_test(sid, final_theta):
    session = sessions_col.find_one({"session_id": sid})
    history = session.get('history', [])
    correct_count = sum(1 for item in history if item.get('is_correct'))
    total_q = len(history)
    
    # AI Prompt
    prompt = f"Student finished GRE test with ability {final_theta}. History: {history}. Provide a 3-step study plan."
    
    try:
        response = ai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250
        )
        plan = response.choices[0].message.content
    except Exception as e:
        plan = f"AI Study plan currently unavailable (Invalid API Key). \n\nHowever, you completed the test! You got {correct_count} out of {total_q} questions correct."

    return jsonify({
        "final_score": final_theta, 
        "correct_count": correct_count, 
        "total_questions": total_q,
        "study_plan": plan
    })

if __name__ == '__main__':
    app.run(debug=True, port=8000)