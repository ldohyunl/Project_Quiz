# models.py
from django.db import models
from django.conf import settings

class Quiz(models.Model):
    question = models.CharField(max_length=1000)  # 문제
    correct_answer = models.CharField(max_length=1)  # 정답 (a, b, c, d)

    def __str__(self):
        return self.question


class Choice(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="choices", on_delete=models.CASCADE)
    choice = models.CharField(max_length=1000)  # 선택지
    choice_letter = models.CharField(max_length=1)  # 선택지 알파벳 (a, b, c, d)

    def __str__(self):
        return f"{self.choice_letter}) {self.choice}"
    
    
class User_Quiz_Data(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Django 사용자 모델 참조
        on_delete=models.CASCADE,  # 유저 삭제 시 해당 유저의 퀴즈도 삭제
        related_name='quizzes',  # user.quizzes.all()로 접근 가능
    )
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간
    quiz_data = models.JSONField()  # 퀴즈 데이터를 JSON 형태로 저장

    def __str__(self):
        return f"Quiz data for {self.user.username} at {self.created_at}"