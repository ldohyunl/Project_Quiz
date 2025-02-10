from django.db import models

class UserProfile(models.Model):
    email = models.EmailField(unique=True)  # 이메일 필드
    username = models.CharField(max_length=100)  # 사용자 이름
    social_provider = models.CharField(max_length=50)  # 소셜 로그인 종류 (네이버, 구글 등)
    created_at = models.DateTimeField(auto_now_add=True)  # 가입일

    def __str__(self):
        return self.username