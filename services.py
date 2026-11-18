from tkinter import PhotoImage
TILE = 60
GAP = 6
WIDTH = 240
HEIGHT = 280
PAGER_H = 20
GRID_LEFT = (WIDTH - (TILE*3 + GAP*2)) // 2
items = [
    ("YSWS", "https://hackclub.com/programs"),
    ("HCAI", "https://ai.hackclub.com"),
    ("Nest", "https://nest.hackclub.com"),
    None,
    None,
    None,
    None,
    None,
    None,
]
logos = {}

def load_logos():
    if logos:
        return
    for item in items:
        if item is None:
            continue
        name = item[0]
        logos[name] = PhotoImage(file="logos/" + name.lower() + ".png")

def address(name):
    for item in items:
        if item is None:
            continue
        if item[0] == name:
            return item[1]
    return ""

def show_screen(screen):
    load_logos()
    found = []
    top = 22
    for i in range(9):
        row = i // 3
        col = i % 3
        x = GRID_LEFT + col * (TILE+GAP)
        y = top + row * (TILE+GAP)
        screen.create_rectangle(x,y,x+TILE,y+TILE,outline = "#f2f2f2", width = 2)
        item = items[i]
        if item is None:
            continue
        name = item[0]
        cx = x+ TILE //2
        cy = y+ TILE //2
        screen.create_image(cx, cy, image=logos[name])
        found.append((x,y,x+TILE,y+TILE,name))
    screen.create_line(8, HEIGHT-PAGER_H, WIDTH-8, HEIGHT-PAGER_H, fill="#c8c2b4")
    mid = WIDTH // 2
    ay = HEIGHT - PAGER_H // 2
    screen.create_line(
        mid-28,ay-4,mid,ay+4,mid+28,ay-4,
        fill="#f2f2f2", width = 2, joinstyle="miter",capstyle= "butt"
    )
    return found