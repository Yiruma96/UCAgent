# UCAgent 计划管理函数工作流程图

## 整体架构图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          UCAgent 系统架构                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐         │
│  │   用户/外部   │      │    LLM 模型   │      │   MCP Server │         │
│  │  Code Agent  │ ◄──► │  (OpenAI等)   │ ◄──► │    (可选)    │         │
│  └──────────────┘      └──────────────┘      └──────────────┘         │
│         │                     │                      │                 │
│         └─────────────────────┼──────────────────────┘                 │
│                               ▼                                        │
│                  ┌─────────────────────────┐                          │
│                  │   VerifyAgent (核心)     │                          │
│                  │  - 会话管理              │                          │
│                  │  - 消息处理              │                          │
│                  │  - 工具编排              │                          │
│                  └─────────────────────────┘                          │
│                               │                                        │
│         ┌─────────────────────┼─────────────────────┐                 │
│         ▼                     ▼                     ▼                 │
│  ┌─────────────┐      ┌──────────────┐     ┌──────────────┐          │
│  │ 交互逻辑层   │      │  工具系统     │     │  阶段管理器   │          │
│  │ Standard    │      │ - 文件操作    │     │ - Check      │          │
│  │ Enhanced    │      │ - 搜索查询    │     │ - Complete   │          │
│  │ Advanced    │      │ - 记忆管理    │     │ - Status     │          │
│  │             │      │ - 计划管理 ★  │     │              │          │
│  └─────────────┘      └──────────────┘     └──────────────┘          │
│         │                     │                     │                 │
│         └─────────────────────┼─────────────────────┘                 │
│                               ▼                                        │
│                  ┌─────────────────────────┐                          │
│                  │      ToDoPanel          │                          │
│                  │  (计划管理数据中心)      │                          │
│                  │  - 待办列表存储          │                          │
│                  │  - 状态跟踪              │                          │
│                  │  - 进度计算              │                          │
│                  └─────────────────────────┘                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## 计划管理函数调用流程

### 流程 1：标准执行流程（Standard Mode）

```
开始任务
   │
   ▼
智能体收到任务描述
   │
   ├─ 是否启用 --use-todo-tools？
   │     │
   │     ├─ 否 → 直接执行（无计划管理）
   │     │
   │     └─ 是 ↓
   │
   ▼
[可选] CreateToDo
   │   - 分析任务
   │   - 创建步骤列表
   │
   ▼
执行任务步骤
   │
   ├─ GetToDoSummary（查看进度）
   │
   ├─ 执行具体操作...
   │
   ├─ CompleteToDoSteps（标记完成）
   │
   ├─ 发现问题？
   │   └─ UndoToDoSteps / ResetToDo
   │
   ▼
任务完成
```

### 流程 2：增强执行流程（Enhanced Mode）

