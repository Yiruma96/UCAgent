# Auto-Generate ToDo from Stage Tasks

## Overview

UCAgent now supports automatically generating ToDo lists from stage tasks defined in `default.yaml`. This functionality is implemented through the new `AutoCreateToDoFromStage` tool.

## Background

In UCAgent, each verification stage has a corresponding task list (task) defined in the `default.yaml` configuration file. Previously, although the system provided the `CreateToDo` tool to create task lists, these ToDos had to be created manually and were not directly linked to the tasks defined in stages.

**User Question:** "Tasks for each stage are defined in default.yaml. I want to know if the create_todo process is generated based on these tasks?"

**Answer:** Before this feature was implemented, the answer was **No**. The `CreateToDo` tool needed to be called manually and would not automatically generate based on stage tasks. However, now through the new `AutoCreateToDoFromStage` tool, this functionality can be achieved.

## New Features

### 1. Auto-Generate ToDo Method

A new method `auto_create_todo_from_stage` has been added to the `StageManager` class:

```python
def auto_create_todo_from_stage(self, stage_index=None):
    """
    Automatically create a ToDo list from the current stage's tasks.
    This generates ToDo items based on the task list defined in the stage configuration.
    
    Args:
        stage_index: Optional stage index. If None, uses current stage.
        
    Returns:
        str: Result message from the ToDo creation
    """
```

This method will:
1. Read the task list from the specified stage (or current stage)
2. Use the stage description as the ToDo task description
3. Use each task defined in the stage as a ToDo step
4. Automatically create a structured ToDo list

### 2. New Tool: AutoCreateToDoFromStage

A new tool class `ToolAutoCreateToDoFromStage` has been added, allowing AI Agents or users to invoke this functionality:

```python
class ToolAutoCreateToDoFromStage(ManagerTool):
    """Automatically create a ToDo list from stage tasks."""
    name: str = "AutoCreateToDoFromStage"
    description: str = (
        "Automatically create a ToDo list based on the tasks defined in a stage's configuration (from default.yaml). \n"
        "This tool reads the task list from the stage configuration and creates a structured ToDo with those tasks as steps. \n"
        "By default, it creates a ToDo from the current stage. You can specify a stage_index to create from a different stage. \n"
        "This is useful for quickly setting up a ToDo that matches the stage's defined workflow. \n"
        "Returns the result of the ToDo creation."
    )
```

### 3. Usage Conditions

This tool is only available when the following conditions are met:
- `force_todo` flag is enabled
- `todo_panel` is initialized

## Usage

### Method 1: Using the Tool (Recommended)

When `force_todo` is enabled, AI Agents can directly call the `AutoCreateToDoFromStage` tool:

```python
# Auto-create ToDo from current stage
AutoCreateToDoFromStage()

# Create ToDo from a specific stage
AutoCreateToDoFromStage(stage_index=2)
```

### Method 2: Programmatic Invocation

```python
# Call in StageManager instance
stage_manager.auto_create_todo_from_stage()  # Use current stage
stage_manager.auto_create_todo_from_stage(stage_index=1)  # Use specific stage
```

## Example

Suppose the following stage is defined in `default.yaml`:

```yaml
stage:
  - name: requirement_analysis_and_planning
    desc: "Requirement Analysis and Verification Planning"
    task:
      - "Step 1: Read {DUT}/README.md and understand verification requirements"
      - "Step 2: Define verification objectives - what features to test? What are inputs/outputs?"
      - "Step 3: Identify risk points - where can errors occur? What are boundary conditions?"
      - "Step 4: Develop verification plan - how to systematically test all features?"
      - "Step 5: Write verification planning document to {OUT}/{DUT}_verification_needs_and_plan.md"
```

After calling `AutoCreateToDoFromStage()`, a ToDo will be automatically created with:
- **Task Description**: "Stage 0: Requirement Analysis and Verification Planning"
- **Step List**: Contains the 5 task steps listed above

## Relationship with Original CreateToDo

1. **CreateToDo**: Manually create custom ToDos, suitable for scenarios requiring flexible task definition
2. **AutoCreateToDoFromStage**: Automatically generate ToDo from stage configuration, suitable for quickly starting stage work

Both tools can be used together:
- Use `AutoCreateToDoFromStage` to quickly generate a base ToDo
- Use `CreateToDo` to create additional custom ToDos as needed (will overwrite existing ToDo)
- Use `CompleteToDoSteps`, `UndoToDoSteps`, and other tools to manage ToDo progress

## Implementation Details

### Code Location

- Core method: `StageManager.auto_create_todo_from_stage()` in `vagent/stage/vmanager.py`
- Tool class: `ToolAutoCreateToDoFromStage` in `vagent/stage/vmanager.py`
- Tool function: `StageManager.tool_auto_create_todo_from_stage()` in `vagent/stage/vmanager.py`

### Tool Registration

The tool is registered in the `StageManager.new_tools()` method and is only added to the tool list when both `force_todo` and `todo_panel` are available.

## Notes

1. **ToDo Overwriting**: Creating a new ToDo will overwrite existing ToDos, use with caution
2. **Task Length Limits**: ToDo step count and length have limits (default max 20 steps, max 100 characters per step)
3. **Empty Task Handling**: If a stage has no defined tasks, the tool will return an error message
4. **Stage Index**: stage_index must be a valid index (0 to number of stages - 1)

## Testing

Test file: `tests/test_auto_todo_from_stage.py`

Test scenarios included:
- Basic auto-generation of ToDo
- Scenario when todo_panel is not initialized
- Scenario when stage has no tasks
- Invalid stage index scenario
- Default usage of current stage scenario

## Future Improvements

1. Automatically prompt whether to create ToDo when switching stages
2. Support ToDo templates, allowing custom generation rules
3. Support merging tasks from multiple stages into one ToDo
4. Provide automatic synchronization mechanism between ToDo and stage progress
