
"""Database setup for the Student Academic Management System."""

import os
import sqlite3
from pathlib import Path

APP_NAME = "StudentAcademicManagement"

# Store application data in the user's Windows AppData directory.
APP_DATA = Path(os.getenv("LOCALAPPDATA", Path.home())) / APP_NAME
APP_DATA.mkdir(parents=True, exist_ok=True)

DB_PATH = APP_DATA / "students.db"


def create_database():
    """Create the students table and always close the connection."""
    connection = None

    try:
        connection = sqlite3.connect(DB_PATH)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS students (
                roll_no TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                python_mark REAL NOT NULL,
                database_mark REAL NOT NULL,
                web_mark REAL NOT NULL
            )
        """)

        connection.commit()
        print(f"Student database ready: {DB_PATH}")

    finally:
        if connection is not None:
            connection.close()


if __name__ == "__main__":
    create_database()
