import json                                      # tool to read JSON text

from django.http import JsonResponse             # sends a JSON reply
from django.shortcuts import render              # fills a template and returns the page
from django.views.decorators.http import require_GET, require_POST   # limit which request types are allowed


@require_GET                                     # only allow GET (opening the page)
def chat_page(request):                          # runs when someone opens the home page
    return render(request, "chat.html")          # fill in chat.html and send it as HTML


@require_POST                                    # only allow POST (sending a question)
def chat_api(request):                           # runs when the page sends a question
    try:
        data = json.loads(request.body)          # read the JSON the browser sent
    except json.JSONDecodeError:                 # if it was not valid JSON...
        return JsonResponse({"error": 'Send JSON like {"question": "..."}'}, status=400)   # ...reply 400 = bad request

    if not isinstance(data, dict):               # JSON must be an object like {"a": 1}
        return JsonResponse({"error": "JSON must be an object"}, status=400)

    question = str(data.get("question", "")).strip()   # get the question text and trim spaces
    if not question:                             # empty question
        return JsonResponse({"error": "question is required"}, status=400)
    if len(question) > 2000:                     # too long
        return JsonResponse({"error": "question too long (max 2000 characters)"}, status=400)

    answer = f"(demo reply) You asked: {question}. Real answers arrive when we add the agents."
    return JsonResponse({"answer": answer, "sources": []})   # reply with an answer and an empty source list