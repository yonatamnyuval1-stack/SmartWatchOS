import json
import base64
import threading
import urllib.request
import urllib.error
from datetime import datetime
WIDTH = 240
HEIGHT = 280
PAGER_H = 20
today = "..."
project = ""
language = ""

def clock(hours,minutes):
    if minutes < 10:
        minutes = "0" + str(minutes)
    else:
        minutes = str(minutes)
    return str(hours) + ":" + minutes

def biggest(rows):
    best = None
    for row in rows:
        if best == None or row["total_seconds"] > best["total_seconds"]:
            best = row
    if best == None:
        return ""
    return best["name"]

def load():
    global today,project,language
    try:
        with open("hackatime_key.txt",encoding="utf-8") as f:
            key = f.read().strip()
    except Exception:
        today = "no key"
        project = ""
        language = ""
        return
    day = datetime.now().strftime("%Y-%m-%d")
    url = "https://hackatime.hackclub.com/api/v1/users/current/summaries?start=" + day + "&end=" + day
    token = base64.b64encode((key + ":").encode()).decode()
    req = urllib.request.Request(url, headers={
        "Authorization": "Basic "+ token,
    })
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read().decode())
        one = data["data"][0]
        grand = one["grand_total"]
        today = clock(grand["hours"],grand["minutes"])
        project = biggest(one["projects"])
        language = biggest(one["languages"])
    except urllib.error.HTTPError as e:
        if e.code == 401:
            project= ""
            language=""
            today = "bad key"
        else:
            project = ""
            language = ""
            today = "no hours"
    except Exception:
        today = "no internet"
        project = ""
        language = ""

def load_later(done):
    def work():
        load()
        done()
    threading.Thread(target=work,daemon=True).start()

def show_screen(screen):
    screen.create_text(120,48,text="today",fill="#c8c2b4",font=("Segoe UI",12))
    screen.create_text(120,108,text=today,fill="#f2f2f2",font=("Segoe UI",32))
    screen.create_line(56,152,184,152,fill="#333333")
    if project != "":
        screen.create_text(120,182,text=project,width=200, justify="center",fill="#f2f2f2",font=("Segoe UI",14))
    if language != "":
        screen.create_text(120,214,text=language,fill="#c8c2b4",font=("Segoe UI",12))
    screen.create_line(8, HEIGHT-PAGER_H,WIDTH-8,HEIGHT-PAGER_H,fill="#c8c2b4")
    mid = WIDTH // 2
    ay = HEIGHT - PAGER_H // 2
    screen.create_line(
        mid-28,ay-4,mid,ay+4,mid+28,ay-4,
        fill="#f2f2f2",width=2,joinstyle="miter",capstyle="butt"
    )
    return []