```
开始任务
   │
   ▼
┌─────────────────────────────────────────┐
│ 阶段 1: 规划阶段 (Planning Phase)        │
├─────────────────────────────────────────┤
│                                         │
│  1. 系统自动触发规划提示                 │
│     "PLANNING PHASE - Let's create..."  │
│                                         │
│  2. 智能体执行规划动作:                  │
│     ├─ SemanticSearchInGuidDoc          │
│     │  (搜索相关文档)                    │
│     │                                   │
│     ├─ MemoryGet                        │
│     │  (获取历史上下文)                  │
│     │                                   │
│     ├─ ReadTextFile                     │
│     │  (阅读需求文件)                    │
│     │                                   │
│     └─ CreateToDo ★                     │
│        (创建详细计划)                    │
│        • task_description: "..."        │
│        • steps: [步骤1, 步骤2, ...]     │
│                                         │
│  3. MemoryPut                           │
│     (保存规划洞察)                       │
│                                         │
└─────────────────────────────────────────┘
   │
   ▼
┌─────────────────────────────────────────┐
│ 阶段 2: 执行阶段 (Execution Phase)       │
├─────────────────────────────────────────┤
│                                         │
│  每轮循环：                              │
│                                         │
│  1. 系统注入执行提示                     │
│     "EXECUTION PHASE - Execute..."      │
│     + 当前计划状态                       │
│                                         │
│  2. ToDoState                           │
│     (查看工具描述了解进度)               │
│     "Current ToDo List has 8 steps,    │
│      3 completed and 5 uncompleted."   │
│                                         │
│  3. [可选] GetToDoSummary               │
│     (详细查看计划)                       │
│                                         │
│  4. 执行当前步骤                         │
│     ├─ ReadTextFile / EditTextFile     │
│     ├─ SearchText / FindFiles          │
│     ├─ RunTestCases                    │
│     └─ ...其他操作                      │
│                                         │
│  5. CompleteToDoSteps([步骤索引]) ★    │
│     (标记完成)                          │
│     → ToDoPanel 更新状态                │
│     → ToDoState 描述自动更新            │
│                                         │
│  6. 遇到问题？                          │
│     ├─ UndoToDoSteps ★                 │
│     │  (撤销需要重做的步骤)              │
│     └─ ResetToDo ★                     │
│        (完全重新规划)                    │
│                                         │
│  重复直到所有步骤完成                    │
│                                         │
└─────────────────────────────────────────┘
   │
   ▼
┌─────────────────────────────────────────┐
│ 阶段 3: 验证阶段 (Verification Phase)    │
├─────────────────────────────────────────┤
│                                         │
│  1. GetToDoSummary                      │
│     (确认所有步骤完成)                   │
│                                         │
│  2. Check                               │
│     (运行验证检查)                       │
│                                         │
│  3. Complete                            │
│     (完成当前stage)                      │
│                                         │
└─────────────────────────────────────────┘
   │
   ▼
┌─────────────────────────────────────────┐
│ 阶段 4: 反思阶段 (Reflection Phase)      │
│  (每3轮触发一次)                         │
├─────────────────────────────────────────┤
│                                         │
│  1. 系统触发反思提示                     │
│                                         │
│  2. 评估执行效果                         │
│     - 哪些步骤顺利？                     │
│     - 哪些遇到困难？                     │
│     - 需要调整策略吗？                   │
│                                         │
│  3. 可能的动作：                         │
│     ├─ 继续执行                         │
│     ├─ UndoToDoSteps (调整)            │
│     └─ ResetToDo (重新规划)            │
│                                         │
└─────────────────────────────────────────┘
   │
   └─ 返回执行阶段或进入下一任务
```

## ToDoPanel 状态机

```
┌────────────────────────────────────────────┐
│             ToDoPanel 状态                  │
└────────────────────────────────────────────┘

状态 1: 空闲 (Empty)
├─ todo_list = {}
├─ ToDoState 描述: "No Active ToDo List."
└─ 可用操作: CreateToDo

      │ CreateToDo(description, steps)
      ▼

状态 2: 活跃 (Active - 有未完成步骤)
├─ todo_list = {task, steps, ...}
├─ 某些 steps[i][1] = False
├─ ToDoState 描述: "Current ToDo List has X steps,
│                   Y completed and Z uncompleted."
└─ 可用操作:
    ├─ GetToDoSummary (查看详情)
    ├─ CompleteToDoSteps (标记完成)
    ├─ UndoToDoSteps (撤销)
    ├─ ResetToDo (重置)
    └─ CreateToDo (覆盖)

      │ CompleteToDoSteps (所有步骤)
      ▼

状态 3: 完成 (Completed)
├─ 所有 steps[i][1] = True
├─ ToDoState 描述: "Current ToDo list is completed!
│                   You can create a new one."
└─ 可用操作:
    ├─ UndoToDoSteps (重新打开某些步骤)
    ├─ ResetToDo (清空)
    └─ CreateToDo (创建新任务)

      │ ResetToDo()
      ▼

返回状态 1: 空闲
```

## 与其他系统的集成

### 与 Stage Manager 的集成

