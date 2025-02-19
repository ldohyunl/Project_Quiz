from django.urls import path
from .views import history_view, history_detail_view, quiz_detail_view, retake_quiz_view  # ✅ quiz_retake 뷰 추가

urlpatterns = [
    path('', history_view, name='history'),
    path('<str:selected_date>/', history_detail_view, name='history_detail'),
    path('<int:quiz_id>/', quiz_detail_view, name='quiz_detail'),  # ✅ 퀴즈 상세 페이지
    path('<int:quiz_id>/retake/', retake_quiz_view, name='quiz_retake'),  # ✅ 다시 풀기 URL 추가
]
