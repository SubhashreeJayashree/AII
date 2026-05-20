
from flask import Flask, g, jsonify, request, render_template
import sqlite3
from datetime import datetime, timedelta, date, time
import math
from uuid import uuid4

DB_PATH = "schedule.db"
POMODORO_MIN = 25

app = Flask(__name__, static_folder='static', template_folder='templates')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db


def init_db():
    db = get_db()
    sql = r'''CREATE TABLE IF NOT EXISTS assignments (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  course TEXT,
  due_date TEXT NOT NULL,
  est_hours REAL NOT NULL,
  priority INTEGER DEFAULT 1,
  completed_blocks INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS availability (
  day INTEGER PRIMARY KEY,
  hours REAL NOT NULL DEFAULT 1.0
);
CREATE TABLE IF NOT EXISTS availability_windows (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  day INTEGER NOT NULL,
  start TEXT NOT NULL,
  end TEXT NOT NULL
);
'''
    db.executescript(sql)
    # backfill availability_windows from availability if empty
    cur = db.execute("SELECT COUNT(*) AS c FROM availability_windows")
    if cur.fetchone()["c"] == 0:
        rows = db.execute("SELECT day, hours FROM availability").fetchall()
        if rows:
            for r in rows:
                hours = float(r['hours'])
                if hours <= 0:
                    continue
                # create a single evening window starting at 19:00 with length=hours
                start_hour = 8
                start_min = 0
                end_dt = datetime(2000,1,1,start_hour,start_min) + timedelta(hours=hours)
                end_hour = end_dt.hour
                end_min = end_dt.minute
                start_s = f"{start_hour:02d}:{start_min:02d}"
                end_s = f"{end_hour:02d}:{end_min:02d}"
                db.execute("INSERT INTO availability_windows (day, start, end) VALUES (?,?,?)", (r['day'], start_s, end_s))
        else:
            # create a default 1-hour window 19:00-20:00 for all days
            for d in range(7):
                db.execute("INSERT INTO availability_windows (day, start, end) VALUES (?,?,?)", (d, '08:00', '22:00'))
    db.commit()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/assignments', methods=['GET', 'POST', 'DELETE'])
def api_assignments():
    db = get_db()
    if request.method == 'GET':
        rows = db.execute("SELECT * FROM assignments ORDER BY due_date").fetchall()
        return jsonify([dict(r) for r in rows])
    if request.method == 'POST':
        data = request.json
        aid = data.get('id') or str(uuid4())
        cb = int(data.get('completed_blocks', 0))
        db.execute("INSERT OR REPLACE INTO assignments (id,title,course,due_date,est_hours,priority,completed_blocks) VALUES (?,?,?,?,?,?,?)",
                   (aid, data['title'], data.get('course',''), data['due_date'], float(data['est_hours']), int(data.get('priority',1)), cb))
        db.commit()
        return jsonify(success=True)
    if request.method == 'DELETE':
        aid = request.args.get('id')
        db.execute("DELETE FROM assignments WHERE id = ?", (aid,))
        db.commit()
        return jsonify(success=True)


@app.route('/api/availability', methods=['GET','POST'])
def api_availability():
    db = get_db()
    if request.method == 'GET':
        # return windows if present, otherwise return old hours-per-day
        rows = db.execute("SELECT id, day, start, end FROM availability_windows ORDER BY day, start").fetchall()
        if rows:
            return jsonify([dict(r) for r in rows])
        rows2 = db.execute("SELECT * FROM availability").fetchall()
        return jsonify([dict(r) for r in rows2])
    data = request.json
    # If payload elements contain start/end -> replace windows; otherwise update hours table
    if data and isinstance(data, list) and 'start' in data[0]:
        # replace all windows for posted days (or full replacement)
        # simple approach: clear and re-insert
        db.execute("DELETE FROM availability_windows")
        for entry in data:
            db.execute("INSERT INTO availability_windows (day, start, end) VALUES (?,?,?)", (int(entry['day']), entry['start'], entry['end']))
        db.commit()
        return jsonify(success=True)
    else:
        for entry in data:
            # robustly parse hours that might be None or empty string
            raw_hours = entry.get('hours') if isinstance(entry, dict) else None
            if raw_hours is None or raw_hours == '':
                hours_val = 0.0
            else:
                try:
                    hours_val = float(raw_hours)
                except Exception:
                    hours_val = 0.0
            db.execute("UPDATE availability SET hours = ? WHERE day = ?", (hours_val, int(entry['day'])))
        db.commit()
        return jsonify(success=True)


