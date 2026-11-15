import json
import threading
import urllib.request
import urllib.error
with open("deepl_key.txt", encoding="utf-8") as f:
    KEY = f.read().strip()
URL = "https://api-free.deepl.com/v2/translate"
LANG_URL = "https://api-free.deepl.com/v2/languages?type=target"
saved_langs = []
def translate(text, target):
    body = json.dumps({
        "text":[text],
        "target_lang": target,
    }).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "Content-Type": "application/json",
        "Authorization": "DeepL-Auth-Key " + KEY,
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode())
        return data["translations"][0]["text"]
    except urllib.error.HTTPError as e:
        if e.code == 403:
            return "Bad API key"
        if e.code == 456:
            return "limit reached"
        return "no translation"
    except Exception:
        return "no internet"
def translate_later(text, target, done):
    def work():
        done(translate(text, target))
    threading.Thread(target=work, daemon=True).start()
def languages():
    global saved_langs
    if saved_langs != []:
        return saved_langs
    req = urllib.request.Request(LANG_URL, headers={
        "Authorization": "DeepL-Auth-Key " + KEY,
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            saved_langs = json.loads(r.read().decode())
        return saved_langs
    except Exception:
        return []

def languages_later(done):
    def work():
        done(languages())
    threading.Thread(target=work,daemon=True).start()