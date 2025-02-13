from django.urls import path
from . import views

# url 과 view 를 연결하기 위해 사용
urlpatterns = [
    path('', views.index, name='index'),
    path('example/', views.example_view, name='example'),
]
                                                # 루트 경로에 해당하는 뷰 함수
                                                # views.py 파일 안에 있는 index 뷰 함수를 실행
                                                # index(request) 함수가 호출되면서 클라이언트가 원하는 HTML을 반환
