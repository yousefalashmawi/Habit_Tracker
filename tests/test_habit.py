import unittest
from habit import Habit
from datetime import datetime

class TestHabit(unittest.TestCase):
    def setUp(self):
        self.habit = Habit("Test Habit", "daily", datetime.now().isoformat())

    def test_habit_initialization(self):
        self.assertEqual(self.habit.name, "Test Habit")
        self.assertEqual(self.habit.periodicity, "daily")
        self.assertIsInstance(self.habit.creation_date, str)
        self.assertEqual(self.habit.completions, [])

    def test_add_completion(self):
        # Add a completion and verify it's added to the completions list.
        timestamp = datetime.now().isoformat()
        self.habit.add_completion(timestamp)
        self.assertIn(timestamp, self.habit.completions)

if __name__ == "__main__":
    unittest.main()
