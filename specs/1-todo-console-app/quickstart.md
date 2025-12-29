# Quickstart Guide: Todo Console Application

## Running the Application

1. Ensure Python 3.13+ is installed on your system
2. Navigate to the project root directory
3. Run the application with the command:
   ```
   python src/main.py
   ```

## Using the Application

When the application starts, you'll see a menu with the following options:

1. **Add Task**: Creates a new task with a required title and optional description
2. **View Tasks**: Displays all tasks with their ID, title, and completion status
3. **Update Task**: Modifies an existing task's title and/or description
4. **Delete Task**: Removes a task by its ID
5. **Mark Complete/Incomplete**: Toggles a task's completion status
6. **Exit**: Closes the application

### Example Workflow

1. Start the application: `python src/main.py`
2. Select "1" to add a task
3. Enter a title (required) and description (optional)
4. Select "2" to view all tasks
5. Continue using other options as needed
6. Select "6" to exit the application

## Important Notes

- All data is stored in memory only and will be lost when the application exits
- Task IDs are assigned sequentially during runtime and remain stable until the application is closed
- Invalid inputs will result in error messages prompting for valid input