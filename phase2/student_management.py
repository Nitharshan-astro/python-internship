
# PYTHON INTERNSHIP - PHASE 02
# MINI PROJECT: STUDENT MARKS MANAGEMENT SYSTEM

import json
from pathlib import Path

# Database file
DATA_FILE = Path(__file__).parent / "students.json"


# Load existing student records
def load_students():
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            print("Unable to read saved records.")
    return []


# Save student records
def save_students(students):
    with open(DATA_FILE, "w") as file:
        json.dump(students, file, indent=4)


# Calculate grade
def calculate_grade(average):
    if average >= 90:
        return "A"
    elif average >= 75:
        return "B"
    elif average >= 50:
        return "C"
    else:
        return "Fail"


# Add a new student
def add_student(students):

    roll = input("Enter Roll Number: ").strip()

    if not roll:
        print("Roll number cannot be empty!")
        return

    for student in students:
        if student["roll"] == roll:
            print("Roll number already exists!")
            return

    name = input("Enter Student Name: ").strip()

    if not name:
        print("Student name cannot be empty!")
        return

    try:
        mark1 = float(input("Enter Python Mark: "))
        mark2 = float(input("Enter Database Mark: "))
        mark3 = float(input("Enter Web Development Mark: "))

        marks = [mark1, mark2, mark3]

        if any(mark < 0 or mark > 100 for mark in marks):
            print("Marks must be between 0 and 100!")
            return

    except ValueError:
        print("Invalid input! Please enter numbers.")
        return

    total = sum(marks)
    average = total / 3

    # A student must pass every subject
    if any(mark < 50 for mark in marks):
        grade = "Fail"
    else:
        grade = calculate_grade(average)

    student = {
        "roll": roll,
        "name": name,
        "marks": marks,
        "total": total,
        "average": round(average, 2),
        "grade": grade
    }

    students.append(student)
    save_students(students)

    print("\nStudent added successfully!")


# Display student details
def display_student(student):

    print("\n---------------------------")
    print("Roll Number:", student["roll"])
    print("Name:", student["name"])
    print("Python Mark:", student["marks"][0])
    print("Database Mark:", student["marks"][1])
    print("Web Development Mark:", student["marks"][2])
    print("Total:", student["total"])
    print("Average:", student["average"])
    print("Grade:", student["grade"])
    print("---------------------------")


# View all students
def view_students(students):

    if not students:
        print("\nNo student records found!")
        return

    for student in students:
        display_student(student)


# Search student
def search_student(students):

    roll = input("Enter Roll Number to Search: ").strip()

    for student in students:
        if student["roll"] == roll:
            display_student(student)
            return

    print("Student not found!")


# Main program
def main():

    students = load_students()

    while True:

        print("\n================================")
        print(" STUDENT MARKS MANAGEMENT SYSTEM")
        print("================================")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_student(students)

        elif choice == "2":
            view_students(students)

        elif choice == "3":
            search_student(students)

        elif choice == "4":
            print("\nThank you! Program Closed.")
            break

        else:
            print("Invalid choice! Try again.")


if __name__ == "__main__":
    main()
