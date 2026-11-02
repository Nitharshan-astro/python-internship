
"""Create a safe backup of the student database."""

import sqlite3
from datetime import datetime
from pathlib import Path

from database import DB_PATH

BACKUP_DIR = Path(__file__).resolve().parent / "backups"


def backup_database():
    """Create a timestamped SQLite database backup."""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"students_backup_{timestamp}.db"

    try:
        with sqlite3.connect(DB_PATH) as source:
            with sqlite3.connect(backup_path) as destination:
                source.backup(destination)

        print("Database backup completed successfully!")
        print(f"Backup location: {backup_path}")

    except sqlite3.Error as error:
        print(f"Database backup failed: {error}")


if __name__ == "__main__":
    backup_database()
