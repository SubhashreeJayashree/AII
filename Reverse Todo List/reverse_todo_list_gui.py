import tkinter as tk
import os
from tkinter import simpledialog
from copy import deepcopy

TASK_FILE = "tasks.txt"
tasks = []
undo_stack = []

categories = {
    "General": "#333333",
    "Work": "#1E90FF",
    "Personal": "#28A745",
    "Urgent": "#DC3545"
}

# Load tasks (force all as done)
if os.path.exists(TASK_FILE):
    with open(TASK_FILE, "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip()
            parts = line.replace("[DONE] ", "").split("|")
            if len(parts) == 2:
                task_text, category = parts
            else:
                task_text, category = line, "General"
            tasks.append((task_text, True, category))

def save_tasks():
    with open(TASK_FILE, "w", encoding="utf-8") as f:
        for task, _, category in tasks:
            f.write(f"[DONE] {task}|{category}\n")

def push_undo():
    undo_stack.append(deepcopy(tasks))
    if len(undo_stack) > 20:
        undo_stack.pop(0)

def undo(event=None):
    if undo_stack:
        global tasks
        tasks = undo_stack.pop()
        apply_filter()
        save_tasks()

def add_task(event=None):
    task = task_entry.get().strip()
    category = category_var.get()
    if task:
        push_undo()
        tasks.append((task, True, category))  # always done
        task_entry.delete(0, tk.END)
        apply_filter(highlight_new=len(tasks)-1)
        save_tasks()

def edit_category(event=None):
    selected_indices = listbox.curselection()
    if selected_indices:
        idx = len(tasks) - 1 - selected_indices[0]
        task, done, old_category = tasks[idx]
        new_category = simpledialog.askstring(
            "Edit Category",
            f"Current category: {old_category}\nEnter new category:",
            initialvalue=old_category
        )
        if new_category:
            push_undo()
            if new_category not in categories:
                categories[new_category] = "#6f42c1"
            tasks[idx] = (task, done, new_category)
            apply_filter()
            save_tasks()

def clear_all():
    if tasks:
        push_undo()
        tasks.clear()
        apply_filter()
        save_tasks()

def update_list(filtered_indices=None, highlight_new=None):
    listbox.delete(0, tk.END)
    display_indices = filtered_indices if filtered_indices else range(len(tasks))
    for idx in reversed(display_indices):
        task, done, category = tasks[idx]
        display_text = f"[DONE] {task}"
        listbox.insert(tk.END, display_text)
        listbox.itemconfig(tk.END, fg="gray")
    if highlight_new is not None:
        rev_idx = len(tasks) - 1 - highlight_new
        listbox.itemconfig(rev_idx, bg="#FFFACD")
        root.after(1000, lambda: listbox.itemconfig(rev_idx, bg="white"))

def apply_filter(highlight_new=None):
    keyword = search_var.get().lower()
    selected_category = filter_var.get()
    filtered_indices = []
    for i, (task, done, category) in enumerate(tasks):
        if (keyword in task.lower()) and (selected_category == "All" or category == selected_category):
            filtered_indices.append(i)
    update_list(filtered_indices, highlight_new)

def apply_bulk_category(category_name):
    selected_indices = listbox.curselection()
    if selected_indices:
        push_undo()
        if category_name not in categories:
            categories[category_name] = "#6f42c1"
        for selected in selected_indices:
            idx = len(tasks) - 1 - selected
            task, done, _ = tasks[idx]
            tasks[idx] = (task, done, category_name)
        apply_filter()
        save_tasks()

# GUI setup
root = tk.Tk()
root.title("🔁 Reversed Todo List (Always Done)")
root.geometry("900x750")
root.configure(bg="#f5f5f5")

title_label = tk.Label(root, text="🔁 Reversed Todo List (Always Done)", font=("Helvetica", 22, "bold"), bg="#f5f5f5")
title_label.pack(pady=15)

task_entry = tk.Entry(root, font=("Helvetica", 14), width=60, bd=2, relief="groove")
task_entry.pack(pady=10)
task_entry.bind("<Return>", add_task)

category_frame = tk.Frame(root, bg="#f5f5f5")
category_frame.pack(pady=5)
category_var = tk.StringVar(value="General")
for cat, color in categories.items():
    b = tk.Radiobutton(category_frame, text=cat, variable=category_var, value=cat, font=("Helvetica", 12),
                       fg="white", bg=color, indicatoron=0, width=10, selectcolor=color)
    b.pack(side="left", padx=5)

# Define filter_var first
filter_var = tk.StringVar(value="All")

filter_frame = tk.Frame(root, bg="#f5f5f5")
filter_frame.pack(pady=5)
tk.Label(filter_frame, text="Filter:", font=("Helvetica", 12), bg="#f5f5f5").pack(side="left")
filter_menu = tk.OptionMenu(filter_frame, filter_var, "All", *categories.keys(), command=lambda _: apply_filter())
filter_menu.config(font=("Helvetica", 12))
filter_menu.pack(side="left", padx=5)

button_frame = tk.Frame(root, bg="#f5f5f5")
button_frame.pack(pady=5)
btn_config = {"font": ("Helvetica", 12, "bold"), "width": 12, "bd": 0, "bg": "#6c757d", "fg": "white", "activebackground": "#495057"}
tk.Button(button_frame, text="Add Task", command=add_task, **btn_config).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Edit Category", command=edit_category, **btn_config).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Clear All", command=clear_all, **btn_config).grid(row=0, column=2, padx=5)
tk.Button(button_frame, text="Undo", command=undo, **btn_config).grid(row=0, column=3, padx=5)

# Create listbox BEFORE search_var.trace
listbox = tk.Listbox(root, font=("Helvetica", 14), width=100, height=25, selectmode=tk.EXTENDED, bd=2, relief="sunken")
listbox.pack(pady=10)
listbox.bind("<Button-3>", lambda e: edit_category())

# Now define search_var safely
search_var = tk.StringVar()
search_var.trace("w", lambda *args: apply_filter())
search_entry = tk.Entry(root, textvariable=search_var, font=("Helvetica", 14), width=40, bd=2, relief="groove")
search_entry.pack(pady=5)
search_entry.insert(0, "Search...")

# Dragging
drag_data = {"index": None, "text": None}

def start_drag(event):
    drag_data["index"] = listbox.nearest(event.y)
    drag_data["text"] = listbox.get(drag_data["index"])
    listbox.delete(drag_data["index"])

def during_drag(event):
    if drag_data["text"] is None:
        return
    y_index = listbox.nearest(event.y)
    listbox.insert(y_index, drag_data["text"])
    drag_data["index"] = y_index

def stop_drag(event):
    if drag_data["text"] is None:
        return
    new_index = listbox.nearest(event.y)
    moving_task = tasks.pop(len(tasks) - 1 - drag_data["index"])
    insert_at = len(tasks) - new_index
    tasks.insert(insert_at, moving_task)
    drag_data["text"] = None
    apply_filter()
    save_tasks()

listbox.bind("<Button-1>", start_drag)
listbox.bind("<B1-Motion>", during_drag)
listbox.bind("<ButtonRelease-1>", stop_drag)

# Bulk categories shortcuts
root.bind("<Control-1>", lambda e: apply_bulk_category("General"))
root.bind("<Control-2>", lambda e: apply_bulk_category("Work"))
root.bind("<Control-3>", lambda e: apply_bulk_category("Personal"))
root.bind("<Control-4>", lambda e: apply_bulk_category("Urgent"))

# Call apply_filter only after everything is created
apply_filter()
root.mainloop()
