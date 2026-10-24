
# Phase 2 - Program 5
# Simple Calculator Using Functions

# Addition Function
def add(a, b):
    return a + b

# Subtraction Function
def subtract(a, b):
    return a - b

# Multiplication Function
def multiply(a, b):
    return a * b

# Division Function
def divide(a, b):
    if b == 0:
        return "Cannot divide by zero"
    return a / b


# Get input from user
print("SIMPLE CALCULATOR")

a = float(input("Enter first number: "))
b = float(input("Enter second number: "))

print("\nAddition:", add(a, b))
print("Subtraction:", subtract(a, b))
print("Multiplication:", multiply(a, b))
print("Division:", divide(a, b))

print("\nProgram 5 Completed Successfully!")
