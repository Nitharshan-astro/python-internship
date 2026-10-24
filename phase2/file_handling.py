
# Phase 2 - Program 7
# Python File Handling

from pathlib import Path

# Save the text file in the same folder as this program
file_path = Path(__file__).parent / "student.txt"

print("PYTHON FILE HANDLING")

# 1. WRITE - Create a new file
with open(file_path, "w") as file:
    file.write("Student Name: Arun\n")
    file.write("Department: Computer Science\n")

print("\nFile created successfully!")

# 2. APPEND - Add new content
with open(file_path, "a") as file:
    file.write("Mark: 90\n")

print("New data added successfully!")

# 3. READ - Display file content
with open(file_path, "r") as file:
    content = file.read()

print("\nFILE CONTENT:")
print(content)

print("Program 7 Completed Successfully!")

