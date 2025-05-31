from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import requests
from .models import Consult, Question
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "mistral"

@csrf_exempt
@require_POST
@login_required
def advisor_chat(request):
    try:
        data = json.loads(request.body)
        user_input = data.get("question")

        if not user_input:
            return JsonResponse({"error": "Missing 'question' field."}, status=400)

        # Create a consult object for the user if not exists (optional logic)
        consult = Consult.objects.create(user=request.user)

        # پیام‌های مکالمه با نقش مشخص (برای context بیشتر)
        messages = [
            {"role": "system", "content": "You are a helpful academic advisor who recommends careers and university majors based on interests."},
            {"role": "user", "content": user_input}
        ]

        # ارسال درخواست به Ollama
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "messages": messages,
                "stream": False
            }
        )
        response.raise_for_status()
        result = response.json()

        # ذخیره پرسش و پاسخ در دیتابیس
        Question.objects.create(
            prompt=messages[1]["content"],
            question=user_input,
            answer=result["message"]["content"],
            next_prompt=""  # فعلاً خالی می‌گذاریم تا ساختار کامل‌تر شود
        )

        return JsonResponse({"response": result["message"]["content"]})

    except requests.RequestException as e:
        return JsonResponse({"error": "Failed to contact model.", "details": str(e)}, status=502)

    except Exception as e:
        return JsonResponse({"error": "Internal server error.", "details": str(e)}, status=500)
