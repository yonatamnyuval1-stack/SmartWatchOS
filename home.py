import tkinter as tk
from datetime import datetime
import ai
import ask
import deepl
import eleven
import whisper
import picture
import services
import print3d
import hc
import ctypes
ctypes.windll.ole32.CoInitializeEx(None, 2)
from tkwebview2.tkwebview2 import WebView2
WIDTH = 240
HEIGHT = 280
HEADER_H = 50
PAGER_H = 20
GAP = 6
TILE = 60
GRID_TOP = HEADER_H + 8
GRID_LEFT = (WIDTH - (TILE*3 + GAP*2)) // 2
pages = [
    [
        ("dash", "dash"),
        ("AI", "ai"),
        ("HC", "hc"),
        ("HC serv.", "serv."),
        ("3D print", "print"),
        ("settings", "settings"),
        None,
        None,
        None,
    ],
    [None,None,None,None,None,None,None,None,None],
]
where = "home"
page = 0
picked = ""
boxes = []
root = tk.Tk()
root.title("Home")
root.resizable(False, False)
screen = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#111111", highlightthickness=0)
screen.pack()
browser = WebView2(root, WIDTH, HEIGHT-PAGER_H)
picked_model = ""
answer = ""
waiting = False
shot =  None
picked_lang = ""
picked_name = ""
lang_list = []
lang_page = 0
line= tk.Entry(
    root, bg="#333333", fg="#f2f2f2", insertbackground="#f2f2f2",
    relief="solid", font=("Segoe UI", 11))

