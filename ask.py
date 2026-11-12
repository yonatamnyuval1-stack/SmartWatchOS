import json
import threading
import urllib.request
import urllib.error
with open("key.txt", encoding="utf-8") as f:
    KEY = f.read().strip()
URL = "https://ai.hackclub.com/proxy/v1/chat/completions"
models = {
    "openai": "openai/gpt-4o-mini",
    "gemini": "google/gemini-2.5-flash",
    "claude": "anthropic/claude-haiku-4.5",
    "grok": "x-ai/grok-4.5",
    "deepseek": "deepseek/deepseek-chat", 
}

def ask(model, question):
    body= json.dumps({
        "model": model,
        "max_tokens": 50,
        "messages": [{"role": "user", "content": question}],
    }) .encode()
    req = urllib.request.Request(URL, data=body, headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + KEY,
    })
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read().decode())
        return data["choices"][0]["message"]["content"].strip()
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return "Bad API key"
        return "no answer"
    except Exception:
        return "No internet"

def ask_later(model,question,done):
    def work():
        done(ask(model,question))
    threading.Thread(target=work,daemon=True).start()