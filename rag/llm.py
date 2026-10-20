import requests                          # tool for calling websites
from django.conf import settings         # gives us GROQ_API_KEY and GROQ_MODEL

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"   # Groq's chat address


class LLMError(Exception):               # our own error type: "the AI could not answer"
    """Raised when the AI service cannot give an answer."""


def ask_llm(question: str) -> str:       # takes a question, returns the answer text
    if not settings.GROQ_API_KEY:        # no key set?
        raise LLMError("GROQ_API_KEY is not set")   # stop with a clear reason

    payload = {                          # the request we send to Groq
        "model": settings.GROQ_MODEL,    # which model should answer
        "messages": [                    # the conversation so far
            {"role": "system", "content": "You are a helpful assistant. Answer clearly and briefly."},  # rules for the AI
            {"role": "user", "content": question},   # the user's question
        ],
        "temperature": 0.2,              # low = steady, less random
        "max_completion_tokens": 2048,   # maximum answer length (this model also "thinks", which uses some of it)
    }
    headers = {"Authorization": f"Bearer {settings.GROQ_API_KEY}"}   # show the key to prove who we are

    try:
        response = requests.post(GROQ_URL, json=payload, headers=headers, timeout=45)   # send it; give up after 45 s
        response.raise_for_status()      # turn HTTP errors (401, 400, 429...) into Python errors
        answer = response.json()["choices"][0]["message"]["content"]    # dig the answer text out of the reply
    except (requests.RequestException, KeyError, IndexError, ValueError) as error:
        raise LLMError(f"Groq call failed: {error}") from error   # any failure becomes our LLMError

    if not answer or not answer.strip(): # empty answer?
        raise LLMError("Groq returned an empty answer")
    return answer.strip()                # the answer, with extra spaces trimmed