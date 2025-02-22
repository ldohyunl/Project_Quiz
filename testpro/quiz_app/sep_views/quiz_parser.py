import re
# 문제 유형에 따라 문제와 답을 딕셔너리로 변환하는 함수

def parse_quiz_to_dict(quiz_text, question_type):
    quiz_dict = {}
    if question_type == "MCQ":
        question_pattern = r"(\d+)\.\s(.+?)(?=\n\d+\.|\Z)"
        choice_pattern = r"([a-d])\)\s(.+)"
        correct_answer_pattern = r"정답:\s*([a-d])"
        questions = re.findall(question_pattern, quiz_text, re.S)
        for idx, question_text in questions:
            choices = re.findall(choice_pattern, question_text)
            choices_dict = {choice[0]: choice[1].strip() for choice in choices if choice[0] in ['a','b','c','d']}
            correct_answer_match = re.search(correct_answer_pattern, question_text)
            correct_answer = correct_answer_match.group(1) if correct_answer_match else "오류"
            quiz_dict[idx] = {
                'question': question_text.strip().split("\n")[0],
                'choices': choices_dict,
                'correct_answer': correct_answer
            }
    elif question_type == "OX":
        question_pattern = r"(\d+)\.\s(.+?)(?=\n\d+\.|\Z)"
        correct_answer_pattern = r"정답:\s*(O|X)"
        questions = re.findall(question_pattern, quiz_text, re.S)
        for idx, question_text in questions:
            correct_answer_match = re.search(correct_answer_pattern, question_text)
            correct_answer = correct_answer_match.group(1) if correct_answer_match else "오류"
            quiz_dict[idx] = {
                'question': question_text.strip().split("\n")[0],
                'correct_answer': correct_answer
            }
    elif question_type == "Short":
        question_pattern = r"(\d+)\.\s(.+?)(?=\n\d+\.|\Z)"
        correct_answer_pattern = r"정답:\s*(.+)"
        questions = re.findall(question_pattern, quiz_text, re.S)
        for idx, question_text in questions:
            correct_answer_match = re.search(correct_answer_pattern, question_text)
            correct_answer = correct_answer_match.group(1) if correct_answer_match else "오류"
            quiz_dict[idx] = {
                'question': question_text.strip().split("\n")[0],
                'correct_answer': correct_answer
            }
    return quiz_dict