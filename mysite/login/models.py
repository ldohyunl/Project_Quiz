# from django.db import models

# class UserProfile(models.Model):
#     email = models.EmailField(unique=True)  # 이메일 필드
#     username = models.CharField(max_length=100)  # 사용자 이름
#     social_provider = models.CharField(max_length=50)  # 소셜 로그인 종류 (네이버, 구글 등)
#     created_at = models.DateTimeField(auto_now_add=True)  # 가입일

#     def __str__(self):
#         return self.username

from django.db import models
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount # type: ignore

class SocialUserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Django 기본 User 모델과 연결
    social_account = models.OneToOneField(SocialAccount, on_delete=models.CASCADE)  # allauth의 SocialAccount와 연결
    provider = models.CharField(max_length=50)  # 네이버 / 카카오 구분
    email = models.EmailField(unique=True, blank=True, null=True)  # 이메일 정보 (없을 수도 있음)
    nickname = models.CharField(max_length=100, blank=True, null=True)  # 사용자 닉네임
    profile_image = models.URLField(blank=True, null=True)  # 프로필 이미지 URL
    created_at = models.DateTimeField(auto_now_add=True)  # 계정 생성일

    def __str__(self):
        return f"{self.user.username} ({self.provider})"
