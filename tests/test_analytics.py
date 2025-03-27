import unittest
from datetime import datetime, timedelta
from habit import Habit
from analytics import compute_longest_streak, longest_run_streak_all

class TestAnalytics(unittest.TestCase):
    def setUp(self):
        # Create a habit with daily completions for 4 weeks.
        self.daily_habit = Habit("Daily Habit", "daily", datetime.now().isoformat())
        start_date = datetime.now() - timedelta(days=27)  # 28 days period
        for i in range(28):
            ts = (start_date + timedelta(days=i)).isoformat()
            self.daily_habit.add_completion(ts)

        # Create a weekly habit with completions every week.
        self.weekly_habit = Habit("Weekly Habit", "weekly", datetime.now().isoformat())
        start_date = datetime.now() - timedelta(weeks=3)
        for i in range(4):
            ts = (start_date + timedelta(weeks=i)).isoformat()
            self.weekly_habit.add_completion(ts)


    def test_compute_longest_streak_daily(self):
        # For a complete daily streak, the longest streak should be 28.
        streak = compute_longest_streak(self.daily_habit)
        self.assertEqual(streak, 28)

    def test_compute_longest_streak_weekly(self):
        # For a complete weekly streak, the longest streak should be 4.
        streak = compute_longest_streak(self.weekly_habit)
        self.assertEqual(streak, 4)

    def test_longest_run_streak_all(self):
        # Test analytics across multiple habits.
        habits = [self.daily_habit, self.weekly_habit]
        best_habits, max_streak = longest_run_streak_all(habits)
        # The daily habit should have the longest streak.
        self.assertIn(self.daily_habit.name, best_habits)
        self.assertEqual(max_streak, 28)

if __name__ == "__main__":
    unittest.main()
