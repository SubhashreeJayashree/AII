import tkinter as tk
from tkinter import simpledialog, messagebox

# Function to toggle visibility of the note text

def toggle_visibility(event=None):
	if note_label.cget("fg") == "white":
		note_label.config(fg="black")
	else:
		note_label.config(fg="white")

# Function to set a new note

def set_note():
	note = simpledialog.askstring("New Note", "Type your note (it will be hidden):")
	if note:
		note_label.config(text=note, fg="white")  # Hide by default
		messagebox.showinfo("Note Saved", "Your note is saved. Hover over it or press any key to reveal!")

# Tkinter GUI setup

root = tk.Tk()
root.title("Invisible Ink Notes")
root.geometry("400x250")

title_label = tk.Label(root, text="Invisible Ink Notes 📝", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

note_label = tk.Label(root, text="", font=("Arial", 14), wraplength=350)
note_label.pack(pady=30)

set_note_button = tk.Button(root, text="Add Note", font=("Arial", 14), command=set_note)
set_note_button.pack(pady=10)

# Bind mouse hover and keypress to reveal the note

note_label.bind("<Enter>", toggle_visibility)
note_label.bind("<Leave>", toggle_visibility)
root.bind("<Key>", toggle_visibility)

root.mainloop()
