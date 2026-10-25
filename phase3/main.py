
# PYTHON INTERNSHIP - PHASE 03
# STUDENT ACADEMIC MANAGEMENT SYSTEM
# Responsive Tkinter GUI

import tkinter as tk
from tkinter import ttk, messagebox

from database import create_database

from student_operations import (
    add_student,
    view_students,
    search_student,
    update_student,
    delete_student,
    calculate_result
)


# ---------------------------------
# DATABASE SETUP
# ---------------------------------

create_database()


# ---------------------------------
# MAIN WINDOW
# ---------------------------------

root = tk.Tk()

root.title("Student Academic Management System")
root.geometry("1000x700")
root.minsize(480, 450)

root.resizable(True, True)


# ---------------------------------
# RESPONSIVE HEADING
# ---------------------------------

title = tk.Label(
    root,
    text="STUDENT ACADEMIC MANAGEMENT SYSTEM",
    font=("Arial", 18, "bold"),
    anchor="center",
    justify="center"
)

title.pack(
    fill="x",
    padx=10,
    pady=(12, 8)
)


# ---------------------------------
# SCROLLABLE CONTENT AREA
# ---------------------------------

content_frame = tk.Frame(root)
content_frame.pack(
    fill="both",
    expand=True
)

canvas = tk.Canvas(
    content_frame,
    highlightthickness=0
)

page_scrollbar = ttk.Scrollbar(
    content_frame,
    orient="vertical",
    command=canvas.yview
)

canvas.configure(
    yscrollcommand=page_scrollbar.set
)

page_scrollbar.pack(
    side="right",
    fill="y"
)

canvas.pack(
    side="left",
    fill="both",
    expand=True
)

page = tk.Frame(canvas)

page_window = canvas.create_window(
    (0, 0),
    window=page,
    anchor="nw"
)


def update_scroll_region(event=None):
    canvas.configure(
        scrollregion=canvas.bbox("all")
    )


def resize_page(event):
    canvas.itemconfigure(
        page_window,
        width=event.width
    )


page.bind(
    "<Configure>",
    update_scroll_region
)

canvas.bind(
    "<Configure>",
    resize_page
)


# ---------------------------------
# STUDENT INPUT FORM
# ---------------------------------

form = tk.LabelFrame(
    page,
    text="Student Details",
    font=("Arial", 11, "bold"),
    padx=10,
    pady=10
)

form.pack(
    fill="x",
    padx=15,
    pady=8
)


fields = [
    "Roll Number",
    "Student Name",
    "Department",
    "Python Mark",
    "Database Mark",
    "Web Development Mark"
]

entries = {}

for i, field in enumerate(fields):

    label = tk.Label(
        form,
        text=field,
        font=("Arial", 10),
        anchor="w"
    )

    label.grid(
        row=i,
        column=0,
        padx=5,
        pady=5,
        sticky="w"
    )

    entry = ttk.Entry(
        form,
        font=("Arial", 10)
    )

    entry.grid(
        row=i,
        column=1,
        padx=5,
        pady=5,
        sticky="ew"
    )

    entries[field] = entry


form.grid_columnconfigure(0, weight=1)
form.grid_columnconfigure(1, weight=2)


# ---------------------------------
# INPUT FUNCTIONS
# ---------------------------------

def get_values():

    return [
        entries[field].get()
        for field in fields
    ]


def clear_fields():

    for entry in entries.values():
        entry.delete(0, tk.END)


# ---------------------------------
# STUDENT TABLE FUNCTIONS
# ---------------------------------

def refresh_table():

    # Remove previously displayed rows
    for item in table.get_children():
        table.delete(item)

    # Fetch saved student records
    for student in view_students():

        marks = student[3:6]

        total, average, grade = calculate_result(marks)

        table.insert(
            "",
            tk.END,
            values=(
                student[0],
                student[1],
                student[2],
                total,
                average,
                grade
            )
        )


# ---------------------------------
# ADD STUDENT
# ---------------------------------

def add_record():

    values = get_values()

    result = add_student(*values)

    messagebox.showinfo(
        "Add Student",
        result
    )

    refresh_table()


# ---------------------------------
# SEARCH STUDENT
# ---------------------------------

def search_record():

    roll = entries["Roll Number"].get().strip()

    if not roll:

        messagebox.showwarning(
            "Search Student",
            "Please enter a roll number!"
        )

        return

    student = search_student(roll)

    if student:

        clear_fields()

        for field, value in zip(fields, student):

            entries[field].insert(
                0,
                str(value)
            )

        messagebox.showinfo(
            "Search Student",
            "Student found successfully!"
        )

    else:

        messagebox.showwarning(
            "Search Student",
            "Student not found!"
        )


