import tkinter as tk
import random

# List of micro habits

habits = ["Stretch for 1 min", "Drink a glass of water", "Blink 10 times",
"Take 3 deep breaths", "Walk 1 minute", "Write 1 thing you’re grateful for"]

def spin_wheel():
	selected_habit = random.choice(habits)
	result_label.config(text=f"🎯 Your Habit: {selected_habit}")

# Tkinter GUI setup

root = tk.Tk()
root.title("Micro Habit Wheel")
root.geometry("400x250")

title_label = tk.Label(root, text="🎡 Micro Habit Wheel", font=("Arial", 16, "bold"))
title_label.pack(pady=15)

instructions = tk.Label(root, text="Click the button to spin and get a tiny daily habit!", font=("Arial", 12), wraplength=350)
instructions.pack(pady=10)

spin_button = tk.Button(root, text="Spin Wheel", font=("Arial", 14), command=spin_wheel)
spin_button.pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 14, "bold"), fg="blue")
result_label.pack(pady=20)

root.mainloop()
