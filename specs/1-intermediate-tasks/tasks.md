# Tasks: Intermediate Level Tasks (Organization & Usability)

**Input**: Design documents from `/specs/1-intermediate-tasks/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Todo Console App**: `src/todo2/main.py` (entry point), `src/todo2/models.py`, `src/todo2/service.py`, `src/todo2/cli.py`
- **Tests**: `tests/unit/`, `tests/integration/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan in src/todo2/
- [x] T002 Initialize Python project with standard library only in src/todo2/
- [ ] T003 [P] Configure linting and formatting tools

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [ ] T004 Create in-memory data structure for task storage
- [x] T005 [P] Implement task model with ID, title, description, and completion status in src/todo2/models.py
- [x] T006 [P] Setup command-line interface structure in src/todo2/cli.py
- [x] T007 Create base models/entities that all stories depend on in src/todo2/models.py
- [ ] T008 Configure error handling and logging infrastructure in src/todo2/
- [x] T009 Setup application entry point and main loop in src/todo2/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Prioritize Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to assign priority levels (High, Medium, Low) to tasks so they can focus on the most important items first.

**Independent Test**: Can be fully tested by adding tasks with different priority levels and verifying they can be displayed and filtered by priority. This delivers immediate value by allowing users to identify urgent tasks.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T010 [P] [US1] Contract test for priority setting endpoint in tests/contract/test_priority.py
- [ ] T011 [P] [US1] Integration test for priority functionality in tests/integration/test_priority.py

### Implementation for User Story 1

- [x] T012 [P] [US1] Update Task model to include priority field in src/todo2/models.py
- [x] T013 [P] [US1] Create Priority enum in src/todo2/models.py
- [x] T014 [US1] Implement update_task_priority method in src/todo2/service.py
- [x] T015 [US1] Implement get_tasks_by_priority method in src/todo2/service.py
- [x] T016 [US1] Implement command-line interface for setting priority in src/todo2/cli.py
- [ ] T017 [US1] Add validation for priority updates in src/todo2/models.py
- [ ] T018 [US1] Add logging for priority operations in src/todo2/service.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Tag Tasks (Priority: P2)

**Goal**: Enable users to assign tags or categories to tasks so they can group related tasks together.

**Independent Test**: Can be fully tested by adding tags to tasks and verifying they can be viewed and filtered by tags. This delivers value by allowing users to quickly find tasks related to specific contexts.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T019 [P] [US2] Contract test for tag assignment endpoint in tests/contract/test_tags.py
- [ ] T020 [P] [US2] Integration test for tagging functionality in tests/integration/test_tags.py

### Implementation for User Story 2

- [x] T021 [P] [US2] Enhance Task model with tags field in src/todo2/models.py
- [x] T022 [US2] Implement add_tag_to_task method in src/todo2/service.py
- [ ] T023 [US2] Implement remove_tag_from_task method in src/todo2/service.py
- [x] T024 [US2] Implement get_tasks_by_tag method in src/todo2/service.py
- [x] T025 [US2] Implement command-line interface for tagging in src/todo2/cli.py
- [ ] T026 [US2] Add validation for tag operations in src/todo2/models.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Search Tasks (Priority: P3)

**Goal**: Enable users to search for tasks by keyword so they can quickly find specific tasks in a long list.

**Independent Test**: Can be fully tested by creating tasks with different titles/descriptions and searching for keywords. This delivers value by reducing the time needed to find specific tasks.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T027 [P] [US3] Contract test for search endpoint in tests/contract/test_search.py
- [ ] T028 [P] [US3] Integration test for search functionality in tests/integration/test_search.py

### Implementation for User Story 3

- [x] T029 [P] [US3] Implement search_tasks method in src/todo2/service.py
- [x] T030 [US3] Implement command-line interface for search in src/todo2/cli.py
- [x] T031 [US3] Add case-insensitive search functionality in src/todo2/service.py
- [ ] T032 [US3] Add search validation in src/todo2/service.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Filter Tasks (Priority: P4)

**Goal**: Enable users to filter tasks by different criteria so they can focus on specific subsets of tasks.

**Independent Test**: Can be fully tested by applying different filters and verifying the correct tasks are displayed. This delivers value by allowing users to focus on specific task categories.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T033 [P] [US4] Contract test for filtering endpoint in tests/contract/test_filter.py
- [ ] T034 [P] [US4] Integration test for filtering functionality in tests/integration/test_filter.py

### Implementation for User Story 4

- [x] T035 [P] [US4] Implement filter_tasks method in src/todo2/service.py
- [x] T036 [US4] Implement command-line interface for filtering in src/todo2/cli.py
- [x] T037 [US4] Add multiple filter combination logic in src/todo2/service.py
- [x] T038 [US4] Add filter validation in src/todo2/service.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: User Story 5 - Sort Tasks (Priority: P5)

**Goal**: Enable users to sort tasks by different criteria so they can view them in an order that makes sense for their workflow.

**Independent Test**: Can be fully tested by applying different sorting options and verifying tasks are displayed in the correct order. This delivers value by allowing users to organize tasks according to their preferences.

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [ ] T039 [P] [US5] Contract test for sorting endpoint in tests/contract/test_sort.py
- [ ] T040 [P] [US5] Integration test for sorting functionality in tests/integration/test_sort.py

### Implementation for User Story 5

- [x] T041 [P] [US5] Implement sort_tasks method in src/todo2/service.py
- [x] T042 [US5] Implement command-line interface for sorting in src/todo2/cli.py
- [x] T043 [US5] Add multiple sort criteria logic in src/todo2/service.py
- [x] T044 [US5] Add sort validation in src/todo2/service.py

**Checkpoint**: All user stories should now be functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T045 [P] README.md documentation updates with new command usage
- [ ] T046 Code cleanup and refactoring
- [ ] T047 Performance optimization across all stories
- [ ] T048 [P] Additional unit tests (if requested) in tests/unit/
- [ ] T049 Error handling improvements
- [ ] T050 Run quickstart.md validation

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
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - No dependencies on other stories

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
T010 [P] [US1] Contract test for priority setting endpoint in tests/contract/test_priority.py
T011 [P] [US1] Integration test for priority functionality in tests/integration/test_priority.py

# Launch all models for User Story 1 together:
T012 [P] [US1] Update Task model to include priority field in src/todo2/models.py
T013 [P] [US1] Create Priority enum in src/todo2/models.py
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
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
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