```
┌───────────────────────────────────────────────────┐
│           Stage Manager (阶段管理器)               │
├───────────────────────────────────────────────────┤
│                                                   │
│  Stage 1: requirement_analysis_and_planning       │
│  ├─ Tips: "请分析需求并制定验证计划..."            │
│  ├─ 智能体调用: CreateToDo                        │
│  └─ 工具: CurrentTips, RoleInfo, ...             │
│                                                   │
│  Stage 2: basic_functionality_tests               │
│  ├─ Tips: "请为基本功能编写测试用例..."            │
│  ├─ 智能体查看: GetToDoSummary                    │
│  ├─ 执行测试编写                                   │
│  └─ 更新: CompleteToDoSteps([1,2,3])             │
│                                                   │
│  Stage 3: corner_case_tests                       │
│  ├─ Tips: "请补充边界和异常测试..."               │
│  ├─ 继续执行计划中的步骤                           │
│  └─ CompleteToDoSteps([4,5])                     │
│                                                   │
│  Stage N: report_generation                       │
│  ├─ Tips: "请生成测试报告..."                     │
│  ├─ GetToDoSummary (确认所有完成)                 │
│  └─ 生成报告                                       │
│                                                   │
└───────────────────────────────────────────────────┘
```

### 与 Memory System 的集成

```
┌──────────────────────────────────────────┐
│        计划 + 记忆系统协同                │
├──────────────────────────────────────────┤
│                                          │
│  1. 规划阶段                              │
│     CreateToDo(...)                      │
│     ↓                                    │
│     MemoryPut(                           │
│       content="规划：步骤1-8...",        │
│       scope="planning"                   │
│     )                                    │
│                                          │
│  2. 执行阶段                              │
│     MemoryGet(                           │
│       query="之前的设计决策",             │
│       scope="planning"                   │
│     )                                    │
│     ↓                                    │
│     基于记忆执行步骤                       │
│     ↓                                    │
│     CompleteToDoSteps([...])             │
│     ↓                                    │
│     MemoryPut(                           │
│       content="完成步骤3，发现...",       │
│       scope="execution"                  │
│     )                                    │
│                                          │
│  3. 反思阶段                              │
│     MemoryGet(scope="planning")          │
│     + MemoryGet(scope="execution")       │
│     ↓                                    │
│     评估和学习                            │
│     ↓                                    │
│     MemoryPut(                           │
│       content="经验总结...",             │
│       scope="reflection"                 │
│     )                                    │
│                                          │
└──────────────────────────────────────────┘
```

## MCP Server 协同模式

