# Human → Robot Translation Engine (Simulator)

Student-friendly project that converts natural language instructions into robot-style commands,
checks for safety, and simulates execution in the browser (no real robot required).

## Features
- Rule-based safety checker (rejects dangerous tasks)
- Optional LLM safety & translator (configure via .env)
- Offline rule-based translator (task → steps)
- Flask backend with `/check` and `/translate` endpoints
- Frontend chat UI, fake robot canvas, animation, and speech output
- Simple SQLite logging of instructions

## Folder structure
