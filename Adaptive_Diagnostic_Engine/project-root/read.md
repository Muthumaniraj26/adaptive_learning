# Implementation Instructions

To complete the AI-Driven Adaptive Diagnostic Engine, follow these structural and technical steps.

## 1. Environment Setup

Create a virtual environment and install the required dependencies.
- **Python Version:** 3.9 or higher.
- **Dependencies:** `fastapi`, `uvicorn`, `motor`, `pydantic`, `openai`, `python-dotenv`.
- **Database:** Install MongoDB locally or create a cluster on MongoDB Atlas.

## 2. Directory Structure

Organize your code to ensure modularity and separation of concerns.
- `app/main.py`: Entry point for FastAPI routes.
- `app/models.py`: Pydantic schemas for data validation.
- `app/database.py`: MongoDB connection and seeding logic.
- `app/engine.py`: IRT algorithm and question selection logic.
- `app/ai_service.py`: OpenAI/Anthropic API integration for study plans.
- `.env`: Store `MONGO_URI` and `OPENAI_API_KEY`.

## 3. Core Algorithm (Item Response Theory)

The engine must not use a linear difficulty increase. It must use the 1-Parameter Logistic (1PL) model.
- **Probability Formula:** $P(\theta) = \frac{1}{1 + e^{-(\theta - b)}}$ where $\theta$ is user ability and $b$ is question difficulty.
- **Update Rule:** Adjust $\theta$ based on the difference between the actual result (1 or 0) and the predicted probability.

## 4. Execution Workflow

- **Seed the Database:** Run a script to insert at least 20 questions into the questions collection. Each must have a difficulty field between 0.1 and 1.0.
- **Initialize Session:** The `/start` endpoint creates a `UserSession` document with an initial `ability_score` of 0.5.
- **The Adaptive Loop:**
  - The user submits an answer via `/submit-answer`.
  - The system calculates the new `ability_score` using `engine.py`.
  - The system queries MongoDB for the next question: find questions not in history where difficulty is closest to new `ability_score`.
- **Generate Insights:** After 10 questions, the backend sends the session history to the LLM via `ai_service.py` to generate a structured 3-step study plan.

## 5. Evaluation Readiness

- **Error Handling:** Ensure the system handles cases where the database connection fails or the question bank is exhausted.
- **Documentation:** FastAPI will automatically generate documentation at `/docs`. Ensure all endpoints are clearly named.
- **AI Log:** Document specific prompts used to generate the question bank or to debug the IRT mathematical implementation.

---

# AI-Driven Adaptive Diagnostic Engine

## Project Description
A professional-grade adaptive testing prototype that utilizes Item Response Theory (IRT) to dynamically assess student proficiency. The system adjusts question difficulty in real-time based on user performance and provides an AI-generated personalized learning plan upon completion.

## Technical Stack
- **Backend:** FastAPI (Python)
- **Database:** MongoDB
- **AI Integration:** OpenAI API / Anthropic API
- **Mathematical Model:** 1-Parameter Logistic (1PL) IRT

## Adaptive Algorithm Logic
The engine utilizes a 1D Adaptive Logic:
1. **Initial Ability:** Every user starts with a baseline $\theta$ (theta) of 0.5.
2. **Probability Calculation:** For every question, the system calculates the probability of a correct response based on the gap between user ability and question difficulty.
3. **Theta Update:** After each response, the user's ability score is refined. A correct answer on a high-difficulty question results in a larger upward shift than a correct answer on an easy question.
4. **Question Selection:** The system performs a proximity search in MongoDB to find the most appropriate next question for the user's current estimated ability.



## Installation and Setup
1. Clone the repository.
2. Create a `.env` file with `MONGO_URI` and `OPENAI_API_KEY`.
3. Install dependencies: `pip install -r requirements.txt`.
4. Seed the database: `python seed_db.py`.
5. Start the server: `uvicorn app.main:app --reload`.

## API Endpoints
- `POST /start`: Initializes a test session.
- `POST /submit-answer`: Validates response and updates ability score.
- `GET /next-question`: Retrieves the next optimized question.
- `GET /results/{session_id}`: Provides the final score and LLM-generated study plan.

## AI Log
- **Usage:** Used LLM to generate 20 GRE-style questions with calibrated difficulty scores.
- **Problem Solving:** AI was utilized to verify the gradient descent logic for the IRT parameter updates.
- **Limitations:** The LLM required multiple iterations to produce questions with mathematically accurate difficulty scores.