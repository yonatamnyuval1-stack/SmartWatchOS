from tkinter import PhotoImage
TILE = 60
GAP = 6
WIDTH = 240
HEIGHT = 280
PAGER_H = 20
GRID_LEFT = (WIDTH - (TILE*3 + GAP*2)) // 2
items = ["hf", "openai", "gemini", "claude", "grok", "cursor", "ollama", "perplexity", "deepseek"]
logos = {}
def load_logos():
    if logos:
        return 
    for name in items:
        if name is None:
            continue
        logos[name] = PhotoImage(file="logos/" + name + ".png")
def show_screen(screen):
    load_logos()
    found = []
    top = 22
    for i in range(9):
        row = i //3
        col = i%3
        x = GRID_LEFT + col * (TILE+GAP)
        y = top +row * (TILE+GAP)
        screen.create_rectangle(x,y,x+TILE,y+TILE, outline="#f2f2f2", width=2)
        kind = items[i]
        if kind is None:
            continue
        screen.create_image(x + TILE//2, y + TILE//2, image=logos[kind])
        found.append((x,y,x+TILE,y+TILE,kind))
    screen.create_line(8, HEIGHT - PAGER_H, WIDTH-8, HEIGHT-PAGER_H, fill="#c8c2b4")
    mid = WIDTH //2
    ay = HEIGHT - PAGER_H // 2
    screen.create_line(
        mid-28, ay-4, mid, ay+4, mid+28, ay-4,
        fill="#f2f2f2", width=2, joinstyle="miter", capstyle="butt")
    return found