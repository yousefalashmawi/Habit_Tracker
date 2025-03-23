
import sqlite3
from datetime import datetime, timedelta
from habit import Habit

DB_NAME = "habits.db"

class HabitManager:
    def __init__(self, db_name=DB_NAME):

        self.connection = sqlite3.connect(db_name)
        self.connection.row_factory = sqlite3.Row
        self.create_tables()
        self.habits = self.load_habits()

    def create_tables(self):

        with self.connection:
            self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS habits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    periodicity TEXT NOT NULL,
                    creation_date TEXT NOT NULL
                )
                """
            )
            self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS completions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_id INTEGER NOT NULL,
                    completion_date TEXT NOT NULL,
                    FOREIGN KEY(habit_id) REFERENCES habits(id)
                )
                """
            )

    def load_habits(self):

        habits_dict = {}
        cursor = self.connection.execute("SELECT * FROM habits")
        for row in cursor.fetchall():
            name = row["name"]
            periodicity = row["periodicity"]
            creation_date = row["creation_date"]
            habits_dict[name] = Habit(name, periodicity, creation_date, [])

        for habit_name in habits_dict:
            habit_id = self.get_habit_id(habit_name)
            cursor = self.connection.execute(
                "SELECT completion_date FROM completions WHERE habit_id = ?",
                (habit_id,)
            )
            for c in cursor.fetchall():
                habits_dict[habit_name].completions.append(c["completion_date"])

        return habits_dict

    def get_habit_id(self, habit_name):
        """Return the habit's database ID given its name."""
        cursor = self.connection.execute(
            "SELECT id FROM habits WHERE name = ?",
            (habit_name,)
        )
        row = cursor.fetchone()
        return row["id"] if row else None

    def create_habit(self, name, periodicity):

        if name in self.habits:
            return False

        creation_date = datetime.now().isoformat()
        with self.connection:
            self.connection.execute(
                "INSERT INTO habits (name, periodicity, creation_date) VALUES (?, ?, ?)",
                (name, periodicity, creation_date)
            )
        self.habits[name] = Habit(name, periodicity, creation_date, [])
        return True

    def delete_habit(self, name):

        if name not in self.habits:
            return False

        habit_id = self.get_habit_id(name)
        with self.connection:
            self.connection.execute("DELETE FROM completions WHERE habit_id = ?", (habit_id,))
            self.connection.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
        del self.habits[name]
        return True

    def mark_completion(self, name):

        habit = self.habits.get(name)
        if not habit:
            return False

        now_ts = datetime.now().isoformat()
        habit_id = self.get_habit_id(name)
        with self.connection:
            self.connection.execute(
                "INSERT INTO completions (habit_id, completion_date) VALUES (?, ?)",
                (habit_id, now_ts)
            )
        habit.add_completion(now_ts)
        return True

    def list_habits(self):
        return list(self.habits.values())

    def commit_changes(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

    def populate_test_data_if_empty(self):
        cursor = self.connection.execute("SELECT COUNT(*) as cnt FROM habits")
        count = cursor.fetchone()["cnt"]
        if count == 0:
            print("[INFO] No habits found. Populating test data...")
            predefined = [
                ("Drink Water", "daily"),
                ("Exercise", "daily"),
                ("Read Book", "daily"),
                ("Weekly House Cleaning", "weekly"),
                ("Weekly Grocery Shopping", "weekly")
            ]
            for hname, p in predefined:
                self.create_habit(hname, p)
            # Add completions for the past 4 weeks.
            for habit in self.habits.values():
                if habit.periodicity == "daily":
                    for i in range(28):
                        ts = (datetime.now() - timedelta(days=(28 - i))).isoformat()
                        habit_id = self.get_habit_id(habit.name)
                        with self.connection:
                            self.connection.execute(
                                "INSERT INTO completions (habit_id, completion_date) VALUES (?, ?)",
                                (habit_id, ts)
                            )
                        habit.completions.append(ts)
                else:
                    for i in range(4):
                        ts = (datetime.now() - timedelta(weeks=(4 - i))).isoformat()
                        habit_id = self.get_habit_id(habit.name)
                        with self.connection:
                            self.connection.execute(
                                "INSERT INTO completions (habit_id, completion_date) VALUES (?, ?)",
                                (habit_id, ts)
                            )
                        habit.completions.append(ts)
            print("[INFO] Test data populated.")
            self.commit_changes()
