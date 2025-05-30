**File Purpose**: Define task workflow and development process

# Task Development Guide

## Quick Reference
- **T** = Task (feature or fix)
- **S** = Step (implementation step)
- **A** = Acceptance criteria

## Task Workflow

### 1. Start New Task
- Move previous task to Done section in `pm/tasks.md`
- Select next task from Future Tasks
- Move it to Current Task section

### 2. Plan Task
Define the task structure:
- Write clear Goals
- Define Scope (what's included/excluded)
- Break down into Steps (S1, S2, S3...)
- List Acceptance criteria (A1, A2, A3...)
- Add empty Notes section

### 3. Confirm with Client
Before proceeding:
- Review goals and scope with client
- Confirm acceptance criteria meet expectations
- Adjust based on feedback
- Get approval to proceed

### 4. Execute Steps

Work through each step sequentially:

#### For each step:
- Review relevant guides and patterns
- Implement following project standards
- Test the specific functionality
- Mark complete with [x] when done
- Add any decisions/issues to Notes

#### Development standards:
- Check `pm/design/components_guide.md` for patterns
- Follow coding guides in `pm/guides/`
- Use design tokens consistently
- Consider accessibility and responsive design
- If critical issues are encountered, pause development and check in with client

### 5. Verify & Complete
- Test against all acceptance criteria
- Ensure all steps show [x]
- Do final review of functionality
- Move task to Done section
- Update any affected documentation

## Common Commands Client May Issue Coding Agent
- "Start next task" - Move to new task from queue
- "Plan T03" - Create steps and acceptance criteria
- "Work on T03.S2" - Execute specific step
- "Complete T03" - Finalize and move to done