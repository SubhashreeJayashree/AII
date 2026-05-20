#!/usr/bin/env python3
import sqlite3
from pathlib import Path

p = Path(__file__).parent / 'commands.db'
print('DB Path:', p.resolve())
conn = sqlite3.connect(p)
cur = conn.cursor()
try:
    rows = cur.execute('SELECT id, name, description, template, created_at FROM commands').fetchall()
    if not rows:
        print('No rows in commands table.')
    else:
        print('\nRows in commands table:')
        for r in rows:
            print(r)
except Exception as e:
    print('Error reading DB:', e)
finally:
    conn.close()
