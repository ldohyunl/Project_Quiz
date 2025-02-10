from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from .models import SocialUserProfile

@receiver(post_save, sender=SocialAccount)
def create_or_update_social_user_profile(sender, instance, created, **kwargs):
    """ 소셜 로그인 시 사용자 정보를 SocialUserProfile 테이블에 저장 """
    if created:
        user = instance.user
        provider = instance.provider  # 'naver' 또는 'kakao'
        extra_data = instance.extra_data  # 소셜 계정의 추가 정보 (JSON)

        # 네이버 또는 카카오에서 제공하는 정보 가져오기
        email = extra_data.get("email", "")
        nickname = extra_data.get("nickname", "")
        profile_image = extra_data.get("profile_image", "")

        # SocialUserProfile 테이블에 데이터 저장
        SocialUserProfile.objects.create(
            user=user,
            social_account=instance,
            provider=provider,
            email=email,
            nickname=nickname,
            profile_image=profile_image,
        )