# ---------------------------------
# UPDATE STUDENT
# ---------------------------------

def update_record():

    values = get_values()

    result = update_student(*values)

    messagebox.showinfo(
        "Update Student",
        result
    )

    refresh_table()


# ---------------------------------
# DELETE STUDENT
# ---------------------------------

def delete_record():

    roll = entries["Roll Number"].get().strip()

    if not roll:

        messagebox.showwarning(
            "Delete Student",
            "Please enter a roll number!"
        )

        return

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this student?"
    )

    if confirm:

        result = delete_student(roll)

        messagebox.showinfo(
            "Delete Student",
            result
        )

        refresh_table()


# ---------------------------------
# RESPONSIVE BUTTONS
# ---------------------------------

buttons_frame = tk.Frame(page)

buttons_frame.pack(
    fill="x",
    padx=15,
    pady=10
)


button_data = [
    ("Add", add_record),
    ("View All", refresh_table),
    ("Search", search_record),
    ("Update", update_record),
    ("Delete", delete_record),
    ("Clear", clear_fields)
]


button_widgets = []

for text, command in button_data:

    button = tk.Button(
        buttons_frame,
        text=text,
        command=command,
        font=("Arial", 10),
        padx=8,
        pady=7
    )

    button_widgets.append(button)


current_columns = None


def arrange_buttons(window_width):

    global current_columns

    # Adjust number of buttons per row
    if window_width < 650:
        columns = 2

    elif window_width < 900:
        columns = 3

    else:
        columns = 6

    # Avoid unnecessary rearrangement
    if current_columns == columns:
        return

    current_columns = columns

    for button in button_widgets:
        button.grid_forget()

    for col in range(6):

        buttons_frame.grid_columnconfigure(
            col,
            weight=1 if col < columns else 0
        )

    for i, button in enumerate(button_widgets):

        row = i // columns
        col = i % columns

        button.grid(
            row=row,
            column=col,
            padx=4,
            pady=4,
            sticky="ew"
        )


# ---------------------------------
# RESPONSIVE STUDENT TABLE
# ---------------------------------

table_frame = tk.LabelFrame(
    page,
    text="Student Records",
    font=("Arial", 11, "bold"),
    padx=5,
    pady=5
)

table_frame.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=10
)


columns = (
    "Roll",
    "Name",
    "Department",
    "Total",
    "Average",
    "Grade"
)


table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=10
)


for column in columns:

    table.heading(
        column,
        text=column
    )

    table.column(
        column,
        width=120,
        minwidth=90,
        stretch=True
    )


# Vertical table scrollbar
vertical_scroll = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=table.yview
)


# Horizontal table scrollbar
horizontal_scroll = ttk.Scrollbar(
    table_frame,
    orient="horizontal",
    command=table.xview
)


table.configure(
    yscrollcommand=vertical_scroll.set,
    xscrollcommand=horizontal_scroll.set
)


table.grid(
    row=0,
    column=0,
    sticky="nsew"
)

vertical_scroll.grid(
    row=0,
    column=1,
    sticky="ns"
)

horizontal_scroll.grid(
    row=1,
    column=0,
    sticky="ew"
)


table_frame.grid_rowconfigure(
    0,
    weight=1
)

table_frame.grid_columnconfigure(
    0,
    weight=1
)


# ---------------------------------
# RESPONSIVE WINDOW HANDLER
# ---------------------------------

def handle_resize(event):

    # Only respond to main window resizing
    if event.widget is not root:
        return

    width = event.width

    # Responsive heading
    if width < 650:

        title.config(
            text="STUDENT ACADEMIC\nMANAGEMENT SYSTEM",
            font=("Arial", 11, "bold")
        )

    elif width < 900:

        title.config(
            text="STUDENT ACADEMIC\nMANAGEMENT SYSTEM",
            font=("Arial", 15, "bold")
        )

    else:

        title.config(
            text="STUDENT ACADEMIC MANAGEMENT SYSTEM",
            font=("Arial", 18, "bold")
        )

    # Responsive buttons
    arrange_buttons(width)


root.bind(
    "<Configure>",
    handle_resize
)


# Set initial button arrangement
arrange_buttons(1000)


# ---------------------------------
# START APPLICATION
# ---------------------------------

# Do not call refresh_table() here.
# Records appear only when View All is clicked.

root.mainloop()
