import base64
import json
import os
import tempfile
import threading
import urllib.request
import urllib.error
with open("key.txt", encoding="utf-8") as f:
    KEY = f.read().strip()
URL = "https://ai.hackclub.com/proxy/v1/chat/completions"
SHOT = os.path.join(tempfile.gettempdir(), "shot.png")
def make(text):
    body = json.dumps({
        "model": "google/gemini-2.5-flash-image",
        "messages": [{"role": "user", "content": text}],
        "modalities": ["image", "text"],
        "image_config": {"aspect_ratio": "1:1"},
    }).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "Authorization": "Bearer " + KEY,
        "Content-Type": "Application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            data = json.loads(r.read().decode())
        raw = data["choices"][0]["message"]["images"][0]["image_url"]["url"]
        if "," in raw:
            raw = raw.split(",")[1]
        with open(SHOT, "wb") as f:
            f.write(base64.b64decode(raw))
        return "ok"
    except urllib.request.HTTPError as e:
        if e.code == 401:
            return "Bad API key"
        return "no picture"
    except Exception:
        return "no internet"
def make_later(text, done):
    def work():
        done(make(text))
    threading.Thread(target=work, daemon=True).start()