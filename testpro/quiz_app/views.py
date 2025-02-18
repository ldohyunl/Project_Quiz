from django.shortcuts import render, redirect
from .forms import FileUploadForm
import openai
import fitz  # PyMuPDF (PDF용)
import openpyxl  # Excel용
from pptx import Presentation  # PPT용
from docx import Document  # Word(DOCX)용
from django.utils import timezone
from django.conf import settings
import re
import json
from .models import User_Quiz_Data
import os
from dotenv import load_dotenv  # dotenv 로드
from django.contrib.auth.decorators import login_required

# OpenAI API 클라이언트 초기화
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 파일 형식별 텍스트 추출 함수들
def extract_text_from_pptx(file_path):
    presentation = Presentation(file_path)
    text = [shape.text.strip() for slide in presentation.slides for shape in slide.shapes if
            hasattr(shape, "text") and shape.text.strip()]
    return "\n".join(text)


def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = [page.get_text("text") for page in doc]
    return "\n".join(text)


def extract_text_from_docx(file_path):
    doc = Document(file_path)
    text = [para.text.strip() for para in doc.paragraphs if para.text.strip()]
    return "\n".join(text)


def extract_text_from_xlsx(file_path):
    workbook = openpyxl.load_workbook(file_path)
    text = []
    for sheet in workbook.worksheets:
        for row in sheet.iter_rows():
            text.append(" | ".join([str(cell.value) for cell in row if cell.value]))
    return "\n".join(text)


def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pptx":
        return extract_text_from_pptx(file_path)
    elif ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    elif ext == ".xlsx":
        return extract_text_from_xlsx(file_path)
    else:
        raise ValueError("지원되지 않는 파일 형식입니다.")


# GPT로 문제 생성 함수
def generate_quiz_with_gpt(text, question_type):
    # System prompt를 별도로 변수에 저장
    system_prompt = """
    You have excellent knowledge in all fields. Create difficult problems in a format based on text provided by the user.
    """

    # 문제 유형에 따라 prompt 내용 다르게 설정
    if question_type == "MCQ":  # 객관식 문제
        prompt = f"""
            다음 텍스트를 기반으로 10개의 객관식 문제를 만들어 주세요. *한국어로!!* 

            === 주어진 텍스트 ===
            {text}

            📌 문제 형식 (반드시 아래 형식을 지켜서 출력하세요):
            1. [질문 내용]
            a) [보기1]
            b) [보기2]
            c) [보기3]
            d) [보기4]
            정답: [정답의 알파벳 하나만 출력]

            📌 반드시 문제는 "1."부터 "10."까지 숫자로 시작해야 합니다.
            📌 선택지는 "a)", "b)", "c)", "d)" 형식으로 작성하세요.
            📌 "정답:" 뒤에는 오직 정답의 알파벳 (a/b/c/d)만 있어야 합니다.
            📌 수학 문제에서 지수를 나타낼 때 `2^3` 같은 형식이 아니라, 반드시 **위 첨자(예: 2³, x², 10⁵)** 를 사용하세요.
            📌 수식은 LaTeX이 아닌 일반적인 수학 표기법을 사용하세요. 
            예시:
            - `\$begin:math:text$ x^2 \\$end:math:text$` → `x²`
            - `\\frac{{a}}{{b}}` → `a/b`
            - `\\lim_{{x \\to 0}}` → `lim (x → 0)`
            📌 **모든 선택지는 서로 다른 내용을 가져야 합니다.** (중복된 보기를 만들지 마세요.)

            이 형식을 유지해서 문제를 만들어 주세요.
        """
    elif question_type == "OX":  # O/X 문제
        prompt = f"""
            다음 텍스트를 기반으로 10개의 O/X 문제를 만들어 주세요. *한국어로!!*

            === 주어진 텍스트 ===
            {text}

            📌 문제 형식 (반드시 아래 형식을 지켜서 출력하세요):
            1. [질문 내용]
            정답: [O 또는 X]

            📌 반드시 문제는 "1."부터 "10."까지 숫자로 시작해야 합니다.
            📌 정답은 "O" 또는 "X"로만 작성해주세요.
        """
    elif question_type == "Short":  # 단답형 문제
        prompt = f"""
            다음 텍스트를 기반으로 10개의 단답형 문제를 만들어 주세요. *한국어로!!*

            === 주어진 텍스트 ===
            {text}

            📌 문제 형식 (반드시 아래 형식을 지켜서 출력하세요):
            1. [질문 내용]
            정답: [정답 내용]

            📌 반드시 문제는 "1."부터 "10."까지 숫자로 시작해야 합니다.
        """
    else:
        raise ValueError("지원되지 않는 문제 유형입니다.")

    # GPT-4 요청
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        max_tokens=4000
    )

    return response.choices[0].message.content


