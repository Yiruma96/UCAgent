# 自动从Stage任务生成ToDo功能

## 概述

UCAgent现在支持从`default.yaml`中定义的stage任务自动生成ToDo列表。这个功能通过新增的`AutoCreateToDoFromStage`工具实现。

## 问题背景

在UCAgent中，每个验证阶段（stage）都在`default.yaml`配置文件中定义了相应的任务列表（task）。之前，虽然系统提供了`CreateToDo`工具来创建任务清单，但这些ToDo需要手动创建，与stage中定义的任务没有直接关联。

用户提出的问题：**"在default.yaml里面定义了每个stage的task，我想知道create_todo的过程会基于这个task来生成吗？"**

**答案：** 在此功能实现之前，答案是**否**。`CreateToDo`工具需要手动调用，不会自动基于stage的任务生成。但现在，通过新增的`AutoCreateToDoFromStage`工具，可以实现这个功能。

## 新增功能

### 1. 自动生成ToDo的方法

在`StageManager`类中新增了`auto_create_todo_from_stage`方法：

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

此方法会：
1. 读取指定stage（或当前stage）的任务列表
2. 将stage的描述作为ToDo的任务描述
3. 将stage中定义的每个任务作为ToDo的步骤
4. 自动创建一个结构化的ToDo列表

### 2. 新增工具：AutoCreateToDoFromStage

新增了一个工具类`ToolAutoCreateToDoFromStage`，允许AI Agent或用户调用此功能：

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

### 3. 使用条件

此工具只在满足以下条件时可用：
- `force_todo`标志被启用
- `todo_panel`已初始化

## 使用方式

### 方式1：使用工具（推荐）

当`force_todo`启用时，AI Agent可以直接调用`AutoCreateToDoFromStage`工具：

```python
# 从当前stage自动创建ToDo
AutoCreateToDoFromStage()

# 从指定stage创建ToDo
AutoCreateToDoFromStage(stage_index=2)
```

### 方式2：编程方式调用

```python
# 在StageManager实例中调用
stage_manager.auto_create_todo_from_stage()  # 使用当前stage
stage_manager.auto_create_todo_from_stage(stage_index=1)  # 使用指定stage
```

## 示例

假设`default.yaml`中定义了以下stage：

```yaml
stage:
  - name: requirement_analysis_and_planning
    desc: "需求分析与验证规划"
    task:
      - "第1步：读取{DUT}/README.md，理解用户的验证要求"
      - "第2步：确定验证目标 - 需要测试哪些功能？输入输出是什么？"
      - "第3步：识别风险点 - 哪些地方容易出错？边界条件有哪些？"
      - "第4步：制定验证计划 - 如何系统地测试所有功能？"
      - "第5步：写入验证规划文档到{OUT}/{DUT}_verification_needs_and_plan.md"
```

调用`AutoCreateToDoFromStage()`后，会自动创建一个ToDo，其中：
- **任务描述**: "Stage 0: 需求分析与验证规划"
- **步骤列表**: 包含上述5个任务步骤

## 与原有CreateToDo的关系

1. **CreateToDo**: 手动创建自定义ToDo，适用于需要灵活定义任务的场景
2. **AutoCreateToDoFromStage**: 自动从stage配置生成ToDo，适用于快速启动stage工作的场景

两个工具可以配合使用：
- 使用`AutoCreateToDoFromStage`快速生成基础ToDo
- 根据需要使用`CreateToDo`创建额外的自定义ToDo（会覆盖现有ToDo）
- 使用`CompleteToDoSteps`、`UndoToDoSteps`等工具管理ToDo进度

## 实现细节

### 代码位置

- 核心方法：`vagent/stage/vmanager.py` 中的 `StageManager.auto_create_todo_from_stage()`
- 工具类：`vagent/stage/vmanager.py` 中的 `ToolAutoCreateToDoFromStage`
- 工具函数：`vagent/stage/vmanager.py` 中的 `StageManager.tool_auto_create_todo_from_stage()`

### 工具注册

工具在`StageManager.new_tools()`方法中注册，只有在`force_todo`和`todo_panel`都可用时才会添加到工具列表中。

## 注意事项

1. **ToDo覆盖**: 创建新的ToDo会覆盖现有的ToDo，请谨慎使用
2. **任务长度限制**: ToDo中的步骤数量和长度有限制（默认最多20步，每步最多100字符）
3. **空任务处理**: 如果stage没有定义任务，工具会返回错误信息
4. **stage索引**: stage_index必须是有效的索引（0到stages数量-1）

## 测试

测试文件：`tests/test_auto_todo_from_stage.py`

包含的测试场景：
- 基本的ToDo自动生成
- 没有初始化todo_panel的情况
- stage任务为空的情况
- 无效stage索引的情况
- 默认使用当前stage的情况

## 未来改进方向

1. 在stage切换时自动提示是否创建ToDo
2. 支持ToDo模板，允许自定义生成规则
3. 支持合并多个stage的任务到一个ToDo
4. 提供ToDo与stage进度的自动同步机制
