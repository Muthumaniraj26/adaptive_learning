import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_study_plan(final_score: float, performance_history: list):
    """
    Sends session data to LLM to create a personalized plan.
    """
    # Analyze history to find weak topics
    wrong_answers = [item['topic'] for item in performance_history if not item['is_correct']]
    weak_topics = ", ".join(set(wrong_answers)) if wrong_answers else "None"

    prompt = f"""
    A student completed a GRE diagnostic test.
    Final Proficiency Score: {final_score}/1.0
    Weak Topics identified: {weak_topics}
    
    Based on this data, provide a concise 3-step study plan to improve their score.
    Format the response as:
    1. Immediate Focus
    2. Practice Strategy
    3. Resource Recommendation
    """

    response = client.chat.completions.create(
        model="gpt-4o", # or gpt-3.5-turbo
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content