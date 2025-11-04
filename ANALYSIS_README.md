# UCAgent 计划管理函数分析文档

本目录包含对 UCAgent 项目中计划管理函数（CreateToDo 等）在智能体执行过程中作用的深入分析。

## 📄 文档列表

### 1. [计划管理函数分析报告.md](./计划管理函数分析报告.md)
**主要分析报告 - 推荐首先阅读**

这是对计划管理函数完整的中文分析文档，包含：

- **核心函数概览**：CreateToDo, CompleteToDoSteps, UndoToDoSteps 等函数的详细说明
- **在智能体执行中的作用**：三种交互模式（Standard/Enhanced/Advanced）下的应用
- **验证工作流集成**：计划管理函数在芯片验证各阶段的角色
- **技术实现细节**：步骤验证机制、状态持久化、工具链集成
- **实际应用场景**：硬件验证任务分解、MCP Server 协同等实例
- **优势与价值**：提升效率、增强推理、支持人机协同
- **使用建议**：何时启用、配置方式、最佳实践

**适合读者**：想要全面了解计划管理函数设计理念和使用方法的开发者和用户

### 2. [planning_functions_workflow.md](./planning_functions_workflow.md)
**工作流程和架构图 - 可视化参考**

这是补充的可视化文档，包含：

- **整体架构图**：UCAgent 系统各组件关系
- **执行流程图**：Standard 和 Enhanced 模式的详细流程
- **状态机图**：ToDoPanel 的状态转换
- **集成图**：与 Stage Manager、Memory System、MCP Server 的协同
- **时序图**：完整执行周期的时间线

**适合读者**：喜欢通过图表理解系统工作原理的读者，或需要快速了解整体流程的开发者

## 🎯 核心发现总结

### 计划管理函数的 8 大作用

1. **任务组织器** - 将复杂的芯片验证任务分解为结构化的执行步骤
2. **进度追踪器** - 实时记录和显示任务执行状态，支持进度查询
3. **执行引导器** - 在 Enhanced/Advanced 模式下主动引导智能体按计划执行
4. **上下文记忆** - 减少对长对话历史的依赖，提供持久的任务上下文
5. **人机接口** - 为人机协同验证提供清晰的沟通界面
6. **质量保证** - 通过系统化的步骤管理，降低遗漏关键验证环节的风险
7. **灵活调整** - 支持撤销、重置，适应动态变化的验证需求
8. **工具编排** - 作为工具系统的一部分，与其他工具协同提升整体效能

### 关键代码位置

| 组件 | 文件路径 | 说明 |
|-----|---------|------|
| 计划管理工具定义 | `vagent/tools/planning.py` | ToDoPanel, CreateToDo, CompleteToDoSteps 等 |
| 智能体主类 | `vagent/verify_agent.py` | VerifyAgent 类，工具初始化逻辑 |
| Enhanced 交互逻辑 | `vagent/interaction/enhanced.py` | EnhancedInteractionLogic 类，规划/执行/反思阶段 |
| 工具编排系统 | `vagent/interaction/orchestrator.py` | ToolRecommendationEngine，上下文映射 |
| 阶段管理 | `vagent/stage/vmanager.py` | StageManager，验证流程管理 |
| 配置文件 | `vagent/lang/zh/config/default.yaml` | Stage 定义和配置 |

## 🚀 快速开始

### 如何启用计划管理功能？

#### 方法 1：使用 Enhanced 模式（推荐）
```bash
ucagent output/ Adder --interaction-mode enhanced
```
自动启用计划管理，并引导智能体进行结构化规划和执行。

#### 方法 2：在 Standard 模式中启用
```bash
ucagent output/ Adder --use-todo-tools
```
启用计划管理工具，但不强制使用。

#### 方法 3：配合 MCP Server 使用
```bash
ucagent output/ Adder --mcp-server --use-todo-tools
```
作为 MCP Server 为外部 Code Agent 提供计划管理能力。

### 典型使用场景

```python
# 1. 创建计划
CreateToDo(
    task_description="为 Adder DUT 创建完整的单元测试",
    steps=[
        "阅读 README.md 理解 DUT 功能",
        "搜索测试规范文档",
        "设计基础功能测试用例",
        "设计边界测试用例",
        "编写测试代码",
        "运行测试并分析覆盖率",
        "生成测试报告"
    ]
)

# 2. 执行任务并标记进度
CompleteToDoSteps(
    completed_steps=[1, 2, 3],
    notes="已完成前3步，设计了15个测试用例"
)

# 3. 查看进度
GetToDoSummary()

# 4. 发现问题，撤销某些步骤
UndoToDoSteps(
    steps=[3],
    notes="测试用例需要重新设计"
)

# 5. 必要时完全重新规划
ResetToDo()
```

## 📊 适用场景对比

| 场景类型 | 推荐模式 | 计划管理作用 |
|---------|---------|-------------|
| 简单单步任务 | Standard (不启用) | 不需要 |
| 中等复杂度任务 (3-10步) | Standard + `--use-todo-tools` | 可选使用，提供结构 |
| 复杂多步骤任务 (>10步) | Enhanced | 自动引导规划，强烈推荐 |
| 长时间执行任务 | Enhanced 或 Advanced | 保持上下文，防止遗忘 |
| 需要人机协同 | 任意模式 + `--use-todo-tools` | 提供清晰沟通界面 |
| MCP Server 模式 | Standard + `--use-todo-tools` | 为外部 Agent 提供计划能力 |

## 🔍 深入学习路径

### 对于用户
1. 阅读 [计划管理函数分析报告.md](./计划管理函数分析报告.md) 第一、二、六、七章
2. 了解如何配置和使用计划管理功能
3. 查看实际应用场景示例
4. 尝试在自己的验证任务中使用

### 对于开发者
1. 完整阅读 [计划管理函数分析报告.md](./计划管理函数分析报告.md)
2. 结合 [planning_functions_workflow.md](./planning_functions_workflow.md) 理解架构
3. 查看源代码：
   - `vagent/tools/planning.py` - 核心实现
   - `vagent/interaction/enhanced.py` - Enhanced 模式集成
   - `vagent/interaction/orchestrator.py` - 工具编排
4. 运行示例验证任务，观察计划管理工具的调用
5. 考虑如何扩展或定制计划管理功能

### 对于研究者
1. 阅读两份文档了解完整设计
2. 分析计划管理如何提升 LLM Agent 的执行能力
3. 研究不同交互模式的效果差异
4. 探索更高级的任务分解和执行策略

## 💡 相关资源

- [UCAgent 主项目 README](./README.zh.md)
- [UCAgent 官方文档](https://open-verify.cc/mlvp/docs/ucagent/)
- [Picker 框架](https://github.com/XS-MLVP/picker)
- [Toffee 测试框架](https://open-verify.cc/mlvp/docs/toffee-test/)

## 🤝 贡献

如果您发现文档中的错误或有改进建议，欢迎提交 Issue 或 Pull Request。

## 📝 文档信息

- **创建日期**：2024-11-04
- **分析基于**：UCAgent 主分支最新代码
- **语言**：中文（分析报告）
- **文档类型**：技术分析、架构说明

## 📄 许可

本分析文档遵循与 UCAgent 项目相同的开源许可。

---

**问题反馈**：如有疑问，请在项目 Issue 中提出。
