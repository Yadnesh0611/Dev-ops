from flask import Flask, jsonify, request, send_from_directory
import sqlite3
import socket
import os

app = Flask(__name__)
DB_PATH = "/data/library.db"
os.makedirs("/data", exist_ok=True)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL
            )
        """)
        count = db.execute("SELECT COUNT(*) FROM books").fetchone()[0]
        if count == 0:
            db.executemany(
                "INSERT INTO books (title, author) VALUES (?, ?)",
                [
                    ("Atomic Habits", "James Clear"),
                    ("Clean Code", "Robert C. Martin"),
                    ("The Pragmatic Programmer", "Andrew Hunt"),
                    ("Python Crash Course", "Eric Matthes"),
                    ("The Alchemist", "Paulo Coelho"),
                ],
            )

def fetch_books():
    with get_db() as db:
        rows = db.execute("SELECT id, title, author FROM books ORDER BY id").fetchall()
        return [dict(row) for row in rows]

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/health")
def health():
    return jsonify(status="healthy", server=socket.gethostname())

@app.route("/api/books", methods=["GET"])
def list_books():
    return jsonify(fetch_books())

@app.route("/books", methods=["GET"])
def books_api():
    return jsonify(fetch_books())

@app.route("/books", methods=["POST"])
def add_book():
    data = request.get_json(silent=True) or {}
    title, author = data.get("title"), data.get("author")

    if not isinstance(title, str) or not title.strip() or not isinstance(author, str) or not author.strip():
        return jsonify(error="Valid title and author are required"), 400

    with get_db() as db:
        cursor = db.execute(
            "INSERT INTO books (title, author) VALUES (?, ?)",
            (title.strip(), author.strip()),
        )
        book = {
            "id": cursor.lastrowid,
            "title": title.strip(),
            "author": author.strip(),
        }

    return jsonify(book), 201

@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    with get_db() as db:
        cursor = db.execute("DELETE FROM books WHERE id = ?", (book_id,))
        if cursor.rowcount == 0:
            return jsonify(error="Book not found"), 404

    return "", 204

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
