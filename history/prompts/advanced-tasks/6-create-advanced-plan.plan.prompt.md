---
id: 6
title: Create Advanced Plan
stage: plan
date: 2026-01-01
surface: agent
model: gpt-4o
feature: advanced-tasks
branch: phase1
user: user
command: /sp.plan
labels: [plan, advanced, tasks]
links:
  spec: specs/3-advanced-tasks/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/3-advanced-tasks/plan.md
 - specs/3-advanced-tasks/research.md
 - specs/3-advanced-tasks/data-model.md
 - specs/3-advanced-tasks/quickstart.md
 - specs/3-advanced-tasks/contracts/api-contracts.md
tests:
 - null
---

## Prompt

```
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `.specify/scripts/powershell/setup-plan.ps1 -Json` from repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read FEATURE_SPEC and `.specify/memory/constitution.md`. Load IMPL_PLAN template (already copied).

3. **Execute plan workflow**: Follow the structure in IMPL_PLAN template to:
   - Fill Technical Context (mark unknowns as "NEEDS CLARIFICATION")
   - Fill Constitution Check section from constitution
   - Evaluate gates (ERROR if violations unjustified)
   - Phase 0: Generate research.md (resolve all NEEDS CLARIFICATION)
   - Phase 1: Generate data-model.md, contracts/, quickstart.md
   - Phase 1: Update agent context by running the agent script
   - Re-evaluate Constitution Check post-design

4. **Stop and report**: Command ends after Phase 2 planning. Report branch, IMPL_PLAN path, and generated artifacts.

## Phases

### Phase 0: Outline & Research

1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:

   ```text
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

### Phase 1: Design & Contracts

**Prerequisites:** `research.md` complete

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Agent context update**:
   - Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType qwen`
   - These scripts detect which AI agent is in use
   - Update the appropriate agent-specific context file
   - Add only new technology from current plan
   - Preserve manual additions between markers

**Output**: data-model.md, /contracts/*, quickstart.md, agent-specific file

## Key rules

- Use absolute paths
- ERROR on gate failures or unresolved clarifications

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage
   - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate Title and Determine Routing:
   - Generate Title: 3–7 words (slug for filename)
   - Route is automatically determined by stage:
     - `constitution` → `history/prompts/constitution/`
     - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
     - `general` → `history/prompts/general/`

3) Create and Fill PHR (Shell first; fallback agent‑native)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
   - If the script fails:
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
     - Allocate an ID; compute the output path based on stage from step 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4) Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.

## Response snapshot

I have successfully completed the implementation planning for the Advanced Level Tasks feature. Here's what was accomplished:

1. Created the implementation plan at `specs/3-advanced-tasks/plan.md` with:
   - Summary of the feature
   - Technical context including performance goals
   - Constitution check (all requirements met)
   - Project structure documentation

2. Created the research document at `specs/3-advanced-tasks/research.md` with:
   - Technical decisions for recurring task implementation
   - Technical decisions for due date and time implementation
   - Technical decisions for reminder implementation
   - Technology considerations

3. Created the data model at `specs/3-advanced-tasks/data-model.md` with:
   - Enhanced Task entity with recurring, due date, and reminder fields
   - RecurrencePattern enum definition
   - Reminder entity definition
   - FilterCriteria and SortCriteria entities
   - Validation rules and relationships

4. Created the quickstart guide at `specs/3-advanced-tasks/quickstart.md` with:
   - Implementation steps for each feature
   - Code examples for recurring task logic
   - Code examples for due date handling
   - Code examples for reminder functionality
   - CLI updates

5. Created API contracts at `specs/3-advanced-tasks/contracts/api-contracts.md` with:
   - Contract definitions for recurring task operations
   - Contract definitions for due date operations
   - Contract definitions for reminder operations

All required artifacts have been created and the constitution check has been satisfied.

## Outcome

- ✅ Impact: Complete implementation plan for Advanced Level features
- 🧪 Tests: No tests required for planning phase
- 📁 Files: plan.md, research.md, data-model.md, quickstart.md, and contracts created
- 🔁 Next prompts: Ready for task breakdown with `/sp.tasks`
- 🧠 Reflection: The plan is comprehensive and ready for the next phase

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin task breakdown with `/sp.tasks`