# 문제 유형에 따라 문제와 답을 딕셔너리로 변환하는 함수
def parse_quiz_to_dict(quiz_text, question_type):
    quiz_dict = {}

    print(quiz_text)  # 디버깅용, 생성된 문제 원본을 확인하기 위해 출력

    if question_type == "MCQ":  # 객관식 문제
        question_pattern = r"(\d+)\.\s(.+?)(?=\n\d+\.|\Z)"
        choice_pattern = r"([a-d])\)\s(.+)"
        correct_answer_pattern = r"정답:\s*([a-d])"

        questions = re.findall(question_pattern, quiz_text, re.S)

        for idx, question_text in questions:
            choices = re.findall(choice_pattern, question_text)
            choices_dict = {choice[0]: choice[1].strip() for choice in choices if choice[0] in ['a', 'b', 'c', 'd']}
            correct_answer_match = re.search(correct_answer_pattern, question_text)
            correct_answer = correct_answer_match.group(1) if correct_answer_match else "오류"

            quiz_dict[idx] = {
                'question': question_text.strip().split("\n")[0],
                'choices': choices_dict,
                'correct_answer': correct_answer
            }

    elif question_type == "OX":  # OX 문제
        question_pattern = r"(\d+)\.\s(.+?)(?=\n\d+\.|\Z)"
        correct_answer_pattern = r"정답:\s*(O|X)"

        questions = re.findall(question_pattern, quiz_text, re.S)

        for idx, question_text in questions:
            correct_answer_match = re.search(correct_answer_pattern, question_text)
            correct_answer = correct_answer_match.group(1) if correct_answer_match else "오류"

            quiz_dict[idx] = {
                'question': question_text.strip().split("\n")[0],
                'choices': None,  # OX 문제는 선택지가 없음
                'correct_answer': correct_answer
            }

    elif question_type == "Short":  # 단답형 문제
        question_pattern = r"(\d+)\.\s(.+?)(?=\n\d+\.|\Z)"
        correct_answer_pattern = r"정답:\s*(.+)"

        questions = re.findall(question_pattern, quiz_text, re.S)

        for idx, question_text in questions:
            correct_answer_match = re.search(correct_answer_pattern, question_text)
            correct_answer = correct_answer_match.group(1) if correct_answer_match else "오류"

            quiz_dict[idx] = {
                'question': question_text.strip().split("\n")[0],
                'choices': None,  # 단답형 문제는 선택지가 없음
                'correct_answer': correct_answer
            }

    return quiz_dict

# db 데이터 저장
def save_quiz_to_db(quiz_dict, user, file_name, question_type):
    User_Quiz_Data.objects.create(
        created_at=timezone.now(),
        quiz_data=quiz_dict,
        user=user,
        file_name=file_name,  # 사용자가 지정한 파일 이름도 함께 저장
        question_type=question_type  # 문제 유형 저장
    )


@login_required
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
                if file_text:
                    # GPT로 문제 생성
                    quiz_text = generate_quiz_with_gpt(file_text, question_type)
                    quiz_dict = parse_quiz_to_dict(quiz_text, question_type)
                    save_quiz_to_db(quiz_dict, request.user, file_name, question_type)

                    # 문제 생성 후 바로 'example' 페이지로 리디렉션
                    return redirect('example')
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

def example_view(request):
    # 예시: 특정 사용자의 최신 퀴즈 데이터를 가져옴
    user = request.user  # 현재 로그인한 사용자를 가져옴
    quiz_data = User_Quiz_Data.objects.filter(user=user).order_by('-created_at').first()

    if quiz_data:
        quiz_dict = quiz_data.quiz_data  # 저장된 quiz_data를 가져옴
        question_type = quiz_data.question_type  # 문제 유형 가져오기
    else:
        quiz_dict = None
        question_type = None

    # 현재 문제 번호 (1번 문제부터 시작)
    current_question_number = int(request.GET.get('question_number', 1))

    # 현재 문제 가져오기
    current_question = quiz_dict.get(str(current_question_number), None) if quiz_dict else None

    context = {
        'current_question': current_question,
        'quiz_data': quiz_dict,
        'question_type': question_type,
        'current_question_number': current_question_number,
    }

    return render(request, 'quiz_app/example.html', context)