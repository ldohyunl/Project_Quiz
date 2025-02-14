from django import forms

class FileUploadForm(forms.Form):
    file = forms.FileField()  # 파일 업로드 필드
    file_name = forms.CharField(max_length=255, required=False, label="파일 이름")  # 파일 이름 필드 (옵션으로 설정)
    question_type = forms.ChoiceField(
        choices=[('MCQ', '객관식'), ('OX', 'O/X'), ('Short', '단답형')],
        initial='MCQ',  # 기본값을 'MCQ'로 설정
        label="문제 유형"
    )