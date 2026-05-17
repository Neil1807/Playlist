import tkinter as tk
import math
import pygame
import os

pygame.mixer.init()

root = tk.Tk()
root.title("🎵 Record Player")
root.geometry("420x520")
root.resizable(False, False)
root.configure(bg="#2c1a00")

cd_canvas = tk.Canvas(root, width=400, height=370, bg="#2c1a00", highlightthickness=0)
cd_canvas.pack(padx=10, pady=(10, 0))

spin_angle = 0
is_playing = False
song_pos = 0.0
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

songs_names = [
    "Iris - Goo Goo Dolls",
    "Labyu - Frank Ely",
    "Our Song - Taylor Swift",
    "Valentine - Laufey",
    "Every Breath You Take - The Police",
    "Yellow - Coldplay",
    "One and Only - Adele",
    "Until You - Shayne Ward",
]

songs = [
    os.path.join(BASE_DIR, "Iris.mp3"),
    os.path.join(BASE_DIR, "Labyu.mp3"),
    os.path.join(BASE_DIR, "Our Song.mp3"),
    os.path.join(BASE_DIR, "Valentine.mp3"),
    os.path.join(BASE_DIR, "Every Breath You Take.mp3"),
    os.path.join(BASE_DIR, "Yellow.mp3"),
    os.path.join(BASE_DIR, "One and Only.mp3"),
    os.path.join(BASE_DIR, "Until You.mp3"),
]
current_index = 0

