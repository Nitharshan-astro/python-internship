
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

import database
import student_operations as operations


class TestStudentOperations(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_db = Path(self.temp_dir.name) / "test_students.db"

        self.database_patch = patch.object(
            database, "DB_PATH", self.test_db
        )

        self.database_patch.start()
        database.create_database()

    def tearDown(self):
        self.database_patch.stop()
        self.temp_dir.cleanup()

    # 1. Add and search student
    def test_add_and_search_student(self):
        operations.add_student(
            "101", "Arun", "CSE", 90, 85, 95
        )
        student = operations.search_student("101")

        self.assertIsNotNone(student)
        self.assertEqual(student[1], "Arun")

    # 2. Fail grade calculation
    def test_calculate_result_fail(self):
        self.assertEqual(
            operations.calculate_result([90, 45, 90]),
            (225, 75.0, "Fail")
        )

    # 3. Grade A calculation
    def test_calculate_result_grade_a(self):
        self.assertEqual(
            operations.calculate_result([95, 92, 90]),
            (277, 92.33, "A")
        )

    # 4. Delete student
    def test_delete_student(self):
        operations.add_student(
            "101", "Arun", "CSE", 90, 85, 95
        )

        result = operations.delete_student("101")

        self.assertEqual(result, "Student deleted successfully!")
        self.assertIsNone(operations.search_student("101"))

    # 5. Duplicate roll number
    def test_duplicate_roll_number(self):
        operations.add_student(
            "101", "Arun", "CSE", 90, 85, 95
        )

        result = operations.add_student(
            "101", "Kumar", "IT", 80, 80, 80
        )

        self.assertEqual(result, "Roll number already exists!")

    # 6. Empty student details
    def test_empty_student_details(self):
        result = operations.add_student(
            "", "Arun", "CSE", 90, 80, 70
        )

        self.assertEqual(result, "All student details are required!")

    # 7. Invalid marks
    def test_invalid_marks(self):
        result = operations.add_student(
            "101", "Arun", "CSE", "abc", 80, 70
        )

        self.assertEqual(result, "Please enter valid marks!")

    # 8. Marks out of range
    def test_marks_out_of_range(self):
        result = operations.add_student(
            "101", "Arun", "CSE", 110, 80, 70
        )

        self.assertEqual(result, "Marks must be between 0 and 100!")

    # 9. Update missing student
    def test_student_not_found(self):
        result = operations.update_student(
            "999", "Test", "CSE", 70, 70, 70
        )

        self.assertEqual(result, "Student not found!")

    # 10. Update student
    def test_update_student(self):
        operations.add_student(
            "101", "Arun", "CSE", 90, 85, 95
        )

        result = operations.update_student(
            "101", "Arun Kumar", "IT", 80, 85, 90
        )

        self.assertEqual(result, "Student updated successfully!")
        self.assertEqual(
            operations.search_student("101")[1],
            "Arun Kumar"
        )

    # 11. View and sort students
    def test_view_students(self):
        operations.add_student(
            "102", "Bala", "IT", 80, 80, 80
        )
        operations.add_student(
            "101", "Arun", "CSE", 90, 90, 90
        )

        students = operations.view_students()

        self.assertEqual(len(students), 2)
        self.assertEqual(students[0][0], "101")

    # 12. Empty marks
    def test_empty_marks(self):
        with self.assertRaises(ValueError):
            operations.calculate_result([])

    # 13. Boundary marks
    def test_boundary_marks(self):
        result = operations.add_student(
            "103", "Boundary Student", "CSE", 0, 100, 50
        )

        self.assertEqual(result, "Student added successfully!")

    # 14. Whitespace removal
    def test_whitespace_is_removed(self):
        result = operations.add_student(
            "104", " Arun ", " CSE ", 80, 80, 80
        )

        self.assertEqual(result, "Student added successfully!")

        student = operations.search_student("104")

        self.assertEqual(student[1], "Arun")
        self.assertEqual(student[2], "CSE")

    # 15. Search missing student
    def test_search_missing_student(self):
        self.assertIsNone(operations.search_student("999"))

    # 16. Delete missing student
    def test_delete_missing_student(self):
        self.assertEqual(
            operations.delete_student("999"),
            "Student not found!"
        )

    # 17. Update with invalid marks
    def test_update_with_invalid_marks(self):
        operations.add_student(
            "105", "Arun", "CSE", 80, 80, 80
        )

        result = operations.update_student(
            "105", "Arun", "CSE", 120, 80, 80
        )

        self.assertEqual(result, "Marks must be between 0 and 100!")

    # 18. Grade B boundary
    def test_grade_b_boundary(self):
        self.assertEqual(
            operations.calculate_result([75, 75, 75])[2],
            "B"
        )

    # 19. Grade C
    def test_grade_c(self):
        self.assertEqual(
            operations.calculate_result([60, 65, 70])[2],
            "C"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
