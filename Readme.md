# Task Management Console

## Problem Statement
Keeping track of everyday tasks, deadlines, and priorities can easily become confusing. Without validation, bad date entries or missing details make task tracking unreliable.

## Objective
To build a functional command-line Python program that helps users create, filter, update, and manage tasks with data validation and file storage.

## Features
* **Add Tasks:** Create tasks with title, priority (Low/Medium/High), and due date (YYYY-MM-DD).
* **View & Filter:** View all tasks sorted by due date, or search using keywords, priority, or status.
* **Update & Delete:** Update task progress (Pending, In Progress, Completed) or remove tasks.
* **Overdue Alerts:** Automatically flags tasks as overdue if their due date has passed.
* **Data Persistence:** Automatically saves and loads task data to `tasks.json`.

## Technologies Used
* **Python 3** (Standard modules: `json`, `os`, `datetime`, `unittest`)

## Installation & Setup
1. Download Python 3 if not already installed.
2. Clone or download project files into a folder.

## How to Run
Run this command in terminal/command prompt:
bash
python task_manager.py

##How to Run Tests
Bash
python -m unittest test_tasks.py

##Project Structure
├── task_manager.py     # Main application file
├── test_tasks.py       # Unit test file
├── tasks.json          # Persistent database file (Auto-generated)
└── README.md           # Documentation