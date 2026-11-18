import json
import time
import threading
import urllib.request
state = "..."
percent = ""
left = ""
nozzle = ""
bed = ""
on_screen = False
started = False
WIDTH = 240
HEIGHT = 280
PAGER_H = 20
materials = [
    ("PLA", "210°","60°","on"),
    ("PETG","240°","80°","low"),
    ("TPU","225°","50°","low"),
    ("ABS","250°","100°","off"),
]
picked = ""
def read():
    global state, percent,left,nozzle,bed
    try:
        with open("printer.txt", encoding="utf-8") as f:
            address = f.read().strip()
    except Exception:
        state = "no address"
        return 
    url = address.rstrip("/") + "/printer/objects/query?print_stats&display_status&extruder&heater_bed"
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode())
    except Exception:
        state = "no printer"
        return 
    status = data["result"]["status"]
    stats = status["print_stats"]
    progress = status["display_status"]["progress"]
    state = stats["state"]
    percent = str(int(progress*100)) + "%"
    if progress > 0.01 and state == "printing":
        left_s = int(stats["print_duration"] * (1- progress)/ progress)
        left = str(left_s // 60) + "min"
    else:
        left = ""
    hot = status["extruder"]
    bed_now = status["heater_bed"]
    nozzle = str(int(hot["temperature"])) + "/" + str(int(hot["target"]))
    bed = str(int(bed_now["temperature"])) + "/" + str(int(bed_now["target"]))

def watch():
    global started
    if started:
        return 
    started = True
    def work():
        while True:
            if on_screen:
                read()
                time.sleep(3)
            else:
                time.sleep(1)
    threading.Thread(target=work, daemon=True).start()
def find(name):
    for item in materials:
        if item[0] == name:
            return item
    return None

def show_screen(screen):
    screen.create_text(20,36,text=state,anchor="w",fill="#f2f2f2",font=("Segoe UI",18))
    screen.create_text(20,80,text=percent + "  " + left,anchor="w",fill="#f2f2f2",font=("Segoe UI",16))
    screen.create_text(20,130,text="nozzle " + nozzle,anchor="w",fill="#f2f2f2",font=("Segoe UI",14))
    screen.create_text(20,170,text="bed " + bed,anchor="w",fill="#f2f2f2",font=("Segoe UI",14))
    screen.create_line(8, HEIGHT-PAGER_H,WIDTH-8,HEIGHT-PAGER_H,fill="#c8c2b4")
    mid = WIDTH // 2
    ay = HEIGHT-PAGER_H // 2
    screen.create_line(
        mid-28,ay-4,mid,ay+4,mid+28,ay-4,
        fill="#f2f2f2",width=2,joinstyle="miter",capstyle="butt"
    )
    return []