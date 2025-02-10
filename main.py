messages = [
    {
        "role": "system",
        "content": (
            "You are an AI that summarizes PowerPoint content and generates multiple-choice questions. "
            "Based on the summary, create 10 multiple-choice questions with 5 answer choices each. "
            "Make sure the questions are in Korean and display only the questions and answer choices without explanations."
        ),
    },
    {
        "role": "user",
        "content": (
            f"Summarize the following PowerPoint content:\n\n{text}\n\n"
            "Then, create 10 multiple-choice questions (5 answer choices each) in Korean.\n"
            "Only show the questions and answer choices, and do not include explanations or summaries."
        ),
    }
],
max_tokens = 3000  # 요약 길이 제한