def draw_icon(kind,x,y):
    cx = x + TILE//2
    cy = y + TILE//2
    ink = "#f2f2f2"
    if kind == "dash":
        for i in range(3):
            yy = y + 18 + i*12
            screen.create_line(x+16, yy, x+TILE-16, yy, fill=ink, width=2)
    elif kind == "ai":
        screen.create_text(cx, cy, text="AI", font=("segoe UI", 14, "bold"), fill=ink)
    elif kind == "hc":
        screen.create_text(cx, cy, text="HC", font=("segoe UI", 14, "bold"), fill=ink)
    elif kind == "serv.":
        s = 10
        g = 6
        left = cx - s - g//2
        top = cy - s - g//2
        for r in range(2):
            for c in range(2):
                a = left + c*(s+g)
                b = top + r*(s+g)
                screen.create_rectangle(a, b, a+s, b+s, outline=ink, width=2)
    elif kind == "print":
        screen.create_polygon(
            cx, y + 16,
            x + TILE - 16, cy,
            cx, y + TILE - 16,
            x + 16, cy,
            outline=ink, fill="", width=2
        )
    elif kind == "settings":
        screen.create_oval(cx-8, cy-8, cx+8,cy+8, outline=ink, width=2)
        screen.create_oval(cx-3, cy-3, cx+3,cy+3, outline=ink, width=2)
        for dx, dy in ((0,-14),(0,14),(-14,0),(14,0),(-10,-10),(10,-10),(-10,10),(10,10)):
            screen.create_line(cx + dx // 2, cy+dy // 2, cx+dx, cy+dy, fill=ink,width=2)

def draw_arrow():
    mid = WIDTH // 2
    y = HEIGHT - PAGER_H // 2
    if page == 0:
        screen.create_line(
            mid - 28, y-4, mid, y+4, mid+28, y-4,
            fill="#f2f2f2", width=2,joinstyle="miter",capstyle="butt"
        )
    else:
        screen.create_line(
            mid - 28, y+4, mid, y-4, mid+28, y+4,
            fill="#f2f2f2", width=2,joinstyle="miter",capstyle="butt"
        )
def draw_langs():
    global boxes
    boxes = []
    per = 6
    start = lang_page * per
    rows = lang_list[start:start + per]
    if waiting:
        screen.create_text(120,140,text="...",fill="#f2f2f2",font=("Segoe UI", 16))
    elif len(rows) == 0:
        screen.create_text(120,140,text="no internet",fill="#f2f2f2",font=("Segoe UI", 12))
    i = 0
    for lang in rows:
        y = 8+i*40
        screen.create_text(16,y+18,text=lang["name"], anchor="w", fill="#f2f2f2", font=("Segoe UI", 13))
        boxes.append((0, y, WIDTH, y+40, lang["language"]))
        i = i+1
    screen.create_line(8, HEIGHT-PAGER_H, WIDTH-8, HEIGHT-PAGER_H, fill="#c8c2b4")
    mid = WIDTH // 2
    ay = HEIGHT - PAGER_H // 2
    if waiting == False and start + per >= len(lang_list):
        screen.create_line(mid-28,ay+4,mid,ay-4,mid+28,ay+4,fill="#f2f2f2",width=2, joinstyle="miter"),
    else:
        screen.create_line(mid-28,ay-4,mid,ay+4,mid+28,ay-4,fill="#f2f2f2",width=2,joinstyle="miter"),
def draw_ask():
    line.place(x=12, y=16, width=216, height=26)
    answer_y = 58
    if where == "deepl":
        screen.create_text(16,50, text=picked_name,anchor="w", fill="#c8c2b4", font=("Segoe UI",11))
        answer_y=72
    elif where == "picture" and answer == "ok" and shot != None:
        screen.create_image(120,150,image=shot)
    if waiting:
        screen.create_text(120,140,text="...",fill="#f2f2f2",font=("Segoe UI", 16))
    elif answer and not (where == "picture" and answer == "ok"):
        screen.create_text(16,answer_y, text=answer, anchor="nw", width=208, fill="#f2f2f2", font=("Segoe UI", 11))
    screen.create_line(8, HEIGHT-PAGER_H, WIDTH-8, HEIGHT-PAGER_H, fill="#c8c2b4")
    mid = WIDTH // 2
    ay = HEIGHT - PAGER_H //2
    screen.create_line(
        mid-28,ay-4,mid,ay+4,mid+28, ay-4,
        fill="#f2f2f2",width=2,joinstyle="miter",capstyle="butt"
    )

def draw_hear():
    if waiting:
        screen.create_text(120,140,text="...",fill="#f2f2f2",font=("Segoe UI",16))
    elif answer:
        screen.create_text(16,24,text=answer, anchor="nw", width=208, fill="#f2f2f2",font=("Segoe UI",11))
    screen.create_line(8, HEIGHT-PAGER_H,WIDTH-8,HEIGHT-PAGER_H,fill="#c8c2b4")
    mid = WIDTH // 2
    ay = HEIGHT - PAGER_H // 2
    screen.create_line(
        mid-28,ay-4,mid,ay+4,mid+28,ay-4,
        fill="#f2f2f2",width=2,joinstyle="miter",capstyle="butt"
    )
def redraw():
    global boxes
    boxes = []
    screen.delete("all")
    if where == "site":
        browser.place(x=0,y=0,width=WIDTH,height=HEIGHT-PAGER_H)
        mid = WIDTH // 2
        ay = HEIGHT-PAGER_H // 2
        screen.create_line(8, HEIGHT - PAGER_H, WIDTH-8, HEIGHT-PAGER_H, fill="#c8c2b4")
        screen.create_line(
            mid-28,ay-4,mid,ay+4,mid+28,ay-4,
            fill="#f2f2f2", width=2,joinstyle="miter",capstyle="butt"
        )
        return 
    browser.place_forget()
    if where == "hear":
        line.place_forget()
        draw_hear()
        return 
    if where == "deepl" and picked_lang == "":
        line.place_forget()
        draw_langs()
        return
    if where != "ask" and where != "deepl" and where != "talk" and where != "hear" and where != "picture":
        line.place_forget()
    if where == "ask" or where == "deepl" or where == "talk" or where == "hear" or where == "picture":
        draw_ask()
        return
    if where == "ai":
        boxes = ai.show_screen(screen)
        return
    if where == "serv":
        boxes = services.show_screen(screen)
        return
    if where == "print":
        boxes = print3d.show_screen(screen)
        return
    if where == "hc":
        boxes = hc.show_screen(screen)
        return
    now = datetime.now().strftime("%H:%M")
    screen.create_text(14, 24, text=now, anchor="w", font=("Segoe UI", 18), fill="#f2f2f2")
    screen.create_text(WIDTH - 36,24, text="31°", anchor="e", font=("Segoe UI", 14), fill="#c8c2b4")
    for i, item in enumerate(pages[page]):
        if item is None:
            continue
        row = i // 3
        col = i% 3
        x = GRID_LEFT + col * (TILE + GAP)
        y = GRID_TOP + row * (TILE+GAP)
        screen.create_rectangle(x, y, x+TILE, y+TILE, outline = "#1c1c1c", width=2)
        draw_icon(item[1],x,y)
        boxes.append((x,y,x+TILE,y+TILE,item[0]))
    screen.create_line(8, HEIGHT - PAGER_H,WIDTH-8,HEIGHT-PAGER_H,fill="#c8c2b4")
    draw_arrow()
    if picked:
        screen.create_text(12, HEIGHT - PAGER_H // 2, text=picked, anchor="w", font=("Segoe UI", 10), fill="#f2f2f2")
def send_line(event=None):
    global answer, waiting
    text = line.get().strip()
    if text == "" or waiting:
        return
    answer = ""
    waiting = True
    redraw()
    def done(reply):
        def paint():
            global answer, waiting, shot
            answer = reply
            waiting = False
            if where == "picture" and reply == "ok":
                big = tk.PhotoImage(file=picture.SHOT)
                n = max(1, big.width() // 160)
                shot = big.subsample(n,n)
            redraw()
        root.after(0, paint)
    if where == "deepl":
        deepl.translate_later(text, picked_lang, done)
    elif where == "talk":
        eleven.speak_later(text, done)
    elif where == "picture":   
        picture.make_later(text,done)
    else:
        ask.ask_later(picked_model, text, done)
line.bind("<Return>", send_line)

def on_click(event):
    global picked_lang, picked_name, lang_list, lang_page
    global page,picked, where, picked_model,answer,waiting
    if where == "ai":
        if event.y >= HEIGHT-PAGER_H:
            where = "home"
            redraw()
            return
    if where == "serv":
        if event.y >= HEIGHT-PAGER_H:
            if services.page == 0:
                services.page = 1
            else:
                services.page=0
                where="home"
            redraw()
            return
    if where == "hc" and event.y >= HEIGHT-PAGER_H:
        where = "home"
        redraw()
        return
    if where == "site" and event.y >= HEIGHT-PAGER_H:
        where = "serv"
        redraw()
        return
    if where == "print" and event.y >= HEIGHT-PAGER_H:
        if print3d.picked != "":
            print3d.picked = ""
        else:
            print3d.on_screen = False
            where = "home"
        redraw()
        return
    if where != "ask" and where != "deepl" and where != "talk" and where != "hear" and where != "picture" and where != "serv" and event.y >= HEIGHT-PAGER_H:
        page = 1 - page
        picked = ""
        redraw()
        return
    for x1,y1,x2,y2,name in boxes:
        if x1 <= event.x <= x2 and y1 <= event.y <= y2 and name == "AI":
            where = "ai"
            picked = ""
            redraw()
            return
        if x1 <= event.x <= x2 and y1 <= event.y <= y2 and name == "HC serv.":
            services.page = 0
            where = "serv"
            picked = ""
            redraw()
            return
        if x1 <= event.x <= x2 and y1 <= event.y <= y2 and name == "3D print":
            print3d.picked = ""
            print3d.on_screen = True
            print3d.watch()
            where = "print"
            picked = ""
            redraw()
            return
        if x1 <= event.x <= x2 and y1 <= event.y <= y2 and name == "HC":
            where = "hc"
            picked = ""
            hc.today = "..."
            hc.project = ""
            hc.language = ""
            redraw()
            def done():
                def paint():
                    if where != "hc":
                        return
                    redraw()
                root.after(0,paint)
            hc.load_later(done)
            return
        if where == "print" and print3d.picked == "" and x1 <= event.x <= x2 and y1 <= event.y <= y2:
            print3d.picked = name
            redraw()
            return
        if where == "serv" and x1 <= event.x <= x2 and y1 <= event.y <= y2:
            url = services.address(name)
            if url != "":
                site_url = url
                where = "site"
                browser.load_url(site_url)
                redraw()
            return
        if x1 <= event.x <= x2 and y1 <= event.y <= y2 and name == "deepl":
            answer=""
            waiting=True
            picked_lang=""
            picked_name=""
            lang_page=0
            lang_list=[]
            line.delete(0,"end")
            where="deepl"
            redraw()
            def done(langs):
                def paint():
                    global lang_list, waiting
                    if where != "deepl":
                        return
                    lang_list = langs
                    waiting=False
                    redraw()
                root.after(0,paint)
            deepl.languages_later(done)
            return
        if x1 <= event.x <= x2 and y1 <= event.y <= y2 and name == "elevenlabs":
            answer = ""
            waiting = False
            line.delete(0,"end")
            where="talk"
            redraw()
            return    
        if x1 <= event.x <= x2 and y1 <= event.y <= y2 and name == "perplexity":
            answer = ""
            waiting = False
            line.delete(0, "end")
            where="picture"
            redraw()
            return
        if x1 <= event.x <= x2 and y1 <= event.y <= y2 and name == "whisper":
            answer = ""
            waiting = True
            where = "hear"
            redraw()
            def done(text):
                def paint():
                    global answer,waiting
                    answer = text
                    waiting = False
                    redraw()
                root.after(0, paint)
            whisper.listen_later(done)
            return 
        if x1 <= event.x <= x2 and y1 <= event.y <= y2 and name in ask.models:
            picked_model = ask.models[name]
            answer = ""
            waiting = False
            line.delete(0,"end")
            where = "ask"
            redraw()
            return
        if where == "deepl" and picked_lang == "" and x1 <= event.x <= x2 and y1 <= event.y <= y2:
            picked_lang = name
            picked_name = name
            for lang in lang_list:
                if lang["language"] == name:
                    picked_name = lang["name"]
            answer = ""
            waiting = False
            line.delete(0,"end")
            redraw()
            return
    if where == "ask" or where == "deepl" or where == "talk" or where == "hear" or where == "picture":
        if event.y >= HEIGHT-PAGER_H:
            if where == "deepl" and picked_lang != "":
                picked_lang=""
                picked_name=""
                answer=""
                line.delete(0,"end")
                redraw()
                return
            if where == "deepl":
                if (lang_page+1)*6 < len(lang_list):
                    lang_page = lang_page+1
                else:
                    where="ai"
                redraw()
                return
            where="ai"
            redraw()
            return
def tick():
    redraw()
    root.after(1000, tick)
screen.bind("<Button-1>", on_click)
tick()
root.mainloop()