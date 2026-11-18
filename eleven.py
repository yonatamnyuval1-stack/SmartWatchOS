import json
import wave
import winsound
import threading
import urllib.request
import urllib.error
with open("eleven_key.txt",encoding="utf-8") as f:
    KEY= f.read().strip()
VOICE = "21m00Tcm4TlvDq8ikWAM"
try:
    with open("voice.txt",encoding="utf-8") as f:
        found = f.read().strip()
    if found != "":
        VOICE=found
except Exception:
    pass

def speak(text):
    body = json.dumps({
        "text":text, 
        "model_id":"eleven_flash_v2_5",
    }).encode()
    url = "https://api.elevenlabs.io/v1/text-to-speech/" + VOICE + "?output_format=pcm_22050"
    req = urllib.request.Request(url, data=body, headers={
        "Content-Type": "application/json",
        "xi-api-key": KEY,
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            audio = r.read()
        winsound.PlaySound(None,winsound.SND_PURGE)
        with wave.open("say.wav","wb") as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(22050)
            f.writeframes(audio)
        winsound.PlaySound("say.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
        return "playing"
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return "Bad API"
        return "no voice"
    except Exception:
        return "no internet"
def speak_later(text,done):
    def work():
        done(speak(text))
    threading.Thread(target=work, daemon=True).start()