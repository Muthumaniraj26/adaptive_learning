import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client.adaptive_testing_db
questions_collection = db.questions

def seed_database():
    """Populates the initial database with GRE-style questions with varying difficulties"""
    # Check if already seeded to prevent duplicates
    if questions_collection.count_documents({}) > 0:
        print("Database already contains questions. Dropping collection to re-seed...")
        questions_collection.drop()

    sample_questions = [
        # Difficulty 0.1 - 0.3 (Easy)
        {"text": "What is 15% of 80?", "options": ["10", "12", "15", "18"], "correct_answer": "12", "difficulty": 0.2, "topic": "Arithmetic"},
        {"text": "If 3x - 5 = 16, what is x?", "options": ["5", "6", "7", "8"], "correct_answer": "7", "difficulty": 0.3, "topic": "Algebra"},
        {"text": "Simplify: 4(2a + 3) - 2a", "options": ["4a + 12", "6a + 12", "8a + 3", "6a + 3"], "correct_answer": "6a + 12", "difficulty": 0.3, "topic": "Algebra"},
        {"text": "A shirt originally costs $40. It is on sale for 25% off. What is the sale price?", "options": ["$10", "$25", "$30", "$35"], "correct_answer": "$30", "difficulty": 0.2, "topic": "Word Problems"},
        {"text": "If a triangle has a base of 6 and a height of 8, what is its area?", "options": ["24", "48", "14", "20"], "correct_answer": "24", "difficulty": 0.1, "topic": "Geometry"},
        
        # Difficulty 0.4 - 0.6 (Medium)
        {"text": "If x + y = 10 and x - y = 4, what is the value of x * y?", "options": ["21", "24", "25", "20"], "correct_answer": "21", "difficulty": 0.5, "topic": "Algebra"},
        {"text": "What is the slope of the line passing through (2, 3) and (4, 11)?", "options": ["2", "3", "4", "5"], "correct_answer": "4", "difficulty": 0.4, "topic": "Coordinate Geometry"},
        {"text": "A machine produces 120 widgets in 3 hours. How many widgets can 5 such machines produce in 2 hours?", "options": ["200", "300", "400", "500"], "correct_answer": "400", "difficulty": 0.6, "topic": "Word Problems"},
        {"text": "If the probability of event A is 0.4 and event B is 0.5, and they are independent, what is P(A and B)?", "options": ["0.1", "0.2", "0.8", "0.9"], "correct_answer": "0.2", "difficulty": 0.5, "topic": "Probability"},
        {"text": "What is the median of the following set of numbers: 3, 1, 4, 1, 5, 9, 2?", "options": ["3", "4", "2", "3.5"], "correct_answer": "3", "difficulty": 0.4, "topic": "Statistics"},

        # Difficulty 0.7 - 0.9 (Hard)
        {"text": "Find the sum of the infinite geometric series: 1 + 1/2 + 1/4 + 1/8 + ...", "options": ["1.5", "2", "Infinity", "Depends"], "correct_answer": "2", "difficulty": 0.7, "topic": "Sequences & Series"},
        {"text": "If log_2(x) + log_2(x-3) = 2, what is x?", "options": ["4", "-1", "4 or -1", "None of the above"], "correct_answer": "4", "difficulty": 0.8, "topic": "Logarithms"},
        {"text": "A circle is inscribed in a square of side length 's'. What is the ratio of the area of the circle to the area of the square?", "options": ["π/2", "π/4", "1/2", "π"], "correct_answer": "π/4", "difficulty": 0.8, "topic": "Geometry"},
        {"text": "How many ways can 5 people be seated around a circular table?", "options": ["120", "24", "60", "256"], "correct_answer": "24", "difficulty": 0.7, "topic": "Combinatorics"},
        {"text": "If a right circular cylinder's radius is doubled and its height is halved, how does its volume change?", "options": ["It remains the same", "It is halved", "It is doubled", "It is quadrupled"], "correct_answer": "It is doubled", "difficulty": 0.9, "topic": "3D Geometry"}
    ]

    questions_collection.insert_many(sample_questions)
    print(f"Successfully seeded {len(sample_questions)} questions into the database.")

if __name__ == "__main__":
    seed_database()