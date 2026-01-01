# Tasks: Advanced Level Tasks (Recurring & Reminders)

**Input**: Design documents from `/specs/3-advanced-tasks/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Todo Console App**: `src/todo3/main.py` (entry point), `src/todo3/models.py`, `src/todo3/service.py`, `src/todo3/cli.py`
- **Tests**: `tests/unit/`, `tests/integration/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan in src/todo3/
- [x] T002 Initialize Python project with standard library only in src/todo3/
- [ ] T003 [P] Configure linting and formatting tools

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [x] T004 Create in-memory data structure for task storage in src/todo3/
- [x] T005 [P] Implement task model with ID, title, description, and completion status in src/todo3/models.py
- [x] T006 [P] Setup command-line interface structure in src/todo3/cli.py
- [x] T007 Create base models/entities that all stories depend on in src/todo3/models.py
- [ ] T008 Configure error handling and logging infrastructure in src/todo3/
- [x] T009 Setup application entry point and main loop in src/todo3/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Recurring Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to mark tasks as recurring so that they automatically reappear after completion, ensuring they don't forget regular activities like daily habits or weekly meetings.

**Independent Test**: Can be fully tested by creating a recurring task, completing it, and verifying that a new occurrence is automatically generated. This delivers value by reducing the need to manually recreate regular tasks.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T010 [P] [US1] Contract test for recurring task endpoint in tests/contract/test_recurring.py
- [ ] T011 [P] [US1] Integration test for recurring functionality in tests/integration/test_recurring.py

### Implementation for User Story 1

- [x] T012 [P] [US1] Update Task model to include recurring fields in src/todo3/models.py
- [x] T013 [P] [US1] Create RecurrencePattern enum in src/todo3/models.py
- [x] T014 [US1] Implement complete_recurring_task method in src/todo3/service.py
- [x] T015 [US1] Implement calculate_next_occurrence method in src/todo3/service.py
- [x] T016 [US1] Implement command-line interface for recurring tasks in src/todo3/cli.py
- [ ] T017 [US1] Add validation for recurring task updates in src/todo3/models.py
- [ ] T018 [US1] Add logging for recurring task operations in src/todo3/service.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Due Dates with Time (Priority: P2)

**Goal**: Enable users to assign specific due dates and times to tasks so that they can manage their schedule more effectively.

**Independent Test**: Can be fully tested by creating tasks with due dates and times, and verifying they can be viewed and sorted by due date. This delivers value by helping users prioritize time-sensitive tasks.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T019 [P] [US2] Contract test for due date assignment endpoint in tests/contract/test_due_dates.py
- [ ] T020 [P] [US2] Integration test for due date functionality in tests/integration/test_due_dates.py

### Implementation for User Story 2

- [x] T021 [P] [US2] Enhance Task model with due date field in src/todo3/models.py
- [x] T022 [US2] Implement set_task_due_date method in src/todo3/service.py
- [x] T023 [US2] Implement get_overdue_tasks method in src/todo3/service.py
- [x] T024 [US2] Implement get_tasks_due_soon method in src/todo3/service.py
- [x] T025 [US2] Implement command-line interface for due dates in src/todo3/cli.py
- [ ] T026 [US2] Add validation for due date operations in src/todo3/models.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Time-Based Reminders (Priority: P3)

**Goal**: Enable users to receive browser notifications for tasks at their due time so that they're reminded to complete time-sensitive tasks.

**Independent Test**: Can be fully tested by setting up a task with a due date/time in the near future, enabling reminders, and verifying that a browser notification appears at the scheduled time. This delivers value by helping users stay on track with their commitments.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T027 [P] [US3] Contract test for reminder endpoint in tests/contract/test_reminders.py
- [ ] T028 [P] [US3] Integration test for reminder functionality in tests/integration/test_reminders.py

### Implementation for User Story 3

- [x] T029 [P] [US3] Implement reminder functionality in src/todo3/service.py
- [x] T030 [US3] Implement command-line interface for reminders in src/todo3/cli.py
- [ ] T031 [US3] Add notification permission handling in src/todo3/service.py
- [ ] T032 [US3] Add reminder validation in src/todo3/service.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T033 [P] README.md documentation updates with new command usage
- [ ] T034 Code cleanup and refactoring
- [ ] T035 Performance optimization across all stories
- [ ] T036 [P] Additional unit tests (if requested) in tests/unit/
- [ ] T037 Error handling improvements
- [ ] T038 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
T010 [P] [US1] Contract test for recurring task endpoint in tests/contract/test_recurring.py
T011 [P] [US1] Integration test for recurring functionality in tests/integration/test_recurring.py

# Launch all models for User Story 1 together:
T012 [P] [US1] Update Task model to include recurring fields in src/todo3/models.py
T013 [P] [US1] Create RecurrencePattern enum in src/todo3/models.py
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence