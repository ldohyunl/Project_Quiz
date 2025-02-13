# models.py
from django.db import models


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