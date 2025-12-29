# Data Model: Todo Console Application

## Task Entity

The core entity for the Todo application is the Task, which has the following properties:

### Properties
- **ID**: Integer, unique identifier assigned sequentially during runtime
- **Title**: String (required), the main text of the task
- **Description**: String (optional), additional details about the task
- **Completion Status**: Boolean, indicating whether the task is complete (True) or incomplete (False)

### State Transitions
- A task starts with Completion Status as False (incomplete)
- The status can be toggled between False (incomplete) and True (complete)

### Relationships
- No relationships with other entities in this simple implementation