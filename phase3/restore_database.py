
"""Restore the student database from a selected backup."""

import sqlite3
from datetime import datetime
from pathlib import Path

from database import DB_PATH

BACKUP_DIR = Path(__file__).resolve().parent / "backups"


def restore_database():
    """Restore a backup after preserving the current database."""

    backups = sorted(BACKUP_DIR.glob("students_backup_*.db"))

    if not backups:
        print("No database backups found!")
        return

    print("\nAvailable database backups:")
    for index, backup in enumerate(backups, start=1):
        print(f"{index}. {backup.name}")

    choice = input("\nEnter the backup number to restore: ")

    if not choice.isdigit() or not 1 <= int(choice) <= len(backups):
        print("Invalid backup selection!")
        return

    selected_backup = backups[int(choice) - 1]

    # Verify the selected backup before restoring.
    try:
        with sqlite3.connect(selected_backup) as check_db:
            result = check_db.execute(
                "PRAGMA integrity_check"
            ).fetchone()[0]

            if result != "ok":
                print("Backup verification failed!")
                return

            check_db.execute("SELECT * FROM students").fetchall()

    except sqlite3.Error as error:
        print(f"Invalid backup database: {error}")
        return

    # Preserve the current database before restoration.
    if DB_PATH.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safety_backup = (
            BACKUP_DIR / f"before_restore_{timestamp}.db"
        )

        try:
            with sqlite3.connect(DB_PATH) as source:
                with sqlite3.connect(safety_backup) as destination:
                    source.backup(destination)

            print(f"Current database preserved: {safety_backup}")

        except sqlite3.Error as error:
            print(f"Could not preserve current database: {error}")
            return

    # Restore the selected backup.
    try:
        with sqlite3.connect(selected_backup) as source:
            with sqlite3.connect(DB_PATH) as destination:
                source.backup(destination)

        print("Database restored successfully!")
        print(f"Restored from: {selected_backup.name}")

    except sqlite3.Error as error:
        print(f"Database restoration failed: {error}")


if __name__ == "__main__":
    restore_database()