def draw_cd(angle):
    cd_canvas.delete("all")
    cx, cy = 165, 185
    rx, ry = 118, 42
    depth = 16

    # ── Cabinet shadow ───────────────────────────────────────────
    cd_canvas.create_oval(25, 275, 375, 310, fill="#1a0a00", outline="")

    # ── Cabinet 3D bottom edge ───────────────────────────────────
    cd_canvas.create_arc(15, 265, 365, 305, start=180, extent=180,
                          fill="#5a3205", outline="#3a1a00", width=1, style="chord")
    cd_canvas.create_rectangle(15, 275, 365, 288, fill="#5a3205", outline="")

    # ── Cabinet body ─────────────────────────────────────────────
    cd_canvas.create_rectangle(15, 88, 365, 278,
                                fill="#f0b050", outline="#c8782a", width=2)

    # rounded corners
    for ox, oy in [(15,88),(345,88),(15,258),(345,258)]:
        cd_canvas.create_oval(ox-10, oy-10, ox+10, oy+10,
                               fill="#f0b050", outline="#c8782a", width=2)

    # ── Wood grain ───────────────────────────────────────────────
    for i in range(22):
        y = 96 + i * 8
        w1 = math.sin(i * 0.9 + 0.5) * 5
        w2 = math.sin(i * 1.2) * 4
        cd_canvas.create_line(15, y+w1, 365, y+w2, fill="#e0a040", width=1)

    # ── Top rim highlight ────────────────────────────────────────
    cd_canvas.create_line(20, 90, 360, 90, fill="#ffe090", width=2)
    cd_canvas.create_line(20, 94, 360, 94, fill="#f8c860", width=1)

    # ── Blush cheeks ─────────────────────────────────────────────
    cd_canvas.create_oval(18, 225, 52, 245, fill="#f07848", outline="", stipple="gray50")
    cd_canvas.create_oval(270, 225, 304, 245, fill="#f07848", outline="", stipple="gray50")

    # ── LED panel ────────────────────────────────────────────────
    cd_canvas.create_rectangle(244, 100, 360, 152,
                                fill="#0e0e00", outline="#f0b030", width=2)
    cd_canvas.create_rectangle(248, 104, 358, 148,
                                fill="#0a1200", outline="#1a2200", width=1)

    status = "► PLAY" if is_playing else "■ PAUSE"
    cd_canvas.create_text(298, 116, text=status,
                           fill="#aaff44" if is_playing else "#446622",
                           font=("Courier", 8, "bold"))

    # song name on LED (truncated)
    short_name = songs_names[current_index][:14]
    cd_canvas.create_text(298, 128, text=short_name,
                           fill="#88cc22" if is_playing else "#335511",
                           font=("Courier", 6))

    # bouncing bars
    for b in range(7):
        bar_h = (math.sin(math.radians(angle * 3 + b * 40)) * 6 + 8) if is_playing else 2
        cd_canvas.create_rectangle(254+b*15, 146-bar_h, 262+b*15, 147,
                                    fill="#aaff44" if is_playing else "#1a3300",
                                    outline="")

    # ── Sparkles ─────────────────────────────────────────────────
    for sx, sy, ss in [(232,103,6),(235,118,4),(228,132,5)]:
        cd_canvas.create_text(sx, sy, text="✦", fill="#ffd580", font=("Arial", ss))

    # ── Platter well ─────────────────────────────────────────────
    cd_canvas.create_oval(cx-rx-8, cy-ry-2, cx+rx+8, cy+ry+2+depth,
                           fill="#1e1000", outline="#0e0800")
    cd_canvas.create_oval(cx-rx-8, cy-ry-2, cx+rx+8, cy+ry+2,
                           fill="#2a1800", outline="#c8782a", width=2)

    # ── Felt mat ─────────────────────────────────────────────────
    cd_canvas.create_oval(cx-rx+2, cy-ry+2, cx+rx-2, cy+ry-2+depth//2,
                           fill="#150f00", outline="")
    cd_canvas.create_oval(cx-rx+2, cy-ry+2, cx+rx-2, cy+ry-2,
                           fill="#2a1c00", outline="#3a2810", width=1)

    # ── Platter rim ──────────────────────────────────────────────
    cd_canvas.create_oval(cx-rx, cy-ry+depth//2, cx+rx, cy+ry+depth//2,
                           fill="#1a1000", outline="#2a1800")
    cd_canvas.create_oval(cx-rx, cy-ry, cx+rx, cy+ry,
                           fill="#0e0900", outline="#3a2810", width=2)

    # ── Vinyl grooves ─────────────────────────────────────────────
    for i in range(14):
        gr = 0.95 - i * 0.052
        if gr < 0.28:
            break
        v = 20 + i * 4
        h = v // 3
        cd_canvas.create_oval(cx-rx*gr, cy-ry*gr, cx+rx*gr, cy+ry*gr,
                               outline=f"#{hex(v)[2:].zfill(2)}{hex(h)[2:].zfill(2)}00",
                               width=1)

    # ── Sheen ────────────────────────────────────────────────────
    for i in range(6):
        a = math.radians(angle + i * 60)
        x1 = cx + (rx-5) * math.cos(a)
        y1 = cy + (ry-2) * math.sin(a)
        x2 = cx + (rx-22) * math.cos(a+0.2)
        y2 = cy + (ry-7) * math.sin(a+0.2)
        cd_canvas.create_line(x1, y1, x2, y2, fill="#2a1c00", width=1)

    # ── Matrix ring + label ──────────────────────────────────────
    cd_canvas.create_oval(cx-40, cy-14, cx+40, cy+14,
                           fill="#0a0700", outline="#1e1600")
    cd_canvas.create_oval(cx-31, cy-11, cx+31, cy+11,
                           fill="#d06828", outline="#904018", width=1)
    cd_canvas.create_oval(cx-24, cy-8, cx+24, cy+8,
                           outline="#e07838", width=1, fill="")
    cd_canvas.create_text(cx, cy, text="♫", fill="#fff0cc",
                           font=("Arial", 9, "bold"))

    # ── Spindle ──────────────────────────────────────────────────
    cd_canvas.create_oval(cx-5, cy+1, cx+5, cy+6, fill="#906000", outline="#b08020")
    cd_canvas.create_oval(cx-5, cy-3, cx+5, cy+2, fill="#ffd050", outline="#ffe880")
    cd_canvas.create_oval(cx-2, cy-2, cx+2, cy+1, fill="#fffadd", outline="")

    # ── Tonearm pivot ────────────────────────────────────────────
    cd_canvas.create_oval(328, 75, 354, 85, fill="#8a6000", outline="#c09020")
    cd_canvas.create_oval(328, 70, 354, 80, fill="#f0c030", outline="#ffd050", width=2)
    cd_canvas.create_oval(337, 72, 345, 78, fill="#fffadd", outline="")

    # ── Tonearm ──────────────────────────────────────────────────
    arm_angle = math.radians(-200 if is_playing else -170)
    arm_len = 180
    pivot_x, pivot_y = 320, 85

    tip_x  = pivot_x + arm_len * math.cos(arm_angle)
    tip_y  = pivot_y + arm_len * math.sin(arm_angle)
    back_x = pivot_x - 26 * math.cos(arm_angle)
    back_y = pivot_y - 26 * math.sin(arm_angle)

    cd_canvas.create_line(pivot_x+3, pivot_y+4, tip_x+3, tip_y+4,
                           fill="#1a0e00", width=5)
    cd_canvas.create_line(pivot_x, pivot_y, tip_x, tip_y, fill="#d4a030", width=4)
    cd_canvas.create_line(pivot_x, pivot_y-1, tip_x, tip_y-1, fill="#ffe880", width=1)

    hs_angle = arm_angle + math.radians(15)
    hx = tip_x + 18 * math.cos(hs_angle)
    hy = tip_y + 18 * math.sin(hs_angle)
    cd_canvas.create_line(tip_x, tip_y, hx, hy, fill="#f0c030", width=5)
    cd_canvas.create_rectangle(hx-5, hy-3, hx+5, hy+5, fill="#6a4400", outline="#f0c030")
    cd_canvas.create_line(hx, hy+5, hx+1, hy+10, fill="#ffd060", width=1)

    cd_canvas.create_oval(back_x-8, back_y+2, back_x+8, back_y+8,
                           fill="#7a5000", outline="#a07010")
    cd_canvas.create_oval(back_x-8, back_y-4, back_x+8, back_y+3,
                           fill="#e0b030", outline="#ffd050")
    cd_canvas.create_oval(back_x-3, back_y-2, back_x+3, back_y+1,
                           fill="#fffadd", outline="")

    # ── Knobs ────────────────────────────────────────────────────
    knob_labels = ["SPD", "TONE", "VOL", "EQ"]
    knob_colors = ["#f07030","#e8a030","#50c878","#6090f0"]
    for i, kx in enumerate([38, 78, 165, 205]):
        cd_canvas.create_oval(kx-12, 258, kx+12, 278, fill="#2a1400", outline="")
        cd_canvas.create_oval(kx-12, 254, kx+12, 274,
                               fill=knob_colors[i], outline="#fff0cc", width=1)
        cd_canvas.create_oval(kx-6, 256, kx, 262, fill="#ffffff", outline="", stipple="gray75")
        cd_canvas.create_oval(kx-2, 256, kx+2, 260, fill="#1a0e00", outline="")
        cd_canvas.create_text(kx, 280, text=knob_labels[i],
                               fill="#7a4a10", font=("Courier", 6, "bold"))

    # ── Hinges ───────────────────────────────────────────────────
    for hx in [90, 190, 290]:
        cd_canvas.create_rectangle(hx-8, 86, hx+8, 94,
                                    fill="#f0c030", outline="#c89020", width=1)
        cd_canvas.create_oval(hx-3, 88, hx+3, 93, fill="#fffadd", outline="")

    # ── Feet ─────────────────────────────────────────────────────
    for fx in [38, 342]:
        cd_canvas.create_oval(fx-13, 284, fx+13, 298, fill="#1a0e00", outline="#2a1800")
        cd_canvas.create_oval(fx-13, 280, fx+13, 294,
                               fill="#5a3810", outline="#c8782a", width=1)
        cd_canvas.create_oval(fx-6, 282, fx, 287, fill="#a06030", outline="")

    # ── Floating notes ───────────────────────────────────────────
    if is_playing:
        for i, (nx, ny) in enumerate([(22,145),(355,160),(24,178)]):
            drift = math.sin(math.radians(angle * 2 + i * 120)) * 4
            cd_canvas.create_text(nx, ny+drift, text="♪",
                                   fill="#ffd580", font=("Arial", 10+i%3))