@app.route('/api/complete', methods=['POST'])
def api_complete():
    db = get_db()
    data = request.json
    task_id = data.get('task_id')
    count = int(data.get('count', 1))
    if not task_id:
        return jsonify(success=False, error='missing task_id'), 400
    db.execute("UPDATE assignments SET completed_blocks = COALESCE(completed_blocks,0) + ? WHERE id = ?", (count, task_id))
    db.commit()
    return jsonify(success=True)


def parse_hhmm(s):
    h,m = s.split(':')
    return int(h), int(m)


@app.route('/api/generate', methods=['POST'])
def api_generate():
    db = get_db()
    assignments = db.execute("SELECT * FROM assignments").fetchall()
    windows = db.execute("SELECT day, start, end FROM availability_windows ORDER BY day, start").fetchall()

    if not assignments:
        return jsonify(schedule=[])

    today = date.today()
    pom = int(request.json.get('pomodoro', POMODORO_MIN))

    # build slots per date from windows
    tasks = []
    for a in assignments:
        due = datetime.fromisoformat(a['due_date']).date()
        days_until = max((due - today).days, 0)
        est_hours_val = float(a['est_hours']) if a['est_hours'] is not None else 0.0
        blocks = max(1, math.ceil(est_hours_val * (60 / pom)))
        completed = int(a['completed_blocks'] or 0) if 'completed_blocks' in a.keys() else 0
        remaining = max(0, blocks - completed)
        priority_val = int(a['priority']) if a['priority'] is not None else 1
        course_val = a['course'] if a['course'] is not None else ''
        tasks.append({'id': a['id'], 'title': a['title'], 'course': course_val, 'due': due, 'blocks': remaining, 'priority': priority_val, 'days_until': days_until})

    max_due = max(t['due'] for t in tasks)
    day_list = [today + timedelta(days=i) for i in range((max_due - today).days + 1)]

    # for each date, collect available block start datetimes
    slot_starts = []  # list of (datetime(start), date)
    for d in day_list:
        weekday = d.weekday()
        # find windows matching weekday
        for w in windows:
            if w['day'] != weekday:
                continue
            sh, sm = parse_hhmm(w['start'])
            eh, em = parse_hhmm(w['end'])
            start_dt = datetime.combine(d, time(sh, sm))
            end_dt = datetime.combine(d, time(eh, em))
            cur = start_dt
            while cur + timedelta(minutes=pom) <= end_dt:
                slot_starts.append(cur)
                cur = cur + timedelta(minutes=pom)

    # sort slot_starts chronological
    slot_starts.sort()

    # we will allocate slots by assigning latest-possible slots before due date for each task
    allocated = []
    # keep a set of used slot indices
    used = set()

    # create index mapping from date to slot indexes for quick lookup
    from collections import defaultdict
    date_to_slots = defaultdict(list)
    for idx, s in enumerate(slot_starts):
        date_to_slots[s.date()].append(idx)

    # sort tasks by due date asc then priority desc
    tasks.sort(key=lambda x: (x['days_until'], -x['priority']))

    for t in tasks:
        needed = t['blocks']
        if needed <= 0:
            continue
        # collect candidate slot indices on or before due date (earliest-first, fill days in order)
        cand_indices = [i for i,s in enumerate(slot_starts) if s.date() <= t['due']]
        for idx in cand_indices:
            if needed <= 0:
                break
            if idx in used:
                continue
            used.add(idx)
            st = slot_starts[idx]
            allocated.append({'start': st, 'end': st + timedelta(minutes=pom), 'task_id': t['id'], 'title': t['title'], 'course': t.get('course','')})
            needed -= 1
        if needed > 0:
            # not enough slots before due date: put remaining at due date's last available times (overbook)
            last_min = datetime.combine(t['due'], time(23,59))
            for _ in range(needed):
                allocated.append({'start': last_min, 'end': last_min + timedelta(minutes=pom), 'task_id': t['id'], 'title': t['title'], 'course': t.get('course',''), 'overbooked': True})

    # produce detailed schedule sorted
    detailed = []
    for a in allocated:
        detailed.append({'start': a['start'].isoformat(), 'end': a['end'].isoformat(), 'task_id': a['task_id'], 'title': a['title'], 'course': a.get('course',''), 'overbooked': a.get('overbooked', False)})
    detailed.sort(key=lambda s: s['start'])
    return jsonify(schedule=detailed)


if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)
