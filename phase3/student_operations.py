
# PHASE 3 - STUDENT ACADEMIC MANAGEMENT SYSTEM
# Student Management Operations

import sqlite3
from database import DB_PATH, create_database


# Calculate student result
def calculate_result(marks):

    total = sum(marks)
    average = total / len(marks)

    if any(mark < 50 for mark in marks):
        grade = "Fail"
    elif average >= 90:
        grade = "A"
    elif average >= 75:
        grade = "B"
    else:
        grade = "C"

    return total, round(average, 2), grade


# Add student
def add_student(roll, name, department, m1, m2, m3):

    roll = roll.strip()
    name = name.strip()
    department = department.strip()

    if not roll or not name or not department:
        return "All student details are required!"

    try:
        marks = [float(m1), float(m2), float(m3)]
    except (ValueError, TypeError):
        return "Please enter valid marks!"

    if any(not 0 <= mark <= 100 for mark in marks):
        return "Marks must be between 0 and 100!"

    connection = sqlite3.connect(DB_PATH)

    try:
        connection.execute("""
            INSERT INTO students
            VALUES (?, ?, ?, ?, ?, ?)
        """, (roll, name, department, *marks))

        connection.commit()
        return "Student added successfully!"

    except sqlite3.IntegrityError:
        return "Roll number already exists!"

    finally:
        connection.close()


# View all students
def view_students():

    connection = sqlite3.connect(DB_PATH)

    try:
        cursor = connection.execute(
            "SELECT * FROM students ORDER BY roll_no"
        )
        return cursor.fetchall()

    finally:
        connection.close()


# Search student
def search_student(roll):

    connection = sqlite3.connect(DB_PATH)

    try:
        cursor = connection.execute(
            "SELECT * FROM students WHERE roll_no = ?",
            (roll,)
        )

        return cursor.fetchone()

    finally:
        connection.close()


# Update student

def update_student(roll, name, department, m1, m2, m3):

    roll = roll.strip()
    name = name.strip()
    department = department.strip()

    if not roll or not name or not department:
        return "All student details are required!"

    try:
        marks = [float(m1), float(m2), float(m3)]
    except (ValueError, TypeError):
        return "Please enter valid marks!"

    if any(not 0 <= mark <= 100 for mark in marks):
        return "Marks must be between 0 and 100!"

    connection = sqlite3.connect(DB_PATH)

    try:
        cursor = connection.execute("""
            UPDATE students
            SET name = ?,
                department = ?,
                python_mark = ?,
                database_mark = ?,
                web_mark = ?
            WHERE roll_no = ?
        """, (
            name,
            department,
            *marks,
            roll
        ))

        connection.commit()

        if cursor.rowcount == 0:
            return "Student not found!"

        return "Student updated successfully!"

    finally:
        connection.close()

# Delete student
def delete_student(roll):

    connection = sqlite3.connect(DB_PATH)

    try:
        cursor = connection.execute(
            "DELETE FROM students WHERE roll_no = ?",
            (roll.strip(),)
        )

        connection.commit()

        if cursor.rowcount == 0:
            return "Student not found!"

        return "Student deleted successfully!"

    finally:
        connection.close()


# Test operations
if __name__ == "__main__":

    create_database()

    print("\nSTUDENT MANAGEMENT TEST")

    print(add_student(
        "101", "Arun", "Computer Science",
        90, 85, 95
    ))

    print("\nStudent Records:")

    for student in view_students():
        print(student)

    print("\nSearch Result:")
    print(search_student("101"))

    print("\nCalculated Result:")
    print(calculate_result([90, 85, 95]))

    print("\nProgram executed successfully!")
