import json
import logging                           # tool for writing log messages

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from rag.llm import LLMError, ask_llm    # our new AI helper (the rag folder is importable from the root)

logger = logging.getLogger(__name__)     # a logger named after this file


@require_GET
def chat_page(request):
    return render(request, "chat.html")


@require_POST
def chat_api(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": 'Send JSON like {"question": "..."}'}, status=400)

    if not isinstance(data, dict):
        return JsonResponse({"error": "JSON must be an object"}, status=400)

    question = str(data.get("question", "")).strip()
    if not question:
        return JsonResponse({"error": "question is required"}, status=400)
    if len(question) > 2000:
        return JsonResponse({"error": "question too long (max 2000 characters)"}, status=400)

    try:
        answer = ask_llm(question)       # ask Groq (this replaced the demo echo)
    except LLMError:                     # if the AI could not answer...
        logger.exception("LLM call failed")   # ...write the real reason to the logs
        return JsonResponse({"error": "The AI service is not available right now. Try again."}, status=502)   # 502 = upstream service failed

    return JsonResponse({"answer": answer, "sources": []})