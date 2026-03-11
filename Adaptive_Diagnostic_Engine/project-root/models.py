from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class QuestionSchema(BaseModel):
    text: str
    options: List[str]
    correct_answer: str
    difficulty: float = Field(ge=0.1, le=1.0)
    topic: str
    tags: List[str]

class UserSessionSchema(BaseModel):
    user_id: str
    current_ability: float = 0.5
    history: List[dict] = []  # Stores {"question_id": str, "is_correct": bool}
    start_time: datetime = Field(default_factory=datetime.utcnow)
    is_completed: bool = False