
# Phase 2 - Program 6
# Python Collections

print("PYTHON COLLECTIONS")

# 1. LIST
# Lists are ordered and changeable

students = ["Arun", "Bala", "Kumar"]

print("\nLIST:")
print("Students:", students)

students.append("Ravi")
print("After adding:", students)

# 2. TUPLE
# Tuples are ordered and cannot be changed

marks = (85, 90, 78)

print("\nTUPLE:")
print("Marks:", marks)
print("First Mark:", marks[0])

# 3. SET
# Sets do not allow duplicate values

numbers = {10, 20, 20, 30}

print("\nSET:")
print("Numbers:", sorted(numbers))

# 4. DICTIONARY
# Stores data using key-value pairs

student = {
    "name": "Arun",
    "age": 21,
    "department": "Computer Science"
}

print("\nDICTIONARY:")
print("Name:", student["name"])
print("Age:", student["age"])
print("Department:", student["department"])

print("\nProgram 6 Completed Successfully!")
