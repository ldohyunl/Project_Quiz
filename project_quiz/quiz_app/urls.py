from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # 루트 경로에 해당하는 뷰 함수
]