import os
import requests

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from google import genai


def home(request):
    return render(request, "assistant.html")


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
            contents=prompt
        )

        return JsonResponse({"response": response.text})

    except Exception as error:
        print("Gemini API error:", repr(error), flush=True)
        return JsonResponse(
            {"error": str(error)},
            status=502
        )