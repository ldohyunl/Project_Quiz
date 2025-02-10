from django.urls import path


# CustomLoginView는 LoginView를 상속받아 템플릿을 오버라이드하여 사용자가 만든 템플릿을 사용하도록 합니다.

from . import views

urlpatterns = [
    path("", views.login, name="login"), # 루트 URL에 index.html 연결
    #path('login/', CustomLoginView.as_view(), name='custom_login'),  # 사용자 정의 로그인 URL
]