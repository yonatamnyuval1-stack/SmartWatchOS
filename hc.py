import json
import threading
import urllib.request
import urllib.error
from datetime import datetime, timedelta
WIDTH = 240
HEIGHT = 280
PAGER_H = 20
today = "..."
week = "..."
projects = []

def clock(hours,minutes):
    if minutes < 10:
        minutes = "0" + str(minutes)
    else:
        minutes = str(minutes)
    return str(hours) + ":" + minutes

def short(seconds):
    minutes = int(seconds) // 60
    hours = minutes // 60
    minutes = minutes % 60
    if hours == 0:
        return str(minutes) + "m"
    return str(hours) + "h " + str(minutes) + "m"

def cut(name):
    if len(name) > 11:
        return name[:10] + "."
    return name

def by_time(rows):
    rows = list(rows)
    ordered = []
    while len(rows) > 0:
        best = rows[0]
        for row in rows:
            if row["total_seconds"] > best["total_seconds"]:
                best = row
        ordered.append(best)
        rows.remove(best)
    return ordered

def load():
    global today,week,projects
    try:
        with open("hackatime_key.txt",encoding="utf-8") as f:
            key = f.read().strip()
    except Exception:
        today = "no key"
        week = ""
        projects = []
        return
    now = datetime.now()
    monday = now - timedelta(days=now.weekday())
    end = now.strftime("%Y-%m-%d")
    start = monday.strftime("%Y-%m-%d")
    url = "https://hackatime.hackclub.com/api/hackatime/v1/users/current/summaries?start=" + start + "&end=" + end
    req = urllib.request.Request(url, headers={
        "Authorization": "Bearer " + key,
    })
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read().decode())
        grand = data["cumulative_total"]
        week = clock(grand["hours"],grand["minutes"])
        today = "0:00"
        found = None
        for day in data["data"]:
            if day["range"]["date"] == end:
                found = day
        projects = []
        if found != None:
            one = found["grand_total"]
            today = clock(one["hours"],one["minutes"])
            for row in by_time(found["projects"]):
                if row["total_seconds"] <= 0:
                    continue
                projects.append(row)
    except urllib.error.HTTPError as e:
        if e.code == 401:
            week = ""
            projects= []
            today = "bad key"
        else:
            week = ""
            projects = []
            today = "no hours"
    except Exception:
        today = "no internet"
        week = ""
        projects = []

def load_later(done):
    def work():
        load()
        done()
    threading.Thread(target=work,daemon=True).start()

def show_screen(screen):
    screen.create_text(16,36,text="today",anchor="w",fill="#c8c2b4",font=("Segoe UI", 13))
    screen.create_text(224,36,text=today,anchor="e",fill="#f2f2f2",font=("Segoe UI",16))
    screen.create_text(16,66,text="this week",anchor="w",fill="#c8c2b4",font=("Segoe UI",13))
    screen.create_text(224,66,text=week,anchor="e",fill="#f2f2f2",font=("Segoe UI",16))
    screen.create_line(16, 84, 224, 84, fill="#333333")
    y = 108
    most = 0
    if len(projects) > 0:
        most = projects[0]["total_seconds"]
    for row in projects[:5]:
        screen.create_text(14, y, text=cut(row["name"]), anchor="w", fill="#f2f2f2", font=("Segoe UI", 11))
        wide = 4
        if most > 0:
            wide = int(48*row["total_seconds"]/ most)
        if wide < 4:
            wide = 4
        screen.create_rectangle(112, y - 5, 112 + wide, y + 5, fill="#7ec8e3", outline="")
        screen.create_text(226, y, text=short(row["total_seconds"]), anchor="e", fill="#c8c2b4", font=("Segoe UI", 11))
        y = y+30

    mid = WIDTH // 2
    ay = HEIGHT - PAGER_H // 2
    screen.create_line(
        mid-28,ay-4,mid,ay+4,mid+28,ay-4,
        fill="#f2f2f2",width=2,joinstyle="miter",capstyle="butt"
    )
    return []