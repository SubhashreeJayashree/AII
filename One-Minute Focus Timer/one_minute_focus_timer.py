import tkinter as tk
from tkinter import messagebox
import time

# Timer duration in seconds (1 minute)

TIMER_DURATION = 60

# placeholders to avoid name errors in linters before widgets are created
start_button = None
reset_button = None
timer_label = None
root = None

def start_timer():
	global start_button, reset_button
	start_button.config(state="disabled")
	reset_button.config(state="normal")
	countdown(TIMER_DURATION)

def countdown(seconds):
	global timer_label, root, start_button
	if seconds >= 0:
		mins, secs = divmod(seconds, 60)
		timer_label.config(text=f"{mins:02d}:{secs:02d}")
		# Quirky animation: change color randomly each second
		colors = ["red", "green", "blue", "orange", "purple", "pink"]
		timer_label.config(fg=colors[seconds % len(colors)])
		root.after(1000, countdown, seconds - 1)
	else:
		messagebox.showinfo("Time's Up!", "✅ One minute of focus completed!")
		start_button.config(state="normal")

def reset_timer():
	global start_button, reset_button, timer_label
	start_button.config(state="normal")
	timer_label.config(text="01:00", fg="black")
	reset_button.config(state="disabled")

# Tkinter GUI setup

root = tk.Tk()
root.title("One-Minute Focus Timer")
root.geometry("300x200")

title_label = tk.Label(root, text="⏱ One-Minute Focus Timer", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

timer_label = tk.Label(root, text="01:00", font=("Arial", 36), fg="black")
timer_label.pack(pady=20)

start_button = tk.Button(root, text="Start", font=("Arial", 14), command=start_timer)
start_button.pack(pady=5)

reset_button = tk.Button(root, text="Reset", font=("Arial", 14), command=reset_timer, state="disabled")
reset_button.pack(pady=5)

root.mainloop()
