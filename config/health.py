from django.http import JsonResponse     # tool that replies with JSON

def health(request):                     # runs whenever someone visits /health/
    return JsonResponse({"status": "ok", "service": "ranker-rag"})
    # reply with {"status": "ok", ...}; Docker and AWS check for this