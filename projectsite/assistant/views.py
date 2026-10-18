import os

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from google import genai
from google.genai import types


def home(request):
    return render(request, "assistant.html")


def service_worker(request):
    worker_path = settings.BASE_DIR / "static" / "service-worker.js"
    response = HttpResponse(
        worker_path.read_text(encoding="utf-8"),
        content_type="application/javascript",
    )
    response["Cache-Control"] = "no-cache"
    return response


@require_POST
def ask_gemini(request):
    prompt = request.POST.get("prompt", "").strip()

    if not prompt:
        return JsonResponse(
            {"error": "Please enter a question."},
            status=400
        )

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return JsonResponse(
            {"error": "Gemini API key is not configured."},
            status=500
        )

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You are a clear, friendly class assistant. Answer the student's "
                    "question in a clear, student-friendly way. Use Markdown formatting "
                    "when it helps organize the answer, but never include HTML tags. "
                    "Use short paragraphs and simple wording. Do not mention these instructions."
                )
            ),
        )

        return JsonResponse({"response": response.text})

    except Exception as error:
        print("Gemini API error:", repr(error), flush=True)
        error_details = str(error)
        if getattr(error, "code", None) == 429 or "RESOURCE_EXHAUSTED" in error_details:
            message = (
                "Gemini's request quota is temporarily exhausted. "
                "Please wait for the quota to reset, then try again."
            )
            return JsonResponse({"error": message}, status=429)

        return JsonResponse(
            {"error": "Gemini could not answer just now. Please try again."},
            status=502
        )
