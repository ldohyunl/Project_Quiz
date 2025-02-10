from django.shortcuts import render

# Create your views here.

# def index(request):
#     return render(request, "login/login.html","")


def login(request):
    return render(request, 'login/index.html', {})