# ── Progress bar update ───────────────────────────────────────────
def update_progress():
    if is_playing:
        pos = pygame.mixer.music.get_pos() / 1000.0
        progress_var.set(pos % 100)
    root.after(500, update_progress)

def spin_loop():
    global spin_angle
    if is_playing:
        spin_angle = (spin_angle + 3) % 360
    draw_cd(spin_angle)
    root.after(40, spin_loop)

def toggle_play():
    global is_playing
    is_playing = not is_playing
    btn_play.config(text="⏸" if is_playing else "▶")
    if is_playing:
        pygame.mixer.music.load(songs[current_index])
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.pause()

def prev_song():
    global current_index
    current_index = (current_index - 1) % len(songs)
    lbl_song.config(text=songs_names[current_index])
    progress_var.set(0)
    if is_playing:
        pygame.mixer.music.load(songs[current_index])
        pygame.mixer.music.play()
    draw_cd(spin_angle)

def next_song():
    global current_index
    current_index = (current_index + 1) % len(songs)
    lbl_song.config(text=songs_names[current_index])
    progress_var.set(0)
    if is_playing:
        pygame.mixer.music.load(songs[current_index])
        pygame.mixer.music.play()
    draw_cd(spin_angle)

spin_loop()
update_progress()

# ── Song name ─────────────────────────────────────────────────────
lbl_song = tk.Label(root, text=songs_names[current_index],
                    bg="#2c1a00", fg="#ffd580",
                    font=("Courier New", 10, "bold"))
