# AI-Driven Adaptive Diagnostic Engine

## Project Description
A professional-grade adaptive testing prototype that utilizes Item Response Theory (IRT) to dynamically assess student proficiency. The system adjusts question difficulty in real-time based on user performance and provides an AI-generated personalized learning plan upon completion.

## Instructions on How to Run the Project
1. **Clone the repository:**
   ```bash
   git clone <your-github-repo-url>
   cd Adaptive_Diagnostic_Engine/project-root
   ```
2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install flask pymongo python-dotenv openai motor
   ```
4. **Environment Variables:**
   Create a `.env` file in the project root directory and add your real API keys:
   ```env
   MONGO_URI="mongodb://localhost:27017" # Or your MongoDB Atlas URI
   OPENAI_API_KEY="sk-your-openai-api-key"
   ```
5. **Seed the database:**
   Run the seeding script once to populate the MongoDB database with mathematical GRE questions.
   ```bash
   python seed.py
   ```
6. **Start the server:**
   ```bash
   python app.py
   ```
   *The server will run on `http://127.0.0.1:8000`. Navigate to this URL in your browser to interact with the web interface.*

## Adaptive Algorithm Logic
This engine utilizes a 1-Parameter Logistic (1PL) Item Response Theory (IRT) model to evaluate student proficiency dynamically:
1. **Initial Ability:** Every user starts with a baseline ability score ($\theta$) of 0.5.
2. **Probability Calculation:** For each question, the system estimates the probability ($P(\theta)$) of the student answering correctly using the sigmoid function: $P(\theta) = \frac{1}{1 + e^{-(\theta - b)}}$, where $b$ is the question's set difficulty.
3. **Theta Update:** After each response, the user's ability score is refined. The engine calculates the error between the actual binary outcome (1 for correct, 0 for incorrect) and the predicted probability, multiplying it by a learning rate to dynamically update the student's estimated ability ($\theta$).
4. **Question Selection:** Next questions are dynamically chosen from the MongoDB database by querying for a question with a difficulty ($b$) that best matches the student's updated ability score ($\theta$). This ensures the student is perfectly challenged.

## API Documentation
Here are the REST API endpoints available in the system:
- `GET /`
  - **Description**: Serves the frontend web interface (`index.html`).
- `POST /start`
  - **Description**: Initializes a new test session, stores a baseline ability score of 0.5 in the DB, and returns the first question.
  - **Response body**: `{"session_id": "uuid", "question": {"id": "mongo_id", "text": "...", "options": [...]}}`
- `POST /submit`
  - **Description**: Submits an answer, updates the student's IRT ability score based on correctness, and either fetches the next optimally distant question from the database or returns a final AI-generated study plan if 10 questions have been completed.
  - **Request body**: `{"session_id": "uuid", "question_id": "uuid", "answer": "User String"}`
  - **Response body (Next question)**: `{"is_correct": bool, "correct_answer": "...", "new_score": float, "next_question": {...}}`
  - **Response body (Final Results)**: `{"final_score": float, "correct_count": int, "total_questions": int, "study_plan": "..."}`

## AI Log
- **Usage:** We actively utilized an LLM assistant to systematically structure the architecture (FastAPI/Flask + MongoDB), craft the 1PL IRT engine with gradient descent updates, rapidly build and format the user-facing HTML/JS interaction layer using `fetch()`, and auto-generate 15 valid mathematical mock GRE-style questions with realistic distraction answers and difficulty scores to seed the database.
- **Challenges/Limitations:** While the LLM successfully implemented the system logic, we had to intervene and prompt repeatedly to enforce correct REST payload handling and robust logic fallbacks (such as keeping track of `question_id`s in MongoDB histories to stop infinite repetition models), and resolving mismatched database connection strings (`adaptive_test_db` vs `adaptive_testing_db`) which caused `NoneType` lookup failures.
