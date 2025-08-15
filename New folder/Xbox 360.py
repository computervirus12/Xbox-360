import tkinter as tk
import math
import tkinter.messagebox

# Window setup
root = tk.Tk()
root.title("Xbox 360 Inspired Dashboard")
root.configure(bg="black")
root.attributes("-fullscreen", True)

WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black", highlightthickness=0)
canvas.pack()

# Animation variables
angle = 0
center_x, center_y = WIDTH // 2, HEIGHT // 2
ring_radius = 120
orb_radius = 40
ring_count = 4
startup_done = False

# UI frame
dashboard_frame = tk.Frame(root, bg="#ccffcc")  # Light green wallpaper
tile_buttons = []
selected_tile = [0]
media_player_window = [None]

def draw_center_orb():
    canvas.create_oval(
        center_x - orb_radius, center_y - orb_radius,
        center_x + orb_radius, center_y + orb_radius,
        fill="#00B400", outline="#00FF00", width=4
    )

def draw_rotating_rings(angle):
    for i in range(ring_count):
        offset = i * 90
        rad = math.radians(angle + offset)
        x = center_x + ring_radius * math.cos(rad)
        y = center_y + ring_radius * math.sin(rad)
        canvas.create_oval(
            x - 10, y - 10, x + 10, y + 10,
            outline="#00FF00", width=3
        )

def draw_text():
    canvas.create_text(center_x, center_y + 100, text="Xbox 360", fill="white", font=("Segoe UI", 36))
    canvas.create_text(center_x, center_y + 150, text="Welcome", fill="#00FF00", font=("Segoe UI", 20))

def open_code_editor():
    editor = tk.Toplevel(root)
    editor.title("Coding App")
    editor.geometry("600x400")
    editor.configure(bg="black")

    label = tk.Label(editor, text="Code Editor", font=("Segoe UI", 20), fg="white", bg="black")
    label.pack(pady=10)

    text_area = tk.Text(editor, font=("Consolas", 14), bg="#1e1e1e", fg="white", insertbackground="white")
    text_area.pack(expand=True, fill="both", padx=10, pady=10)

    run_button = tk.Button(editor, text="Run", font=("Segoe UI", 14), bg="#00B400", fg="white")
    run_button.pack(pady=10)

def toggle_media_player():
    if media_player_window[0] and media_player_window[0].winfo_exists():
        media_player_window[0].destroy()
        media_player_window[0] = None
    else:
        player = tk.Toplevel(root)
        player.title("Windows Media Player")
        player.geometry("600x200+100+600")
        player.configure(bg="black")
        media_player_window[0] = player

        label = tk.Label(player, text="Windows Media Player", font=("Segoe UI", 20), fg="white", bg="black")
        label.pack(pady=10)

        info = tk.Label(player, text="(Simulated Player)", font=("Segoe UI", 14), fg="#00FF00", bg="black")
        info.pack()

def shutdown():
    for widget in root.winfo_children():
        widget.destroy()
    shutdown_screen = tk.Label(root, text="Shutting down...", font=("Segoe UI", 48), fg="white", bg="black")
    shutdown_screen.pack(expand=True)
    root.after(2000, root.destroy)

def open_games():
    tk.messagebox.showinfo("Games", "Launching games...")

def open_music():
    tk.messagebox.showinfo("Music", "Opening music library...")

def open_shop():
    tk.messagebox.showinfo("Shop", "Welcome to the store!")

def open_settings():
    tk.messagebox.showinfo("Settings", "Settings panel opened.")

def highlight_tile(index):
    for i, btn in enumerate(tile_buttons):
        if i == index:
            btn.configure(bg="#00FF00")
        else:
            btn.configure(bg="#00B400")

def move_selection(direction):
    if direction == "left" and selected_tile[0] > 0:
        selected_tile[0] -= 1
    elif direction == "right" and selected_tile[0] < len(tile_buttons) - 1:
        selected_tile[0] += 1
    highlight_tile(selected_tile[0])

def activate_tile():
    tile_buttons[selected_tile[0]].invoke()

def show_dashboard():
    canvas.pack_forget()
    dashboard_frame.pack(fill="both", expand=True)

    # Top navigation bar
    nav_bar = tk.Frame(dashboard_frame, bg="#ccffcc")
    nav_bar.pack(pady=10)

    nav_items = ["Bing", "Home", "Social", "Games", "TV & Movies", "Music", "Apps", "Settings"]
    for item in nav_items:
        label = tk.Label(nav_bar, text=item, font=("Segoe UI", 14), fg="#006600", bg="#ccffcc", padx=10)
        label.pack(side="left")

    # Tile container
    tile_container = tk.Frame(dashboard_frame, bg="#ccffcc")
    tile_container.pack(pady=30)

    # Dashboard tiles (smaller size with emojis)
    tiles = [
        ("📌 Games", open_games),
        ("💿 Music", open_music),
        ("🕧 Shop", open_shop),
        ("⚙️ Settings", open_settings),
        ("📝 Coding App", open_code_editor),
        ("⏻ Shutdown", shutdown)
    ]

    tile_buttons.clear()
    selected_tile[0] = 0

    for i, (label, command) in enumerate(tiles):
        tile = tk.Button(
            tile_container, text=label, command=command,
            font=("Segoe UI", 14), width=12, height=3,
            bg="#00B400", fg="white", activebackground="#00FF00"
        )
        tile.grid(row=0, column=i, padx=10, pady=10)
        tile_buttons.append(tile)

    # Bottom media control
    bottom_bar = tk.Frame(dashboard_frame, bg="#ccffcc")
    bottom_bar.pack(side="bottom", pady=20)

    media_btn = tk.Button(bottom_bar, text="🎵 Toggle Windows Media Player", command=toggle_media_player,
                          font=("Segoe UI", 14), bg="#006600", fg="white", activebackground="#00FF00")
    media_btn.pack()

    highlight_tile(selected_tile[0])

    # Keyboard navigation
    root.bind("<Left>", lambda e: move_selection("left"))
    root.bind("<Right>", lambda e: move_selection("right"))
    root.bind("<Return>", lambda e: activate_tile())

def animate():
    global angle, startup_done
    if not startup_done:
        canvas.delete("all")
        draw_rotating_rings(angle)
        draw_center_orb()
        draw_text()
        angle += 2
        if angle >= 360:
            angle = 0
        if angle == 0:
            startup_done = True
            root.after(1000, show_dashboard)
        else:
            root.after(50, animate)

animate()
root.mainloop()