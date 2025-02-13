from django.shortcuts import render
from .forms import FileUploadForm
import os
import openai
import fitz  # PyMuPDF (PDF용)
import openpyxl  # Excel용
from pptx import Presentation  # PPT용
from docx import Document  # Word(DOCX)용
from django.conf import settings
import re
import json
from .models import Quiz, Choice

# OpenAI API 클라이언트 초기화
client = openai.OpenAI(api_key=settings.OPEN_API_KEY)


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
def generate_quiz_with_gpt(text):
    # System prompt를 별도로 변수에 저장
    system_prompt = """
    You have excellent knowledge in all fields. Create difficult problems in a format based on text provided by the user.
    """

    # 질문 형식과 파일 내용을 포함한 user prompt
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
           - `\\( x^2 \\)` → `x²`
           - `\\frac{{a}}{{b}}` → `a/b`
           - `\\lim_{{x \\to 0}}` → `lim (x → 0)`
        📌 **모든 선택지는 서로 다른 내용을 가져야 합니다.** (중복된 보기를 만들지 마세요.)

        이 형식을 유지해서 문제를 만들어 주세요.
        """

    # GPT-4 요청
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        max_tokens=4000
    )
    return response.choices[0].message.content


# 문제와 답을 딕셔너리로 변환하는 함수
def parse_quiz_to_dict(quiz_text):
    quiz_dict = {}

    print(quiz_text)

    # 문제별로 구분하는 패턴 (정답까지 포함)
    question_pattern = r"(\d+)\.\s(.+?)(?=\n\d+\.|\Z)"  # 각 문제를 구분 (다음 문제 번호가 나오기 전까지)
    choice_pattern = r"([a-d])\)\s(.+)"  # a) b) c) d) 선택지 추출
    correct_answer_pattern = r"정답:\s*([a-d])"  # 정답 추출

    # 문제 추출
    questions = re.findall(question_pattern, quiz_text, re.S)  # re.S를 추가해서 줄바꿈도 포함하도록 함

    quiz_dict = {}

    for idx, question_text in questions:
        # 선택지 추출 (해당 문제 범위에서만 찾도록 함)
        choices = re.findall(choice_pattern, question_text)

        choices_dict = {choice[0]: choice[1].strip() for choice in choices if choice[0] in ['a', 'b', 'c', 'd']}

        # 정답 찾기 (해당 문제 범위에서만)
        correct_answer_match = re.search(correct_answer_pattern, question_text)
        correct_answer = correct_answer_match.group(1) if correct_answer_match else "오류"

        quiz_dict[idx] = {
            'question': question_text.strip().split("\n")[0],  # 첫 줄을 문제로 설정
            'choices': choices_dict,
            'correct_answer': correct_answer
        }

    return quiz_dict


# 퀴즈 데이터를 모델에 저장하는 함수
def save_quiz_to_db(quiz_dict):
    for question_id, question_data in quiz_dict.items():
        quiz = Quiz.objects.create(
            question=question_data['question'],
            correct_answer=question_data['correct_answer']
        )


# 파일 업로드 및 텍스트 추출 후 퀴즈 생성 함수
def index(request):
    form = FileUploadForm()
    quiz_text = None  # GPT가 생성한 퀴즈 원본 텍스트
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data["file"]
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
                    # 🔹 GPT로 문제 생성
                    quiz_text = generate_quiz_with_gpt(file_text)

                    # 🔹 자동으로 딕셔너리 변환 후 DB에 저장
                    quiz_dict = parse_quiz_to_dict(quiz_text)
                    save_quiz_to_db(quiz_dict)
                    print(quiz_dict)

                    return render(request, 'quiz_app/index.html', {
                        'quiz_text': quiz_text,  # 웹에 표시 (GPT가 생성한 문제 원본)
                        'form': form
                    })
                else:
                    return render(request, 'quiz_app/index.html', {'error': "파일에서 텍스트를 추출할 수 없습니다.", 'form': form})
            except Exception as e:
                return render(request, 'quiz_app/index.html', {'error': f"오류 발생: {e}", 'form': form})

    return render(request, 'quiz_app/index.html', {'form': form})


# example.html 렌더링하는 뷰
def example_view(request):
    return render(request, 'quiz_app/example.html')
