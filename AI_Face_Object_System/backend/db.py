import sqlite3
import pickle

conn = sqlite3.connect("face.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS face_data (
    id INTEGER PRIMARY KEY,
    name TEXT,
    encoding BLOB
)
""")
conn.commit()

def save_face(name, encoding):
    cursor.execute("DELETE FROM face_data")
    cursor.execute(
        "INSERT INTO face_data (name, encoding) VALUES (?, ?)",
        (name, pickle.dumps(encoding))
    )
    conn.commit()

def load_face():
    cursor.execute("SELECT name, encoding FROM face_data LIMIT 1")
    row = cursor.fetchone()
    if row:
        return row[0], pickle.loads(row[1])
    return None, None
