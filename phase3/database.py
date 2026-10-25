
# PHASE 3 - STUDENT ACADEMIC MANAGEMENT SYSTEM
# Database Setup

import sqlite3
from pathlib import Path

# Database location
DB_PATH = Path(__file__).parent / "students.db"


def create_database():

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
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
    connection.close()

    print("Student database created successfully!")


if __name__ == "__main__":
    create_database()
