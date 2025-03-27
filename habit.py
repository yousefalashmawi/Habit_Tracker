
class Habit:
    def __init__(self, name, periodicity, creation_date, completions=None):

        self.name = name
        self.periodicity = periodicity
        self.creation_date = creation_date
        self.completions = completions if completions else []

    def add_completion(self, timestamp):
        """Adds a new completion timestamp to the habit."""
        self.completions.append(timestamp)
