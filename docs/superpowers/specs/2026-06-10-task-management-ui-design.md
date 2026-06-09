# 任务管理界面优化设计方案

> 生成日期：2026-06-10
> 状态：已批准

---

## 1. 概述

### 1.1 目标
- 美化任务管理界面视觉效果
- 添加日期区间查询功能
- 添加任务优先级功能（正常/中/紧急）

### 1.2 方案
- 功能：快速迭代（方案A）
- 视觉：视觉优先（方案C）

---

## 2. 视觉设计

### 2.1 配色方案

| 用途 | 颜色 | 说明 |
|------|------|------|
| 背景渐变 | `#f8fafc` → `#f1f5f9` | 柔和灰白渐变 |
| 卡片背景 | `rgba(255,255,255,0.8)` | 白色玻璃态 |
| 主色调 | `#475569` | 深蓝灰 |
| 中优先级 | `#fb923c` | 柔和橙色 |
| 紧急优先级 | `#f87171` | 柔和红色 |
| 边框 | `rgba(255,255,255,0.5)` | 半透明白 |

### 2.2 动画效果

| 元素 | 效果 | 参数 |
|------|------|------|
| 按钮Hover | scale(1.02) + 阴影增强 | transition: 200ms ease-out |
| 按钮Press | scale(0.98) | transition: 100ms |
| 卡片Hover | 上浮2px + 阴影加深 | transition: 200ms ease-out |
| 弹窗 | fade-in + scale(0.95→1) | transition: 300ms ease-out |
| 任务行Hover | 背景轻微高亮 | transition: 150ms |

### 2.3 优先级标识

- **位置**：任务行左侧
- **样式**：4px宽色条
- **颜色**：
  - 正常：无色条
  - 中：橙色（`#fb923c`）
  - 紧急：红色（`#f87171`）

### 2.4 Badge样式

- 形状：圆角pill形（`border-radius: 9999px`）
- 背景：柔和色（透明度30%）
- 文字：深色

---

## 3. 功能设计

### 3.1 查询面板

**位置**：Tab切换下方

**元素**：
- 开始日期输入（date-local）
- 结束日期输入（date-local）
- 查询按钮
- 重置按钮

**布局**：横向排列，紧凑

### 3.2 新增/编辑任务

**新增字段**：优先级下拉选择

| 选项 | 值 | 说明 |
|------|-----|------|
| 正常 | `normal` | 默认值 |
| 中 | `medium` | 橙色标识 |
| 紧急 | `urgent` | 红色标识 |

**字段位置**：任务名称下方

### 3.3 任务列表

- 左侧色条标识优先级
- 悬浮效果：整行轻微高亮
- 支持点击查看详情

---

## 4. 数据模型变更

### 4.1 Task 表

```sql
ALTER TABLE sys_task ADD COLUMN priority ENUM('normal', 'medium', 'urgent') DEFAULT 'normal' COMMENT '优先级';
```

### 4.2 TaskResponse 更新

```typescript
interface Task {
  // ... existing fields
  priority: 'normal' | 'medium' | 'urgent'
}
```

---

## 5. API 变更

### 5.1 GET /api/tasks

**新增参数**：
| 参数 | 类型 | 说明 |
|------|------|------|
| start_date | string (date) | 开始日期 |
| end_date | string (date) | 结束日期 |
| priority | string | 优先级筛选 |

### 5.2 POST /api/tasks

**新增字段**：
```json
{
  "name": "string",
  "register_time": "string",
  "publisher": "string",
  "remark": "string",
  "priority": "normal" // normal | medium | urgent
}
```

### 5.3 PUT /api/tasks/{id}

**新增字段**：
```json
{
  "priority": "medium" // 可选修改
}
```

---

## 6. 前端组件变更

| 组件 | 变更 |
|------|------|
| `TasksView.vue` | 添加查询面板、优先级字段 |
| `TaskTable.vue` | 添加行优先级色条 |
| `Card.vue` | 增强hover动画 |
| `Button` | 增强hover/press效果 |
| `DialogContent.vue` | 优化动画效果 |

---

## 7. 实现清单

### 前端
- [ ] 更新 `style.css` 添加动画类
- [ ] 更新 `TaskTable.vue` 添加优先级色条
- [ ] 更新 `TasksView.vue` 添加查询面板
- [ ] 新增任务支持 priority 字段
- [ ] 编辑任务支持修改 priority
- [ ] Button 组件增强动画

### 后端
- [ ] 更新 Task 模型添加 priority 字段
- [ ] 更新 TaskService 支持日期范围查询
- [ ] 更新 API 支持 priority 筛选
- [ ] 执行数据库迁移

---

## 8. 验收标准

1. 任务列表显示优先级色条（正常无、中橙、紧急红）
2. 可通过日期范围筛选任务
3. 新增任务可选择优先级（默认正常）
4. 按钮有 hover/press 动画效果
5. 卡片有悬浮效果
6. 视觉效果柔和不刺眼