#!/usr/bin/env python3
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "commands.db"

def init_db(path: Path):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS commands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            template TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    sample = [
        ("move_forward", "Move robot forward specified meters", '{"action":"move","direction":"forward","meters":1}'),
        ("turn", "Turn robot by degrees", '{"action":"turn","degrees":90}'),
        ("pick", "Pick up object", '{"action":"manipulate","type":"pick"}'),
    ]

    for name, desc, template in sample:
        try:
            cur.execute(
                "INSERT INTO commands (name, description, template) VALUES (?, ?, ?)",
                (name, desc, template),
            )
        except sqlite3.IntegrityError:
            # already exists
            pass

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db(DB_PATH)
    print(f"Created or updated database at: {DB_PATH}")
