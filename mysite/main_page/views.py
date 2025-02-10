from django.shortcuts import render

def home(request):
    return render(request, 'main_page/home.html', {})  # 템플릿 연결
