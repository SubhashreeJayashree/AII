import tkinter as tk
import random

# Canvas size and pixel size
CANVAS_WIDTH = 200
CANVAS_HEIGHT = 200
PIXEL_SIZE = 20  # Size of each "pixel" block

# List of colors
colors = ["red", "green", "blue", "yellow", "purple", "orange", "pink", "cyan"]

def generate_art():
    canvas.delete("all")  # Clear previous art
    rows = CANVAS_HEIGHT // PIXEL_SIZE
    cols = CANVAS_WIDTH // PIXEL_SIZE
    for i in range(rows):
        for j in range(cols):
            color = random.choice(colors)
            x0 = j * PIXEL_SIZE
            y0 = i * PIXEL_SIZE
            x1 = x0 + PIXEL_SIZE
            y1 = y0 + PIXEL_SIZE
            canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

# Tkinter GUI setup
root = tk.Tk()
root.title("🎨 Random Tiny Art Generator")
root.geometry(f"{CANVAS_WIDTH + 50}x{CANVAS_HEIGHT + 100}")

title_label = tk.Label(root, text="🎨 Random Tiny Art Generator", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
canvas.pack(pady=10)

generate_button = tk.Button(root, text="Generate Art", font=("Arial", 14), command=generate_art)
generate_button.pack(pady=10)

root.mainloop()
