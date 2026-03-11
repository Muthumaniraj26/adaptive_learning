import math

def calculate_probability(theta, difficulty):
    """Standard 1PL IRT Model: P(correct) = 1 / (1 + exp(-(theta - difficulty)))"""
    return 1 / (1 + math.exp(-(theta - difficulty)))

def update_ability(current_theta, question_difficulty, is_correct, k_factor=0.3):
    """
    Updates the Ability Score (Theta).
    k_factor determines how 'fast' the score changes.
    """
    prob = calculate_probability(current_theta, question_difficulty)
    actual = 1.0 if is_correct else 0.0
    
    # New Theta = Old Theta + Adjustment based on error
    new_theta = current_theta + k_factor * (actual - prob)
    
    # Keep theta within 0.1 to 1.0 range as per assignment
    return max(0.1, min(1.0, new_theta))