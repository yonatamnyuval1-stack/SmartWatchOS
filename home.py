import tkinter as tk
from datetime import datetime
import ai
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
def redraw():
    global boxes
    boxes = []
    screen.delete("all")
    if where == "ai":
        boxes = ai.show_screen(screen)
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
    
def on_click(event):
    global page,picked, where
    if where == "ai":
        if event.y >= HEIGHT-PAGER_H:
            where = "home"
            redraw()
        return
    if event.y >= HEIGHT-PAGER_H:
        page = 1 - page
        picked = ""
        redraw()
        return
    for x1,y1,x2,y2,name in boxes:
        if x1 <= event.x <= x2 and y1 <= event.y <= y2:
            if name == "AI":
                where = "ai"
                picked = ""
                redraw()
                return
            picked = name
            redraw()
            return 

def tick():
    redraw()
    root.after(1000, tick)
screen.bind("<Button-1>", on_click)
tick()
root.mainloop()