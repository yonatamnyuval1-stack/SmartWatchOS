import json
import os
import base64
import tempfile
import time
import ctypes
import threading
import urllib.request
import urllib.error
with open("key.txt", encoding="utf-8") as f:
    KEY = f.read().strip()
URL = "https://ai.hackclub.com/proxy/v1/replicate/models/vaibhavs10/incredibly-fast-whisper:c6433aab18b7318bbae316495f1a097fc067deef7d59dc2f33e45077ae5956c7/predictions"
winmm = ctypes.windll.winmm
winmm.mciSendStringW.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint, ctypes.c_void_p]

HEAR = os.path.join(tempfile.gettempdir(), "hear.wav")
def mic(command):
    return winmm.mciSendStringW(command,None,0,None)
def record():
    mic("close rec")
    if mic("open new type waveaudio alias rec") != 0:
        return False
    if mic("record rec") != 0:
        mic("close rec")
        return False
    time.sleep(4)
    mic("stop rec")
    if os.path.exists(HEAR):
        os.remove(HEAR)
    mic("save rec " + HEAR)
    mic("close rec")
    return True
def upload(path):
    audio = open(path, "rb").read()
    edge = "watchbound"
    body = ("--" + edge + "\r\n" + 'Content-Disposition: form-data; name="content"; filename="hear.wav"\r\n' + "Content-Type: audio/wav\r\n\r\n").encode()
    body = body + audio + ("\r\n--" + edge + "--\r\n").encode()
    req = urllib.request.Request(
        "https://ai.hackclub.com/proxy/v1/replicate/files",
        data=body,
        headers={
            "Authorization": "Bearer " + KEY,
            "Content-Type": "multipart/form-data; boundary=" + edge,
        },
    )
    with urllib.request.urlopen(req,timeout=30) as r:
        data = json.loads(r.read().decode())
    if "urls" in data and "get" in data["urls"]:
        return data["urls"]["get"]
    return data["url"]

def listen():
    if record() == False:
        return "no mic"
    try:
        audio = open(HEAR, "rb").read()
        audio_url = "data:audio/wav;base64," + base64.b64encode(audio).decode()
        body = json.dumps({
            "input": {
                "audio": audio_url,
                "task": "transcribe",
                "language": "None",
            },
        }).encode()
        req = urllib.request.Request(URL, data=body, headers={
            "Authorization": "Bearer " + KEY,
            "Content-Type": "Application/json",
            "Prefer": "wait",
        })
        with urllib.request.urlopen(req, timeout=90) as r:
            data = json.loads(r.read().decode())
        out = data["output"]
        if type(out) == str:
            return out
        if type(out) == dict and "text" in out:
            text = out["text"].strip()
            if text == "":
                return "nothing"
            return text
        return "no answer"
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return "Bad API key"
        return "no answer"
    except Exception:
        return "no internet"

def listen_later(done):
    def work():
        done(listen())
    threading.Thread(target=work, daemon=True).start()