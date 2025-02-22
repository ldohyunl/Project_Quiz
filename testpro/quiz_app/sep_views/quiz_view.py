from django.shortcuts import render
from ..models import User_Quiz_Data

def multiple_view(request):
    # 1. DB에서 최신 퀴즈 데이터 가져오기
    user = request.user
    quiz_data_obj = User_Quiz_Data.objects.filter(user=user).order_by('-created_at').first()

    if quiz_data_obj:
        quiz_dict = quiz_data_obj.quiz_data  # 예: {"1": {...}, "2": {...}, ...}
        question_type = quiz_data_obj.question_type
    else:
        quiz_dict = None
        question_type = None

    # 2. 현재 문제 번호 (1번부터 시작)
    current_question_number = int(request.GET.get('question_number', 1))

    # 3. 현재 문제 가져오기
    current_question = quiz_dict.get(str(current_question_number), None) if quiz_dict else None

    # 4. 템플릿에 전달할 컨텍스트
    context = {
        'current_question': current_question,
        'quiz_data': quiz_dict,
        'question_type': question_type,
        'current_question_number': current_question_number,
    }
    # Multiple Choice (객관식) → example.html
    return render(request, 'quiz_app/example.html', context)


def short_view(request):
    # 1. DB에서 최신 퀴즈 데이터 가져오기
    user = request.user
    quiz_data_obj = User_Quiz_Data.objects.filter(user=user).order_by('-created_at').first()

    if quiz_data_obj:
        quiz_dict = quiz_data_obj.quiz_data
        question_type = quiz_data_obj.question_type
    else:
        quiz_dict = {}
        question_type = None

    # 2. quiz_dict의 데이터를 프론트엔드에서 사용할 배열 형태로 변환
    questions = []
    # quiz_dict의 key가 문자열 숫자("1", "2", ...)이므로 정렬할 때 int로 변환합니다.
    for key in sorted(quiz_dict.keys(), key=int):
        q = quiz_dict[key]
        questions.append({
            'text': q.get('question', ''),
            'answer': q.get('correct_answer', '')
        })

    # 3. 템플릿에 전달할 컨텍스트 (questions 리스트를 포함)
    context = {
        'questions': questions,
        'quiz_data': quiz_dict,
        'question_type': question_type,
    }
    # Short Answer (단답형) → munje_shortanswer.html
    return render(request, 'quiz_app/munje_shortanswer.html', context)


def OX_view(request):
    # 1. DB에서 최신 퀴즈 데이터 가져오기
    user = request.user
    quiz_data_obj = User_Quiz_Data.objects.filter(user=user).order_by('-created_at').first()

    if quiz_data_obj:
        quiz_dict = quiz_data_obj.quiz_data  # 예: {"1": {"question": "...", "correct_answer": "O"}, ...}
        question_type = quiz_data_obj.question_type
    else:
        quiz_dict = {}
        question_type = None

    # 2. DB에 저장된 O/X 퀴즈 데이터를 프론트엔드에서 사용할 배열 형태로 변환
    # 각 문제는 { text, options, correctIndex } 형태가 되도록 변환합니다.
    # - options는 고정으로 ["참", "거짓"]입니다.
    # - correctIndex는 correct_answer가 "O"이면 0, "X"이면 1로 설정합니다.
    questions = []
    for key in sorted(quiz_dict.keys(), key=int):
        q = quiz_dict[key]
        correct_ans = q.get("correct_answer", "O")
        correctIndex = 0 if correct_ans.upper() == "O" else 1
        questions.append({
            "text": q.get("question", ""),
            "options": ["참", "거짓"],
            "correctIndex": correctIndex
        })

    # 3. 템플릿에 전달할 컨텍스트 구성
    context = {
        "questions": questions,
        "quiz_data": quiz_dict,
        "question_type": question_type,
    }
    # O/X (True/False) → munje_truefalse.html
    return render(request, "quiz_app/munje_truefalse.html", context)
