import os
from django.shortcuts import render, redirect
from django.urls import reverse
from ..forms import FileUploadForm
from .prompt_builder import generate_quiz_with_gpt
from .quiz_parser import parse_quiz_to_dict
from .dboperations import save_quiz_to_db
from .extract_files import extract_text



def index(request):
    form = FileUploadForm()
    quiz_text = None  # GPT가 생성한 퀴즈 원본 텍스트
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data["file"]
            question_type = form.cleaned_data["question_type"]  # 사용자가 선택한 문제 유형
            file_name = form.cleaned_data["file_name"] or "Untitled"  # 사용자가 입력한 파일 이름 없으면 "Untitled"로 설정
            upload_folder = "uploads"
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            file_path = os.path.join(upload_folder, file.name)
            with open(file_path, "wb") as f:
                for chunk in file.chunks():
                    f.write(chunk)

            try:
                file_text = extract_text(file_path)
                if not request.user.is_authenticated:  # 로그인 안하면 로그인 페이지로 리다이렉트 2/18 15:35 이도현
                    return redirect(reverse('account_login'))
                elif file_text:
                    # GPT로 문제 생성
                    quiz_text = generate_quiz_with_gpt(file_text, question_type)
                    quiz_dict = parse_quiz_to_dict(quiz_text, question_type)
                    save_quiz_to_db(quiz_dict, request.user, file_name, question_type)

                    # 문제 유형에 따라 다른 뷰로 리다이렉트
                    if question_type == "MCQ":
                        return redirect('multiple')
                    elif question_type == "Short":
                        return redirect('short')
                    else:
                        return redirect('OX')

                else:
                    return render(request, 'quiz_app/index.html', {
                        'error': "파일에서 텍스트를 추출할 수 없습니다.",
                        'form': form
                    })
            except Exception as e:
                return render(request, 'quiz_app/index.html', {
                    'error': f"오류 발생: {e}",
                    'form': form
                })

    return render(request, 'quiz_app/index.html', {'form': form})