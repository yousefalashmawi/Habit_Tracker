import unittest
import sqlite3
from datetime import datetime, timedelta
from habit_manager import HabitManager


class TestHabitManager(unittest.TestCase):
    def setUp(self):
        # Create a HabitManager using an in-memory SQLite DB.
        self.manager = HabitManager(":memory:")

    def tearDown(self):
        self.manager.close()

    def test_create_and_load_habit(self):
        # Test creating a new habit and then loading it.
        name = "Exercise"
        periodicity = "daily"
        result = self.manager.create_habit(name, periodicity)
        self.assertTrue(result)
        # Reload habits to check if the new habit is there.
        self.manager.habits = self.manager.load_habits()
        self.assertIn(name, self.manager.habits)

    def test_duplicate_habit_creation(self):
        name = "Read Book"
        periodicity = "daily"
        # Create the habit the first time.
        self.assertTrue(self.manager.create_habit(name, periodicity))
        # Try to create the same habit again.
        self.assertFalse(self.manager.create_habit(name, periodicity))

    def test_mark_completion(self):
        name = "Meditate"
        periodicity = "daily"
        self.manager.create_habit(name, periodicity)
        result = self.manager.mark_completion(name)
        self.assertTrue(result)
        # Check if the completion was recorded.
        habit = self.manager.habits[name]
        self.assertGreater(len(habit.completions), 0)

    def test_delete_habit(self):
        name = "Journal"
        periodicity = "daily"
        self.manager.create_habit(name, periodicity)
        # Confirm habit exists.
        self.assertIn(name, self.manager.habits)
        result = self.manager.delete_habit(name)
        self.assertTrue(result)
        # Confirm habit is removed.
        self.assertNotIn(name, self.manager.habits)


if __name__ == "__main__":
    unittest.main()
