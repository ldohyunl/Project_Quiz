from django import forms


# 파일 업로드와 관련
class FileUploadForm(forms.Form):
    file = forms.FileField()
