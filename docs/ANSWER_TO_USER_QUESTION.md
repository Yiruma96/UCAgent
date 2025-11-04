# 关于"create_todo是否基于default.yaml中的stage task生成"的解答

## 问题

> 在default.yaml里面定义了每个stage的task，我想知道create_todo的过程会基于这个task来生成吗？

## 简短回答

**在本次功能实现之前：不会。**

**现在（实现新功能后）：可以。**

## 详细说明

### 1. 原有行为

在UCAgent的原有实现中：

- `default.yaml` 中定义了每个stage的任务列表（`task`字段）
- 系统提供了 `CreateToDo` 工具供用户手动创建ToDo
- 但是 `CreateToDo` 工具**不会**自动从stage的task生成ToDo内容
- 用户或AI Agent需要手动指定ToDo的描述和步骤

示例：
```python
# 手动创建ToDo，需要自己写描述和步骤
CreateToDo(
    task_description="需求分析与验证规划",
    steps=["读取README", "确定目标", "识别风险", "制定计划", "写文档"]
)
```

### 2. 新增功能

现在，我们添加了 `AutoCreateToDoFromStage` 工具，它能够：

✅ **自动读取** default.yaml 中stage定义的task列表  
✅ **自动生成** 基于这些task的ToDo  
✅ **保持一致性** 确保ToDo与stage配置同步  

示例：
```python
# 新工具 - 自动从stage生成ToDo
AutoCreateToDoFromStage()

# 生成的ToDo会包含stage中定义的所有task
# 不需要手动输入每个步骤
```

### 3. 两种工具的对比

| 特性 | CreateToDo | AutoCreateToDoFromStage |
|------|-----------|------------------------|
| 任务来源 | 手动输入 | 自动从default.yaml读取 |
| 灵活性 | 高（完全自定义） | 中（基于stage配置） |
| 一致性 | 需人工保证 | 自动保证 |
| 使用场景 | 自定义工作计划 | 快速开始stage工作 |
| 启用条件 | force_todo | force_todo |

### 4. 具体实现

```python
# 在 StageManager 类中新增的方法
def auto_create_todo_from_stage(self, stage_index=None):
    """
    从stage的任务列表自动创建ToDo
    """
    stage = self.stages[stage_index or self.stage_index]
    task_list = stage.task()  # 从default.yaml中读取
    
    # 使用stage描述作为ToDo描述
    task_description = f"Stage {stage_index}: {stage.description()}"
    
    # 使用stage中的task列表作为ToDo步骤
    steps = [str(task) for task in task_list]
    
    # 创建ToDo
    return self.todo_panel._create(task_description, steps)
```

### 5. 使用示例

假设 `default.yaml` 中有如下定义：

```yaml
stage:
  - name: requirement_analysis_and_planning
    desc: "需求分析与验证规划"
    task:
      - "第1步：读取{DUT}/README.md"
      - "第2步：确定验证目标"
      - "第3步：识别风险点"
      - "第4步：制定验证计划"
      - "第5步：写入验证规划文档"
```

使用新工具：
```python
# 当前在stage 0
AutoCreateToDoFromStage()

# 输出：
# ToDo created successfully!
# Task Description: Stage 0: 需求分析与验证规划
# Steps:
#   1: 第1步：读取{DUT}/README.md
#   2: 第2步：确定验证目标
#   3: 第3步：识别风险点
#   4: 第4步：制定验证计划
#   5: 第5步：写入验证规划文档
```

### 6. 工作流集成

新功能完美融入现有工作流：

```
进入新Stage
    ↓
调用 CurrentTips 查看任务
    ↓
调用 AutoCreateToDoFromStage 自动生成ToDo
    ↓
逐步完成任务，使用 CompleteToDoSteps 标记进度
    ↓
使用 Check 检查完成情况
    ↓
使用 Complete 完成当前Stage
```

### 7. 启用方法

需要在启动UCAgent时启用 `force_todo` 选项：

```bash
ucagent <workspace> <dut_name> --force-todo
```

或在代码中：
```python
agent = UCAgent(
    workspace="./output",
    dut_name="Adder",
    force_todo=True  # 启用ToDo功能
)
```

### 8. 相关文档

- 完整功能说明（中文）: [docs/AUTO_TODO_FROM_STAGE.md](../docs/AUTO_TODO_FROM_STAGE.md)
- 功能说明（英文）: [docs/AUTO_TODO_FROM_STAGE_EN.md](../docs/AUTO_TODO_FROM_STAGE_EN.md)
- 使用示例: [docs/AUTO_TODO_EXAMPLES.md](../docs/AUTO_TODO_EXAMPLES.md)
- 更新日志: [CHANGELOG.md](../CHANGELOG.md)
- 测试代码: [tests/test_auto_todo_from_stage.py](../tests/test_auto_todo_from_stage.py)

## 总结

**回答原问题**: 

原来的 `CreateToDo` **不会**基于 default.yaml 中的 stage task 自动生成。

但现在新增的 `AutoCreateToDoFromStage` 工具**可以**基于 default.yaml 中的 stage task 自动生成ToDo。

这个功能让工作流更加流畅，确保了配置文件与实际工作计划的一致性，是对原有功能的重要补充。
