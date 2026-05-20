
# Assignment Deadline Optimizer (MVP)

Tech: Python (Flask), SQLite, HTML/CSS/JS.

Quick setup (PowerShell):

python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py

Open http://127.0.0.1:5000 in your browser.

Features:
- Add assignments with due date and estimated hours.
- Set weekly availability (hours per day).
- Generate Pomodoro-based schedule (server computes simple schedule).
- Export generated schedule to an .ics calendar file.