```
┌─────────────────────────────────────────────────────────┐
│           MCP Server 模式工作流程                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐                  ┌────────────────┐  │
│  │ Qwen Code CLI│                  │ UCAgent Server │  │
│  │  (客户端)     │  MCP Protocol    │  (localhost:5000)│  │
│  │              │ ◄──────────────► │                │  │
│  └──────────────┘                  └────────────────┘  │
│         │                                   │          │
│         │                                   │          │
│  用户输入："请通过工具RoleInfo获取角色信息..."         │
│         │                                   │          │
│         ▼                                   ▼          │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │ 1. Code Agent 调用 UCAgent 工具                  │  │
│  ├──────────────────────────────────────────────────┤  │
│  │  RoleInfo()                                      │  │
│  │  └─ 返回: "你是硬件验证 AI..."                    │  │
│  │                                                  │  │
│  │  CurrentTips()                                   │  │
│  │  └─ 返回: "当前阶段：需求分析..."                 │  │
│  │                                                  │  │
│  │  CreateToDo(                                     │  │
│  │    task_description="为Adder创建测试",           │  │
│  │    steps=[...]                                   │  │
│  │  )                                               │  │
│  │  └─ 返回: "ToDo created successfully!"          │  │
│  └──────────────────────────────────────────────────┘  │
│         │                                   │          │
│         ▼                                   │          │
│  ┌──────────────────────────────────────────────────┐  │
│  │ 2. Code Agent 使用自己的工具执行                 │  │
│  ├──────────────────────────────────────────────────┤  │
│  │  - 读取文件 (自己的 ReadFile)                    │  │
│  │  - 编写代码 (自己的 WriteFile)                   │  │
│  │  - 执行命令 (自己的 ExecuteCommand)              │  │
│  └──────────────────────────────────────────────────┘  │
│         │                                   │          │
│         ▼                                   ▼          │
│  ┌──────────────────────────────────────────────────┐  │
│  │ 3. 定期同步进度到 UCAgent                        │  │
│  ├──────────────────────────────────────────────────┤  │
│  │  GetToDoSummary()                                │  │
│  │  └─ 返回: 当前进度...                            │  │
│  │                                                  │  │
│  │  CompleteToDoSteps([1,2,3])                      │  │
│  │  └─ 返回: "3 step(s) marked as completed."      │  │
│  │                                                  │  │
│  │  Check()  (运行测试)                             │  │
│  │  └─ 返回: 测试结果...                            │  │
│  └──────────────────────────────────────────────────┘  │
│         │                                   │          │
│         ▼                                   ▼          │
│  ┌──────────────────────────────────────────────────┐  │
│  │ 4. 完成并进入下一阶段                            │  │
│  ├──────────────────────────────────────────────────┤  │
│  │  Complete()                                      │  │
│  │  └─ UCAgent 切换到下一个 Stage                   │  │
│  │                                                  │  │
│  │  重复上述流程...                                  │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 时序图：完整执行周期

```
时间轴
 │
 ├─ T0: 启动 UCAgent (Enhanced mode)
 │      └─ 初始化 ToDoPanel
 │      └─ 加载 planning_tools
 │
 ├─ T1: 首次调用 invoke()
 │      └─ EnhancedInteractionLogic.enhanced_one_loop()
 │         └─ _determine_interaction_strategy()
 │            └─ 返回: "planning_required"
 │
 ├─ T2: 规划阶段开始
 │      └─ _create_planning_message()
 │      └─ 发送规划提示给 LLM
 │
 ├─ T3: LLM 决策调用 CreateToDo
 │      └─ ToDoPanel._create(description, steps)
 │         ├─ 验证步骤数量 (2-20)
 │         ├─ 创建 todo_list 数据结构
 │         ├─ 设置 created_at 时间戳
 │         └─ 调用 set_tool_process()
 │            └─ 更新 ToDoState 描述
 │
 ├─ T4: 转换到执行阶段
 │      └─ state.transition_to_phase("execution")
 │
 ├─ T5-T10: 执行循环 (多次 invoke)
 │      └─ 每次循环:
 │         ├─ _create_execution_message(plan_status)
 │         ├─ LLM 查看 ToDoState 工具描述
 │         ├─ LLM 执行任务操作
 │         └─ LLM 调用 CompleteToDoSteps([...])
 │            └─ ToDoPanel._complete_steps()
 │               ├─ 更新 steps[i][1] = True
 │               ├─ 设置 updated_at 时间戳
 │               └─ 调用 set_tool_process()
 │
 ├─ T11: 反思阶段 (第3轮后)
 │      └─ _handle_reflection_phase()
 │         └─ 评估执行效果
 │         └─ 可能调用 UndoToDoSteps / ResetToDo
 │
 ├─ T12-T15: 继续执行剩余步骤
 │      └─ 重复 T5-T10 的流程
 │
 ├─ T16: 所有步骤完成
 │      └─ ToDoPanel._is_all_completed() = True
 │      └─ ToDoState 描述更新为 "completed"
 │
 └─ T17: 任务完成
        └─ Complete() 工具调用
        └─ Stage Manager 进入下一阶段
```

---

## 关键观察

### 1. 自动化程度
- **Standard**: 手动调用，可选使用
- **Enhanced**: 自动引导创建计划，半自动跟踪
- **Advanced**: 动态调整策略，高度自动化

### 2. 状态同步
- ToDoPanel 状态变化 → ToDoState 描述自动更新
- 智能体可通过工具描述快速了解进度，无需显式调用

### 3. 灵活性
- 支持撤销 (UndoToDoSteps)
- 支持重置 (ResetToDo)
- 支持覆盖 (CreateToDo 可覆盖现有计划)

### 4. 集成点
- 与 Stage Manager 松耦合
- 与 Memory System 协同工作
- 与文件操作/验证工具无缝配合

这些设计使计划管理函数成为 UCAgent 执行复杂验证任务的重要基础设施。
