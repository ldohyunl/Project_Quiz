from django.urls import path
from .sep_views.upload_view import index
from .sep_views.dboperations import save_quiz_score
from .sep_views.quiz_view import multiple_view, short_view, OX_view

urlpatterns = [
    path('', index, name='index'),
    path('multiple/', multiple_view, name='multiple'),
    path('short/', short_view, name='short'),
    path('OX/', OX_view, name='OX'),
    path("save-quiz-score/", save_quiz_score, name="save_quiz_score"),
]