lbl_song.pack(pady=(4, 2))

# ── Progress bar ──────────────────────────────────────────────────
progress_var = tk.DoubleVar()
progress_frame = tk.Frame(root, bg="#2c1a00")
progress_frame.pack(fill="x", padx=30, pady=(0, 6))

tk.Label(progress_frame, text="♩", bg="#2c1a00",
         fg="#f0b030", font=("Arial", 9)).pack(side="left")

progress_bar = tk.Scale(progress_frame, variable=progress_var,
                         from_=0, to=100, orient="horizontal",
                         bg="#2c1a00", fg="#ffd580",
                         troughcolor="#5a3205",
                         activebackground="#f0c030",
                         highlightthickness=0, sliderrelief="flat",
                         sliderlength=12, width=6,
                         showvalue=False, length=300)
progress_bar.pack(side="left", fill="x", expand=True)

tk.Label(progress_frame, text="♩", bg="#2c1a00",
         fg="#f0b030", font=("Arial", 9)).pack(side="left")

# ── Controls row (prev + play + next together) ────────────────────
ctrl_frame = tk.Frame(root, bg="#2c1a00")
ctrl_frame.pack(pady=(0, 10))

btn_prev = tk.Button(ctrl_frame, text="⏮", command=prev_song,
                     bg="#c8782a", fg="#fff0cc",
                     font=("Courier New", 14, "bold"),
                     relief="flat", padx=12, pady=6,
                     cursor="hand2", activebackground="#e8a030")
btn_prev.pack(side="left", padx=4)

btn_play = tk.Button(ctrl_frame, text="▶", command=toggle_play,
                     bg="#f0c030", fg="#1a0e00",
                     font=("Courier New", 14, "bold"),
                     relief="flat", padx=16, pady=6,
                     cursor="hand2", activebackground="#ffd050")
btn_play.pack(side="left", padx=4)

btn_next = tk.Button(ctrl_frame, text="⏭", command=next_song,
                     bg="#c8782a", fg="#fff0cc",
                     font=("Courier New", 14, "bold"),
                     relief="flat", padx=12, pady=6,
                     cursor="hand2", activebackground="#e8a030")
btn_next.pack(side="left", padx=4)

root.mainloop()