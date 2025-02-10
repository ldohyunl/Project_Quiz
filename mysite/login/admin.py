from django.contrib import admin

# Register your models here.
from .models import SocialUserProfile

@admin.register(SocialUserProfile)
class SocialUserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "provider", "email", "nickname", "created_at")
    search_fields = ("user__username", "email", "nickname")

