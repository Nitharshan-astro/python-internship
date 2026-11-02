
# PHASE 3 - STUDENT ACADEMIC MANAGEMENT SYSTEM
# Student Operations

"""Student operations: add, view, search, update and delete records."""

import sqlite3
import database
from app_logging import logger


def calculate_result(marks):
    """Calculate total, average and grade."""

    if not marks:
        raise ValueError("At least one mark is required.")

    total = sum(marks)
    average = round(total / len(marks), 2)

    if any(mark < 50 for mark in marks):
        grade = "Fail"
    elif average >= 90:
        grade = "A"
    elif average >= 75:
        grade = "B"
    else:
        grade = "C"

    return total, average, grade


def add_student(roll_no, name, department,
                python_mark, database_mark, web_mark):
    """Add a new student to the database."""

    roll_no = str(roll_no).strip()
    name = str(name).strip()
    department = str(department).strip()

    if not roll_no or not name or not department:
        return "All student details are required!"

    try:
        marks = [
            float(python_mark),
            float(database_mark),
            float(web_mark)
        ]
    except (ValueError, TypeError):
        return "Please enter valid marks!"

    if any(mark < 0 or mark > 100 for mark in marks):
        return "Marks must be between 0 and 100!"

    connection = sqlite3.connect(database.DB_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO students
            (roll_no, name, department,
             python_mark, database_mark, web_mark)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (roll_no, name, department, *marks))

        connection.commit()

        logger.info(
            "Student added successfully: Roll No %s",
            roll_no
        )

        return "Student added successfully!"

    except sqlite3.IntegrityError:
        logger.warning(
            "Student addition failed: Duplicate Roll No %s",
            roll_no
        )
        return "Roll number already exists!"

    finally:
        connection.close()


def view_students():
    """Display all students in roll number order."""

    connection = sqlite3.connect(database.DB_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT roll_no, name, department,
                   python_mark, database_mark, web_mark
            FROM students
            ORDER BY roll_no
        """)

        return cursor.fetchall()

    finally:
        connection.close()


def search_student(roll_no):
    """Search for a student using roll number."""

    roll_no = str(roll_no).strip()

    connection = sqlite3.connect(database.DB_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT roll_no, name, department,
                   python_mark, database_mark, web_mark
            FROM students
            WHERE roll_no = ?
        """, (roll_no,))

        return cursor.fetchone()

    finally:
        connection.close()


def update_student(roll_no, name, department,
                   python_mark, database_mark, web_mark):
    """Update an existing student's details."""

    roll_no = str(roll_no).strip()
    name = str(name).strip()
    department = str(department).strip()

    if not roll_no or not name or not department:
        return "All student details are required!"

    try:
        marks = [
            float(python_mark),
            float(database_mark),
            float(web_mark)
        ]
    except (ValueError, TypeError):
        return "Please enter valid marks!"

    if any(mark < 0 or mark > 100 for mark in marks):
        return "Marks must be between 0 and 100!"

    connection = sqlite3.connect(database.DB_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE students
            SET name = ?,
                department = ?,
                python_mark = ?,
                database_mark = ?,
                web_mark = ?
            WHERE roll_no = ?
        """, (name, department, *marks, roll_no))

        connection.commit()

        if cursor.rowcount == 0:
            logger.warning(
                "Update failed: Student not found: Roll No %s",
                roll_no
            )
            return "Student not found!"

        logger.info(
            "Student updated successfully: Roll No %s",
            roll_no
        )

        return "Student updated successfully!"

    finally:
        connection.close()


def delete_student(roll_no):
    """Delete a student using roll number."""

    roll_no = str(roll_no).strip()

    connection = sqlite3.connect(database.DB_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM students
            WHERE roll_no = ?
        """, (roll_no,))

        connection.commit()

        if cursor.rowcount == 0:
            logger.warning(
                "Delete failed: Student not found: Roll No %s",
                roll_no
            )
            return "Student not found!"

        logger.info(
            "Student deleted successfully: Roll No %s",
            roll_no
        )

        return "Student deleted successfully!"

    finally:
        connection.close()


if __name__ == "__main__":
    database.create_database()
    print("Student Operations module is ready.")
