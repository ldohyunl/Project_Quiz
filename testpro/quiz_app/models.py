from django.db import models
from django.conf import settings

class User_Quiz_Data(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Django 사용자 모델 참조
        on_delete=models.CASCADE,  # 유저 삭제 시 해당 유저의 퀴즈도 삭제
        related_name='quizzes',  # user.quizzes.all()로 접근 가능
    )
    file_name = models.CharField(max_length=255, default="Untitled")  # 파일 이름
    quiz_data = models.JSONField()  # 퀴즈 데이터를 JSON 형태로 저장
    question_type = models.CharField(max_length=20,
                                     choices=[('MCQ', '객관식'), ('OX', 'O/X'), ('Short', '단답형')],
                                     default='MCQ')  # 문제 유형 저장
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간

    def __str__(self):
        return f"Quiz data for {self.user.username} at {self.created_at}"