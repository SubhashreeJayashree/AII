import sqlite3

# Create database file
conn = sqlite3.connect("commands.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS commands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    is_safe INTEGER NOT NULL,
    details TEXT
)
""")

# Insert robot-safe commands
commands = [
    ("Clean the room", 1, "General cleaning task"),
    ("Pick up the book", 1, "Pickup object"),
    ("Turn on the light", 1, "Switch control"),
    ("Bring me water", 1, "Fetch object"),

    # Unsafe commands
    ("Throw the TV outside", 0, "Unsafe task: property damage"),
    ("Break the glass", 0, "Unsafe task: dangerous"),
    ("Hit someone", 0, "Unsafe task: violence"),
]

cursor.executemany(
    "INSERT INTO commands (task, is_safe, details) VALUES (?, ?, ?)", commands
)

conn.commit()
conn.close()

print("commands.db created successfully!")
