from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quiz_app.urls')),  # quiz_app의 URL을 포함시킴
]