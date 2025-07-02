from typing import Tuple


def validate_set_data(title: str, description: str = '', max_title_length: int = 100, max_description_length: int = 500) -> Tuple[bool, str]:
    if not title or not title.strip():
        return False, "Set title is required"
    
    if len(title.strip()) > max_title_length:
        return False, f"Set title must be less than {max_title_length} characters"
    
    if description and len(description) > max_description_length:
        return False, f"Description must be less than {max_description_length} characters"
    
    return True, ""


def validate_card_data(question: str, answer: str, max_question_length: int = 1000, max_answer_length: int = 1000) -> Tuple[bool, str]:
    if not question or not question.strip():
        return False, "Question is required"
    
    if not answer or not answer.strip():
        return False, "Answer is required"
    
    if len(question.strip()) > max_question_length:
        return False, f"Question must be less than {max_question_length} characters"
    
    if len(answer.strip()) > max_answer_length:
        return False, f"Answer must be less than {max_answer_length} characters"
    
    return True, "" 