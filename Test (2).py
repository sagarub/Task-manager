import unittest
import os
from Test import Task, TaskManager

class TestTaskManager(unittest.TestCase):

    def setUp(self):
        """Runs before each test - sets up a temporary JSON file."""
        self.test_filename = "test_tasks_temp.json"
        self.manager = TaskManager(filename=self.test_filename)

    def tearDown(self):
        """Runs after each test - cleans up the temporary file."""
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_add_valid_task(self):
        """Test 1: Adding a normal valid task."""
        t = self.manager.add_task("Finish Homework", "High", "2026-08-25")
        self.assertEqual(t.task_id, 1)
        self.assertEqual(t.title, "Finish Homework")
        self.assertEqual(len(self.manager.tasks), 1)

    def test_invalid_date_format(self):
        """Test 2: Invalid date format should throw ValueError."""
        with self.assertRaises(ValueError):
            self.manager.add_task("Read Book", "Low", "25-08-2026")

    def test_empty_title(self):
        """Test 3: Empty or spaces-only title should throw ValueError."""
        with self.assertRaises(ValueError):
            self.manager.add_task("   ", "Medium", "2026-08-25")

    def test_overdue_check(self):
        """Test 4: Task with a past due date should be overdue if not completed."""
        past_task = Task(1, "Old Task", "Low", "2020-01-01", "Pending")
        completed_task = Task(2, "Old Task Done", "Low", "2020-01-01", "Completed")

        self.assertTrue(past_task.is_overdue())
        self.assertFalse(completed_task.is_overdue())

    def test_delete_missing_id(self):
        """Test 5: Deleting a non-existent task ID should return False."""
        self.manager.add_task("Task 1", "Low", "2026-08-25")
        result = self.manager.delete_task(999) # Non-existent ID
        self.assertFalse(result)
        self.assertEqual(len(self.manager.tasks), 1)

if __name__ == "__main__":
    unittest.main()