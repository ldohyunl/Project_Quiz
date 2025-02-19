from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='account_login'),  # 'account_login' 이름으로 URL 설정
]