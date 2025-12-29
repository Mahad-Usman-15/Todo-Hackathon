# Todo In-Memory Python Console Application

This is a simple command-line Todo application that stores tasks only in memory, demonstrating Basic Level functionality using Spec-Driven Development.

## Project Overview

This application implements a basic Todo list with the following features:
- Add tasks with title and optional description
- View all tasks with ID, title, and completion status
- Update task title and/or description
- Delete tasks by ID
- Mark tasks as complete/incomplete

All data is stored only in memory and will be lost when the application exits.

## Setup Instructions

This project uses Python 3.13+ with only the standard library. No additional dependencies are required.

1. Clone the repository
2. Ensure you have Python 3.13+ installed
3. Run the application directly with Python

## How to Run the Application

```bash
python src/main.py
```

## Supported Commands

The application provides a console interface with the following commands:
- `add`: Add a new task
- `view`: View all tasks
- `update`: Update a task
- `delete`: Delete a task
- `complete`: Mark a task as complete
- `incomplete`: Mark a task as incomplete
- `help`: Show available commands
- `exit`: Exit the application

## Project Structure

```
src/
├── main.py          # Application entry point
├── todo/
│   ├── __init__.py
│   ├── models.py    # Task data model
│   ├── service.py   # Business logic
│   └── cli.py       # Console interaction
└── tests/
    ├── unit/
    └── integration/
```