# Changelog

All notable changes to UCAgent will be documented in this file.

## [Unreleased]

### Added
- **Auto-Generate ToDo from Stage Tasks**: New `AutoCreateToDoFromStage` tool that automatically creates ToDo lists based on tasks defined in stage configurations (default.yaml)
  - Added `auto_create_todo_from_stage()` method to `StageManager` class
  - New tool `ToolAutoCreateToDoFromStage` available when `force_todo` is enabled
  - Supports creating ToDo from current stage or any specific stage by index
  - See documentation: `docs/AUTO_TODO_FROM_STAGE.md` and `docs/AUTO_TODO_EXAMPLES.md`

### Changed
- Enhanced `StageManager.new_tools()` to conditionally register `AutoCreateToDoFromStage` tool when ToDo features are enabled

### Documentation
- Added Chinese documentation: `docs/AUTO_TODO_FROM_STAGE.md`
- Added English documentation: `docs/AUTO_TODO_FROM_STAGE_EN.md`
- Added usage examples: `docs/AUTO_TODO_EXAMPLES.md`

### Testing
- Added comprehensive test suite: `tests/test_auto_todo_from_stage.py`

---

## Background

This feature was added in response to a user question: "Tasks for each stage are defined in default.yaml. Does the create_todo process get generated based on these tasks?"

Previously, the answer was **no** - ToDo items had to be manually created using the `CreateToDo` tool. With this new feature, users can now automatically generate ToDo lists from stage task definitions, streamlining the workflow and ensuring consistency between stage configurations and task planning.
