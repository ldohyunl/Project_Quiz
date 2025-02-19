from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from quiz_app.models import User_Quiz_Data
from collections import defaultdict
import dateutil.parser

from datetime import datetime

@login_required
def history_view(request):
    """퀴즈 히스토리 페이지"""
    user = request.user
    search_query = request.GET.get('search', '')

    # 데이터베이스에서 퀴즈 데이터 가져오기
    quizzes = User_Quiz_Data.objects.filter(user=user).order_by('-created_at')

    # 검색 기능 추가 (과목명 기반 검색)
    if search_query:
        quizzes = quizzes.filter(file_name__icontains=search_query)

    # ✅ 날짜별로 데이터 그룹화 (datetime 객체 유지)
    grouped_quizzes = defaultdict(list)
    for quiz in quizzes:
        date_obj = quiz.created_at.date()  # ✅ 문자열이 아니라 datetime.date 객체 사용
        grouped_quizzes[date_obj].append({
            "id": quiz.id,
            "file_name": quiz.file_name,
            "question_type": quiz.question_type,
            "score": quiz.quiz_data.get("score", "-"),
        })

    context = {
        'quizzes': dict(grouped_quizzes),  # ✅ dict 사용하여 템플릿에서 접근 가능
        'search_query': search_query
    }
    return render(request, 'history/history.html', context)

@login_required
def quiz_detail_view(request, quiz_id):
    """퀴즈 상세 페이지"""
    quiz = User_Quiz_Data.objects.get(id=quiz_id, user=request.user)

    context = {
        'quiz': quiz,
        'quiz_data': quiz.quiz_data
    }
    return render(request, 'history/quiz_detail.html', context)

@login_required
def retake_quiz_view(request, quiz_id):
    """퀴즈 다시 풀기"""
    quiz = User_Quiz_Data.objects.get(id=quiz_id, user=request.user)

    context = {
        'quiz': quiz,
        'quiz_data': quiz.quiz_data,
        'retake': True
    }
    return render(request, 'history/quiz_retake.html', context)

@login_required
def history_detail_view(request, selected_date):
    """선택한 날짜의 퀴즈 목록 페이지"""
    user = request.user

    try:
        date_obj = datetime.strptime(selected_date, "%Y-%m-%d").date()
    except ValueError:
        try:
            date_obj = dateutil.parser.parse(selected_date).date()  # ✅ 다양한 날짜 형식 지원
        except Exception as e:
            return render(request, 'history/history_detail.html', {'error': f"잘못된 날짜 형식: {e}"})

    # 해당 날짜에 생성된 퀴즈 필터링
    quizzes = User_Quiz_Data.objects.filter(user=user, created_at__date=date_obj)

    context = {
        'selected_date': date_obj,
        'quizzes': quizzes,
    }
    return render(request, 'history/history_detail.html', context)