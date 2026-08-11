import sqlite3
import bcrypt
import os


DATABASE = "data/users.db"


def create_database():
    """Create the users table if it doesn't exist."""

    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect(DATABASE, timeout=10)
    cursor = conn.cursor()

    cursor.execute("PRAGMA journal_mode=WAL")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def register_user(name, email, password):
    """Register a new user."""

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    try:
        conn = sqlite3.connect(DATABASE, timeout=10)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO users (name, email, password)
            VALUES (?, ?, ?)
            """,
            (name, email, password_hash.decode("utf-8"))
        )

        conn.commit()
        conn.close()

        return True, "Account created successfully!"

    except sqlite3.IntegrityError:
        return False, "Email already registered."

    except Exception as e:
        return False, f"Error: {e}"


def login_user(email, password):
    """Verify user login credentials."""

    conn = sqlite3.connect(DATABASE, timeout=10)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, name, email, password FROM users WHERE email = ?",
        (email,)
    )

    user = cursor.fetchone()
    conn.close()

    if user is None:
        return None

    stored_password = user[3].encode("utf-8")

    if bcrypt.checkpw(password.encode("utf-8"), stored_password):
        return {
            "id": user[0],
            "name": user[1],
            "email": user[2]
        }

    return None