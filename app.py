import os
import sqlite3
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-for-deployment")

# Local default. On a host with a persistent disk, set DATABASE_PATH to that disk path.
DATABASE_PATH = os.environ.get("DATABASE_PATH", str(Path(__file__).with_name("tasks.db")))


def get_db():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    Path(DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True)
    with get_db() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        task_text = request.form.get("task", "").strip()
        if task_text:
            with get_db() as connection:
                connection.execute("INSERT INTO tasks (task) VALUES (?)", (task_text,))
            flash("Task added successfully.", "success")
        else:
            flash("Please enter a task.", "error")
        return redirect(url_for("home"))

    with get_db() as connection:
        tasks = connection.execute(
            "SELECT * FROM tasks ORDER BY id DESC"
        ).fetchall()
    return render_template("index.html", tasks=tasks)


@app.post("/complete/<int:task_id>")
def complete_task(task_id):
    with get_db() as connection:
        connection.execute(
            "UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,)
        )
    flash("Task marked as completed.", "success")
    return redirect(url_for("home"))


@app.post("/reopen/<int:task_id>")
def reopen_task(task_id):
    with get_db() as connection:
        connection.execute(
            "UPDATE tasks SET completed = 0 WHERE id = ?", (task_id,)
        )
    flash("Task moved back to pending.", "success")
    return redirect(url_for("home"))


@app.post("/delete/<int:task_id>")
def delete_task(task_id):
    with get_db() as connection:
        connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    flash("Task deleted.", "success")
    return redirect(url_for("home"))


@app.get("/health")
def health():
    return {"status": "ok"}


init_db()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", 5000)), debug=True)
