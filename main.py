
import sys
from habit_manager import HabitManager
from analytics import (
    list_all_habits,
    filter_by_periodicity,
    longest_run_streak_all,
    longest_run_streak_for_habit
)

def main():
    manager = HabitManager()
    manager.populate_test_data_if_empty()

    while True:
        print("\n=== HABIT TRACKER MENU ===")
        print("1) Create Habit")
        print("2) Mark Habit Completion")
        print("3) Delete Habit")
        print("4) List All Habits")
        print("5) Analytics")
        print("6) Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            name = input("Enter habit name: ").strip()
            periodicity = input("Enter periodicity (daily/weekly): ").strip().lower()
            if periodicity not in ("daily", "weekly"):
                print("[ERROR] Periodicity must be 'daily' or 'weekly'.")
                continue
            if manager.create_habit(name, periodicity):
                print(f"[INFO] Habit '{name}' created successfully.")
            else:
                print(f"[WARNING] A habit named '{name}' already exists.")

        elif choice == "2":
            if not manager.habits:
                print("[WARNING] No habits found.")
                continue
            print("Available Habits:")
            for i, hname in enumerate(manager.habits.keys(), start=1):
                print(f"{i}) {hname}")
            selection = input("Select a habit number: ").strip()
            try:
                index = int(selection) - 1
                names = list(manager.habits.keys())
                if 0 <= index < len(names):
                    chosen_name = names[index]
                    if manager.mark_completion(chosen_name):
                        print(f"[INFO] Completion recorded for '{chosen_name}'.")
                    else:
                        print("[ERROR] Failed to mark completion.")
                else:
                    print("[ERROR] Invalid selection.")
            except ValueError:
                print("[ERROR] Please enter a valid number.")

        elif choice == "3":
            if not manager.habits:
                print("[WARNING] No habits found.")
                continue
            print("Available Habits:")
            for i, hname in enumerate(manager.habits.keys(), start=1):
                print(f"{i}) {hname}")
            selection = input("Select a habit number to delete: ").strip()
            try:
                index = int(selection) - 1
                names = list(manager.habits.keys())
                if 0 <= index < len(names):
                    chosen_name = names[index]
                    if manager.delete_habit(chosen_name):
                        print(f"[INFO] Habit '{chosen_name}' deleted.")
                    else:
                        print("[ERROR] Failed to delete habit.")
                else:
                    print("[ERROR] Invalid selection.")
            except ValueError:
                print("[ERROR] Please enter a valid number.")

        elif choice == "4":
            all_habits = manager.list_habits()
            if not all_habits:
                print("[WARNING] No habits to list.")
            else:
                for habit in all_habits:
                    print(f"- {habit.name} ({habit.periodicity}), created: {habit.creation_date}, "
                          f"completions: {len(habit.completions)}")

        elif choice == "5":
            print("\n--- ANALYTICS MENU ---")
            print("1) List all habits")
            print("2) Filter by periodicity (daily/weekly)")
            print("3) Longest run streak (all habits)")
            print("4) Longest run streak (specific habit)")
            print("5) Return to main menu")
            sub_choice = input("Enter choice: ").strip()

            if sub_choice == "1":
                all_habit_data = list_all_habits(manager.list_habits())
                if not all_habit_data:
                    print("[INFO] No habits found.")
                else:
                    for name, periodicity, creation_date in all_habit_data:
                        print(f"- Name: {name}, Periodicity: {periodicity}, Created: {creation_date}")
            elif sub_choice == "2":
                p = input("Enter periodicity (daily/weekly): ").strip().lower()
                filtered = filter_by_periodicity(manager.list_habits(), p)
                if not filtered:
                    print(f"[INFO] No habits with periodicity '{p}' found.")
                else:
                    for h in filtered:
                        print(f"- {h.name} (Created: {h.creation_date}, Completions: {len(h.completions)})")
            elif sub_choice == "3":
                best_habits, max_streak = longest_run_streak_all(manager.list_habits())
                if max_streak == 0:
                    print("[INFO] No completions or no habits found.")
                else:
                    print(f"Longest streak: {max_streak}")
                    print("Habit(s) with longest streak:")
                    for name in best_habits:
                        print(f" - {name}")
            elif sub_choice == "4":
                names = list(manager.habits.keys())
                if not names:
                    print("[INFO] No habits found.")
                else:
                    print("Available Habits:")
                    for i, hname in enumerate(names, start=1):
                        print(f"{i}) {hname}")
                    selection = input("Select a habit number: ").strip()
                    try:
                        index = int(selection) - 1
                        if 0 <= index < len(names):
                            habit = manager.habits[names[index]]
                            streak = longest_run_streak_for_habit(habit)
                            print(f"[INFO] Longest streak for '{habit.name}' is {streak}.")
                        else:
                            print("[ERROR] Invalid selection.")
                    except ValueError:
                        print("[ERROR] Please enter a valid number.")
            else:
                continue  # Go back to main menu

        elif choice == "6":
            manager.commit_changes()
            manager.close()
            print("[INFO] Exiting program. Goodbye!")
            sys.exit(0)

        else:
            print("[ERROR] Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
