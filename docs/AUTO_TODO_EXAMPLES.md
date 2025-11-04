# AutoCreateToDoFromStage 使用示例 / Usage Examples

## 中文示例

### 场景1：开始新的验证阶段

当你进入一个新的验证阶段时，可以快速从stage配置生成ToDo：

```python
# 假设当前在stage 0
# 使用工具自动创建ToDo
result = AutoCreateToDoFromStage()
```

输出示例：
```
ToDo created successfully!

-------- ToDo List --------
 Task Description: Stage 0: 需求分析与验证规划
 Steps:
  1: 第1步：读取{DUT}/README.md，理解用户的验证要求
  2: 第2步：确定验证目标 - 需要测试哪些功能？输入输出是什么？
  3: 第3步：识别风险点 - 哪些地方容易出错？边界条件有哪些？
  4: 第4步：制定验证计划 - 如何系统地测试所有功能？
  5: 第5步：写入验证规划文档到{OUT}/{DUT}_verification_needs_and_plan.md
 Created At: 2024-01-15 10:30:00
 Updated At: 2024-01-15 10:30:00
 Notes: None
----------------------------
```

### 场景2：为特定阶段创建ToDo

如果你想为非当前阶段创建ToDo（比如提前规划）：

```python
# 为stage 3创建ToDo
result = AutoCreateToDoFromStage(stage_index=3)
```

### 场景3：与其他ToDo工具配合使用

```python
# 1. 从stage自动生成基础ToDo
AutoCreateToDoFromStage()

# 2. 完成一些步骤
CompleteToDoSteps(completed_steps=[1, 2])

# 3. 查看当前进度
GetToDoSummary()

# 4. 如果需要，撤销某个步骤
UndoToDoSteps(steps=[2])

# 5. 如果需要完全自定义的ToDo，可以重新创建
CreateToDo(
    task_description="自定义任务",
    steps=["步骤1", "步骤2", "步骤3"]
)
```

## English Examples

### Scenario 1: Starting a New Verification Stage

When entering a new verification stage, quickly generate a ToDo from stage configuration:

```python
# Assuming currently at stage 0
# Use tool to auto-create ToDo
result = AutoCreateToDoFromStage()
```

Example output:
```
ToDo created successfully!

-------- ToDo List --------
 Task Description: Stage 0: Requirement Analysis and Verification Planning
 Steps:
  1: Step 1: Read {DUT}/README.md and understand verification requirements
  2: Step 2: Define verification objectives - what features to test?
  3: Step 3: Identify risk points - where can errors occur?
  4: Step 4: Develop verification plan - how to test systematically?
  5: Step 5: Write verification planning document
 Created At: 2024-01-15 10:30:00
 Updated At: 2024-01-15 10:30:00
 Notes: None
----------------------------
```

### Scenario 2: Create ToDo for Specific Stage

If you want to create a ToDo for a non-current stage (e.g., advance planning):

```python
# Create ToDo for stage 3
result = AutoCreateToDoFromStage(stage_index=3)
```

### Scenario 3: Using with Other ToDo Tools

```python
# 1. Auto-generate base ToDo from stage
AutoCreateToDoFromStage()

# 2. Complete some steps
CompleteToDoSteps(completed_steps=[1, 2])

# 3. Check current progress
GetToDoSummary()

# 4. Undo a step if needed
UndoToDoSteps(steps=[2])

# 5. Create a completely custom ToDo if needed (overwrites existing)
CreateToDo(
    task_description="Custom Task",
    steps=["Step 1", "Step 2", "Step 3"]
)
```

## 命令行使用 / Command Line Usage

当使用UCAgent时，如果启用了`--force-todo`选项，AI Agent将可以访问此工具：

```bash
# 启动UCAgent时启用ToDo功能
ucagent <workspace> <dut_name> --force-todo

# 或者在配置中设置
python ucagent.py --workspace ./output --dut Adder --force-todo
```

## 编程调用 / Programmatic Usage

如果你在代码中使用StageManager：

```python
from vagent.stage.vmanager import StageManager
from vagent.tools.planning import ToDoPanel

# 初始化（简化示例）
todo_panel = ToDoPanel()
stage_manager = StageManager(
    workspace="./output",
    cfg=config,
    agent=agent,
    tool_read_text=read_tool,
    ucagent_info={},
    force_todo=True,  # 启用ToDo功能
    todo_panel=todo_panel
)

# 从当前stage自动创建ToDo
result = stage_manager.auto_create_todo_from_stage()
print(result)

# 从指定stage创建ToDo
result = stage_manager.auto_create_todo_from_stage(stage_index=2)
print(result)
```

## 错误处理 / Error Handling

### 错误示例1：TodoPanel未初始化

```python
# 如果todo_panel为None
result = AutoCreateToDoFromStage()
# 输出: "ToDo panel is not initialized. Cannot create ToDo from stage tasks."
```

### 错误示例2：Stage没有定义任务

```python
# 如果某个stage在default.yaml中没有task列表
result = AutoCreateToDoFromStage(stage_index=10)
# 输出: "Stage 'stage_name' has no tasks defined. Cannot create ToDo."
```

### 错误示例3：无效的Stage索引

```python
# 如果stage_index超出范围
result = AutoCreateToDoFromStage(stage_index=999)
# 输出: "Invalid stage index. Cannot create ToDo from stage tasks."
```

## 最佳实践 / Best Practices

1. **在阶段开始时使用**: 当进入新stage时立即调用`AutoCreateToDoFromStage()`来获得结构化的工作计划
2. **定期更新进度**: 使用`CompleteToDoSteps`标记已完成的任务
3. **保持简洁**: 如果stage的任务过多（>20个），考虑在default.yaml中重新组织stage结构
4. **配合其他工具**: 与`CurrentTips`、`Check`、`Complete`等工具配合使用，形成完整的工作流
5. **文档化特殊情况**: 如果需要偏离stage定义的任务，在notes中记录原因

## 与Stage工作流集成 / Integration with Stage Workflow

```python
# 典型的工作流
# 1. 查看当前阶段
CurrentTips()

# 2. 自动创建ToDo
AutoCreateToDoFromStage()

# 3. 开始工作，逐步完成任务
CompleteToDoSteps(completed_steps=[1])
# ... 执行任务1 ...

CompleteToDoSteps(completed_steps=[2])
# ... 执行任务2 ...

# 4. 检查阶段是否完成
Check()

# 5. 完成当前阶段
Complete()

# 6. 进入下一阶段，重复流程
CurrentTips()
AutoCreateToDoFromStage()
```
