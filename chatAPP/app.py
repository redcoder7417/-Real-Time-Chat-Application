import sqlite3
from flask import Flask, render_template, request, redirect, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from markupsafe import escape
from datetime import timedelta

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = "your_secure_random_key"  # Replace with a secure random key in production
app.permanent_session_lifetime = timedelta(minutes=30)  # Session timeout (30 minutes)

# Database utility functions
def get_db_connection():
    """Creates a new database connection."""
    conn = sqlite3.connect("chat_app.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database with required tables."""
    conn = get_db_connection()
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
    conn.close()

# Initialize the database
init_db()

@app.route("/")
def index():
    """Home page with options to log in or register."""
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Handles user login."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session.permanent = True  # Enable permanent session
            session["user"] = username
            return redirect("/chat")
        else:
            return "Invalid username or password!", 401

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Handles user registration."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        try:
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, hashed_password),
            )
            conn.commit()
            conn.close()
        except sqlite3.IntegrityError:
            return "Username already exists!", 409

        return redirect("/login")

    return render_template("register.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    """Chat page for sending and displaying messages."""
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        message = request.form["message"]
        if message.strip():  # Prevent empty messages
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO messages (user, message) VALUES (?, ?)",
                (session["user"], escape(message)),
            )
            conn.commit()
            conn.close()

    conn = get_db_connection()
    messages = conn.execute(
        "SELECT user, message, timestamp FROM messages ORDER BY timestamp DESC"
    ).fetchall()
    conn.close()

    return render_template("chat.html", messages=messages)

@app.route("/logout")
def logout():
    """Logs the user out and redirects to the home page."""
    session.pop("user", None)
    return redirect("/")

@app.route("/get-messages", methods=["GET"])
def get_messages():
    """API endpoint to fetch chat messages."""
    conn = get_db_connection()
    messages = conn.execute(
        "SELECT user, message, timestamp FROM messages ORDER BY timestamp DESC"
    ).fetchall()
    conn.close()

    return jsonify([dict(msg) for msg in messages])

if __name__ == "__main__":
    # Host the app on the network
    app.run(host="0.0.0.0", port=5000, debug=True)
