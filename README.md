# Student Task Manager — Cloud Computing Project

A beginner-friendly Flask web application for creating, completing, reopening, and deleting student tasks. It uses SQLite for storage and is structured for deployment to a Python-compatible hosting service.

## Features
- Add tasks
- Mark tasks completed
- Reopen completed tasks
- Delete tasks
- Store tasks in SQLite
- Responsive HTML/CSS interface
- Health endpoint at `/health`

## Requirements
- Python 3.10 or newer (Python 3.12 recommended)
- pip

## Run locally on Windows
1. Extract this project folder.
2. Open the folder in VS Code.
3. Open Terminal → New Terminal.
4. (Optional but recommended) create a virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
5. Install dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```
6. Start the app:
   ```powershell
   python app.py
   ```
7. Open `http://127.0.0.1:5000/`.

The SQLite database `tasks.db` is created automatically on first run.

## Deployment notes
The included `Procfile` starts the app with Gunicorn. A host needs to install dependencies from `requirements.txt` and run `web: gunicorn app:app`.

**Important storage note:** SQLite is suitable for a local demo. On a cloud host, a local file may be temporary and may be lost on redeployment or restart. To preserve tasks in the cloud, use a persistent disk and set `DATABASE_PATH` to a path on that disk, or replace SQLite with a managed PostgreSQL database. Do not claim cloud persistence until you have configured and tested it.

## Suggested screenshot checklist
1. App home page before adding tasks.
2. App showing two or three tasks.
3. A task marked Completed.
4. A task deleted.
5. VS Code project folder showing source files.
6. Terminal showing the app starting successfully.
7. Public cloud URL and hosted app, only after deployment.
8. Cloud resource/database configuration page, with secrets hidden.

## Security
- Do not publish `.env` files, passwords, database URLs, API keys, or secret tokens.
- Change `SECRET_KEY` to a long random value in deployment settings.
- This is a classroom demo, not a production multi-user task system.
