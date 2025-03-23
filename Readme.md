# Habit Tracker

A lightweight, command-line Habit Tracker application built with Python and SQLite. This tool allows users to create, manage, and analyze their habits, helping them build and maintain positive routines.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Development](#development)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Habit Tracker is designed to be simple yet effective, enabling users to track daily and weekly habits. The project is structured into modular components to ensure maintainability and ease of use. Users can perform core actions such as creating a habit, marking completions, deleting habits, and analyzing their progress through built-in analytics.

## Features

- **Create Habits:** Easily add new habits with a specified periodicity (daily or weekly).
- **Mark Completions:** Record the completion of a habit with a timestamp.
- **Delete Habits:** Remove habits and their associated completions.
- **List Habits:** View all tracked habits with details like creation date and total completions.
- **Analytics:** Analyze habit data, including:
  - Listing all habits
  - Filtering habits by periodicity
  - Calculating the longest run streak for individual or all habits

## Architecture

The project is divided into several modules:

- **habit.py:**  
  Contains the `Habit` class, representing individual habits and managing their state.

- **habit_manager.py:**  
  Manages database operations using SQLite. This module handles creating, updating, deleting, and loading habits from the database.

- **analytics.py:**  
  Provides functions for analyzing habits, such as filtering and streak calculations, using a functional programming style.

- **main.py:**  
  Acts as the command-line interface (CLI) for user interaction, orchestrating the functionality provided by the other modules.

A detailed flowchart and diagram of the application's structure can be found in the project documentation.

## Installation

### Prerequisites

- Python 3.x
- Git (for version control)

### Steps

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yousefalashmawi/Habit_Tracker.git
   cd Habit_Tracker
