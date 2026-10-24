
# Phase 2 - Program 3
# Conditional Statements

mark = int(input("Enter your mark: "))

if mark < 0 or mark > 100:
    print("Invalid mark")
elif mark >= 90:
    print("Grade: A")
elif mark >= 75:
    print("Grade: B")
elif mark >= 50:
    print("Grade: C")
else:
    print("Result: Fail")

print("Program 3 Completed!")
