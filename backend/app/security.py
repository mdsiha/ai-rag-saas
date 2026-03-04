def is_safe_question(question: str) -> bool:
    forbidden_patterns = [
        "ignore previous instructions",
        "ignore les instructions",
        "donne moi le mot de passe",
        "system prompt",
    ]

    lower_q = question.lower()

    for pattern in forbidden_patterns:
        if pattern in lower_q:
            return False

    return True