import datetime
import ask
import deepl
import eleven
import picture
import whisper

WIDTH = 240
HEIGHT = 280
PAGER_H = 20
part = "menu"
typing = ""
page = 0
country = ""
clock = "24"
places = [
    ("United States", "sunday", "mdy"),
    ("Canada", "sunday", "mdy"),
    ("United Kingdom", "monday", "dmy"),
    ("France", "monday", "dmy"),
    ("Germany", "monday", "dmy"),
    ("Spain", "monday", "dmy"),
    ("Italy", "monday", "dmy"),
    ("Netherlands", "monday", "dmy"),
    ("India", "monday", "dmy"),
    ("Japan", "sunday", "ymd"),
    ("Australia", "monday", "dmy"),
    ("Israel", "sunday", "dmy"),
]
def read_file(name):
    try:
        with open(name, encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return ""

def write(name,text):
    with open(name, "w", encoding="utf-8") as f:
        return f.write(text)

def load():
    global country,clock
    country = read_file("country.txt")
    found = read_file("clock.txt")
    if found == "12":
        clock = "12"
    else:
        clock = "24"

def week_start():
    for row in places:
        if row[0] == country:
            return row[1]
    return "monday"

def two(n):
    if n < 10:
        return "0"+str(n)
    return str(n)

def hour(now):
    if clock != "12":
        return now.strftime("%H:%M")
    h = now.hour
    mark = "am"
    if h >= 12:
        mark = "pm"
    h = h %12
    if h == 0:
        h=12
    return str(h) + ":" + two(now.minute) + mark

def sample(order):
    now = datetime.datetime.now()
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    mon = months[now.month - 1]
    if order == "mdy":
        return mon + " " + str(now.day)
    if order == "ymd":
        return str(now.year) + " " + mon
    return str(now.day) + " " + mon

def cut(text,n):
    if text == "":
        return "none"
    if len(text) > n:
        return text[:n-1]+"."
    return text

def tail(text):
    if text == "":
        return "none"
    if len(text) <= 4:
        return text
    return text[-4:]

def voice_now():
    found = read_file("voice.txt")
    if found != "":
        return found
    return eleven.VOICE

def pick(name):
    global part,page,typing,clock,country
    if part == "menu" and name == "Clock":
        if clock == "24":
            clock = "12"
        else:
            clock = "24"
        write("clock.txt",clock)
        return
    if part == "menu" and name == "Printer":
        typing = "Printer"
        part = "type"
        return
    if part == "menu" and name == "Place":
        part = "place"
        page = 0
        return
    if part == "menu" and name == "Keys":
        part= "keys"
        return
    if part == "keys":
        typing = name
        part = "type"
        return
    if part == "place":
        country = name
        write("country.txt",name)
        part = "menu"
        return
def save_typed(text):
    global part
    if text != "":
        if typing == "Printer":
            write("printer.txt",text)
        elif typing == "Hackatime":
            write("hackatime_key.txt",text)
        elif typing == "Hack Club":
            write("key.txt",text)
            ask.KEY = text
            picture.KEY = text
            whisper.KEY= text
        elif typing == "Deepl":
            write("deepl_key.txt",text)
            deepl.KEY = text
        elif typing == "ElevenLabs":
            write("eleven_key.txt",text)
            eleven.KEY = text
        elif typing == "Voice":
            write("voice.txt",text)
            eleven.VOICE = text
    if typing == "Printer":
        part = "menu"
    else:
        part = "keys"

def back():
    global part,page
    if part == "place":
        if (page +1)*6 < len(places):
            page = page+1
            return "stay"
        else:
            part = "menu"
            page = 0
            return "stay"
    if part == "keys":
        part = "menu"
        return "stay"
    return "home"

def show_screen(screen):
    boxes = []
    if part == "menu":
        rows = [
            ("Place", cut(country,16)),
            ("Clock", clock+"h"),
            ("Printer",cut(read_file("printer.txt"),16)),
            ("Keys","")
        ]
        y = 36
        for label, value in rows:
            screen.create_text(16,y+18,text=label,anchor="w",fill="#f2f2f2",font=("Segoe UI",14))
            if value != "":
                color = "#c8c2b4"
                if value != None:
                    color = "#7ec8e3"
                screen.create_text(224,y+18,text=value,anchor="e",fill=color,font=("Segoe UI",12))
            screen.create_line(16,y+38,224,y+38,fill="#a2a2a2")
            boxes.append((0,y,WIDTH,y+46,label))
            y = y+50
    elif part == "keys":
        rows = [
            ("Hackatime", tail(read_file("hackatime_key.txt"))),
            ("Hack Club", tail(read_file("key.txt"))),
            ("Deepl", tail(read_file("deepl_key.txt"))),
            ("ElevenLabs",tail(read_file("eleven_key.txt"))),
            ("Voice", tail(voice_now())),
        ]
        y = 18
        for label,value in rows:
            color = "#c8c2b4"
            if value != "none":
                color = "#7ec8e3"
            screen.create_text(16, y + 16, text=label, anchor="w", fill="#f2f2f2", font=("Segoe UI", 13))
            screen.create_text(224, y + 16, text=value, anchor="e", fill=color, font=("Segoe UI", 12))
            screen.create_line(16, y + 34, 224, y + 34, fill="#2a2a2a")
            boxes.append((0, y, WIDTH, y + 40, label))
            y = y+44
    elif part == "place":
        start = page*6
        shown = places[start:start+6]
        i = 0
        for row in shown:
            y = 8+i*40
            color = "#f2f2f2"
            if row[0] == country:
                color = "#7ec8e3"
            screen.create_text(16,y+18,text=row[0],anchor="w",fill=color,font=("Segoe UI",13))
            screen.create_text(224, y + 18, text=sample(row[2]), anchor="e", fill=color, font=("Segoe UI", 11))
            boxes.append((0,y,WIDTH,y+40,row[0]))
            i = i+1
    elif part == "type":
        screen.create_text(120,42,text=typing,fill="#f2f2f2",font=("Segoe UI",16))
        if typing == "Printer":
            saved = read_file("printer.txt")
        elif typing == "Hackatime":
            saved = read_file("hackatime_key.txt")
        elif typing == "Hack Club":
            saved = read_file("key.txt")
        elif typing == "Deepl":
            saved = read_file("deepl_key.txt")
        elif typing == "ElevenLabs":
            saved = read_file("eleven_key.txt")
        else:
            saved = voice_now()
        screen.create_text(120,124,text="saved "+tail(saved),fill = "#c8c2b4",font=("Segoe UI",12))
    screen.create_line(8, HEIGHT-PAGER_H,WIDTH-8,HEIGHT-PAGER_H,fill="#c8c2b4")
    mid = WIDTH // 2
    ay = HEIGHT-PAGER_H // 2
    screen.create_line(
        mid-28,ay-4,mid,ay+4,mid+28,ay-4,
        fill="#f2f2f2", width=2, joinstyle="miter", capstyle="butt"
    )
    return boxes
load()