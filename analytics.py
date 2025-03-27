

from datetime import datetime, timedelta


def list_all_habits(habits_list):

    return [(h.name, h.periodicity, h.creation_date) for h in habits_list]


def filter_by_periodicity(habits_list, periodicity):

    return [h for h in habits_list if h.periodicity == periodicity]


def compute_longest_streak(habit):

    if not habit.completions:
        return 0

    sorted_completions = sorted(habit.completions)
    dt_completions = [datetime.fromisoformat(ts) for ts in sorted_completions]

    expected_delta = timedelta(days=1) if habit.periodicity == "daily" else timedelta(weeks=1)
    longest_streak = 1
    current_streak = 1

    for i in range(1, len(dt_completions)):
        diff = dt_completions[i].date() - dt_completions[i - 1].date()
        if diff <= expected_delta:
            current_streak += 1
        else:
            longest_streak = max(longest_streak, current_streak)
            current_streak = 1

    return max(longest_streak, current_streak)


def longest_run_streak_all(habits_list):
    max_streak = 0
    best_habits = []
    for habit in habits_list:
        streak = compute_longest_streak(habit)
        if streak > max_streak:
            max_streak = streak
            best_habits = [habit.name]
        elif streak == max_streak and streak != 0:
            best_habits.append(habit.name)
    return best_habits, max_streak


def longest_run_streak_for_habit(habit):

    return compute_longest_streak(habit)
