import json
from django.utils import timezone
from django.http import JsonResponse
from ..models import User_Quiz_Data


def save_quiz_to_db(quiz_dict, user, file_name, question_type):
    User_Quiz_Data.objects.create(
        created_at=timezone.now(),
        quiz_data=quiz_dict,
        user=user,
        file_name=file_name,
        question_type=question_type
    )

def save_quiz_score(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            score = int(data.get("score", 0))
            latest_quiz = User_Quiz_Data.objects.filter(user=request.user).order_by('-created_at').first()
            if latest_quiz:
                latest_quiz.score = score
                latest_quiz.save()
                return JsonResponse({"message": "Score saved successfully!", "score": latest_quiz.score})
            else:
                return JsonResponse({"error": "No quiz found to update score"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request"}, status=400)