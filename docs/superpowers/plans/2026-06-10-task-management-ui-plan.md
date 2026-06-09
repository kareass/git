# 任务管理界面优化 - 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**目标：** 美化任务管理界面，添加日期区间查询和优先级功能

**架构：**
- 后端：FastAPI + SQLAlchemy，Task 模型新增 priority 字段，查询支持日期范围筛选
- 前端：Vue3 + Pinia + Tailwind，玻璃态UI + 动画效果，任务行优先级色条

**技术栈：** Vue3, FastAPI, TypeScript, Tailwind CSS, SQLAlchemy

---

## 阶段 1: 后端实现

### Task 1: 更新数据库模型

**Files:**
- Modify: `backend/app/models/task.py`
- Modify: `backend/app/schemas/task.py`
- Modify: `docs/sql/init.sql`

- [ ] **Step 1: 更新 Task 模型添加 priority 字段**

```python
# backend/app/models/task.py
from sqlalchemy import String, Enum as SQLEnum

class TaskPriority(str, enum.Enum):
    normal = "normal"
    medium = "medium"
    urgent = "urgent"

class Task(Base):
    __tablename__ = "sys_task"

    # ... existing fields ...
    priority: Mapped[TaskPriority] = mapped_column(
        SQLEnum(TaskPriority),
        default=TaskPriority.normal,
        nullable=False
    )
```

- [ ] **Step 2: 更新 Pydantic Schema**

```python
# backend/app/schemas/task.py
from enum import Enum

class TaskPriority(str, Enum):
    normal = "normal"
    medium = "medium"
    urgent = "urgent"

class TaskCreate(BaseModel):
    name: str
    register_time: datetime
    publisher: str
    remark: Optional[str] = None
    priority: TaskPriority = TaskPriority.normal

class TaskUpdate(BaseModel):
    name: Optional[str] = None
    register_time: Optional[datetime] = None
    publisher: Optional[str] = None
    is_completed: Optional[bool] = None
    remark: Optional[str] = None
    priority: Optional[TaskPriority] = None

class TaskResponse(BaseModel):
    id: int
    name: str
    register_time: datetime
    complete_time: Optional[datetime]
    publisher: str
    is_completed: bool
    remark: Optional[str]
    user_id: int
    priority: TaskPriority
    created_at: datetime
    updated_at: datetime
```

- [ ] **Step 3: 更新 SQL 初始化脚本**

```sql
-- docs/sql/init.sql
-- 在 sys_task 表中添加 priority 字段
ALTER TABLE sys_task ADD COLUMN priority ENUM('normal', 'medium', 'urgent') DEFAULT 'normal' COMMENT '优先级';

-- 更新初始化数据
UPDATE sys_task SET priority = 'normal' WHERE priority IS NULL;
```

- [ ] **Step 4: 提交变更**

```bash
cd "E:/ai/claude code/代码开发/需求开发事项统计"
git add backend/app/models/task.py backend/app/schemas/task.py docs/sql/init.sql
git commit -m "feat: add priority field to Task model"
```

---

### Task 2: 更新 TaskService 支持日期范围查询

**Files:**
- Modify: `backend/app/services/task.py`

- [ ] **Step 1: 查看当前 TaskService 实现**

```python
# backend/app/services/task.py
class TaskService:
    async def get_tasks(self, user_id: int, is_completed: Optional[bool] = None,
                       page: int = 1, page_size: int = 20):
        query = select(Task).where(Task.user_id == user_id)
        if is_completed is not None:
            query = query.where(Task.is_completed == is_completed)
        # ... 分页逻辑
```

- [ ] **Step 2: 更新 get_tasks 方法支持日期范围查询**

```python
async def get_tasks(
    self,
    user_id: int,
    is_completed: Optional[bool] = None,
    page: int = 1,
    page_size: int = 20,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    priority: Optional[str] = None
):
    query = select(Task).where(Task.user_id == user_id)
    if is_completed is not None:
        query = query.where(Task.is_completed == is_completed)
    if start_date:
        query = query.where(Task.register_time >= start_date)
    if end_date:
        query = query.where(Task.register_time <= end_date)
    if priority:
        query = query.where(Task.priority == priority)
    # ... 分页逻辑
```

- [ ] **Step 3: 提交变更**

```bash
git add backend/app/services/task.py
git commit -m "feat: support date range and priority query in TaskService"
```

---

### Task 3: 更新 API 路由

**Files:**
- Modify: `backend/app/api/routes/tasks.py`

- [ ] **Step 1: 更新 get_tasks API 添加新参数**

```python
@router.get("", response_model=TaskListResponse)
async def get_tasks(
    is_completed: Optional[bool] = Query(None),
    start_date: Optional[str] = Query(None, description="开始日期 YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD"),
    priority: Optional[str] = Query(None, description="优先级筛选"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 转换日期字符串
    start_dt = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
    end_dt = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1) if end_date else None

    task_service = TaskService(db)
    tasks, total = await task_service.get_tasks(
        current_user.id, is_completed, page, page_size,
        start_dt, end_dt, priority
    )
    # ...
```

- [ ] **Step 2: 添加 timedelta 导入**

```python
from datetime import datetime, timedelta
```

- [ ] **Step 3: 提交变更**

```bash
git add backend/app/api/routes/tasks.py
git commit -m "feat: add date range and priority query params to GET /api/tasks"
```

---

## 阶段 2: 前端实现

### Task 4: 更新 TypeScript 类型定义

**Files:**
- Modify: `frontend/src/types/index.ts`

- [ ] **Step 1: 更新 Task 接口添加 priority**

```typescript
export type TaskPriority = 'normal' | 'medium' | 'urgent'

export interface Task {
  id: number
  name: string
  register_time: string
  complete_time: string | null
  publisher: string
  is_completed: boolean
  remark: string | null
  user_id: number
  priority: TaskPriority
  created_at: string
  updated_at: string
}

export interface CreateTaskRequest {
  name: string
  register_time: string
  publisher: string
  remark?: string
  priority?: TaskPriority
}

export interface UpdateTaskRequest {
  name?: string
  register_time?: string
  publisher?: string
  is_completed?: boolean
  remark?: string
  priority?: TaskPriority
}
```

- [ ] **Step 2: 提交变更**

```bash
cd "E:/ai/claude code/代码开发/需求开发事项统计/frontend"
git add src/types/index.ts
git commit -m "feat: add priority field to Task types"
```

---

### Task 5: 更新 API 调用

**Files:**
- Modify: `frontend/src/api/task.ts`

- [ ] **Step 1: 查看当前 API 实现**

```typescript
// frontend/src/api/task.ts
export const taskApi = {
  list: (params: { is_completed?: boolean; page?: number; page_size?: number }) =>
    api.get('/tasks', { params }),
  // ...
}
```

- [ ] **Step 2: 更新 list 方法支持新参数**

```typescript
list: (params: {
  is_completed?: boolean
  start_date?: string
  end_date?: string
  priority?: string
  page?: number
  page_size?: number
}) => api.get('/tasks', { params }),
```

- [ ] **Step 3: 提交变更**

```bash
git add src/api/task.ts
git commit -m "feat: add date range and priority params to task API"
```

---

### Task 6: 更新 TaskStore

**Files:**
- Modify: `frontend/src/stores/task.ts`

- [ ] **Step 1: 更新 fetchTasks 支持查询参数**

```typescript
async function fetchTasks(params: {
  is_completed?: boolean
  start_date?: string
  end_date?: string
  priority?: string
} = {}) {
  loading.value = true
  try {
    const { data } = await taskApi.list({
      ...params,
      page: page.value,
      page_size: pageSize.value
    })
    tasks.value = data.items
    total.value = data.total
  } finally {
    loading.value = false
  }
}
```

- [ ] **Step 2: 提交变更**

```bash
git add src/stores/task.ts
git commit -m "feat: update TaskStore to support query params"
```

---

### Task 7: 添加动画样式

**Files:**
- Modify: `frontend/src/style.css`

- [ ] **Step 1: 添加玻璃态和动画类**

```css
/* 玻璃态基础 */
.glass {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.glass-card {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease-out;
}

.glass-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

/* 按钮动画 */
.btn-glow {
  transition: all 0.2s ease-out;
}

.btn-glow:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.btn-glow:active {
  transform: scale(0.98);
}

/* 优先级色条 */
.priority-bar-normal { border-left: 4px solid transparent; }
.priority-bar-medium { border-left: 4px solid #fb923c; }
.priority-bar-urgent { border-left: 4px solid #f87171; }

/* 优先级 Badge */
.badge-normal {
  background: rgba(71, 85, 105, 0.1);
  color: #475569;
}

.badge-medium {
  background: rgba(251, 146, 60, 0.2);
  color: #ea580c;
}

.badge-urgent {
  background: rgba(248, 113, 113, 0.2);
  color: #dc2626;
}
```

- [ ] **Step 2: 提交变更**

```bash
git add src/style.css
git commit -m "feat: add glass morphism and animation styles"
```

---

### Task 8: 更新 TaskTable 组件添加优先级色条

**Files:**
- Modify: `frontend/src/components/TaskTable.vue`

- [ ] **Step 1: 更新 TaskTable 添加优先级色条**

```vue
<script setup lang="ts">
import type { Task, TaskPriority } from '@/types'

const props = defineProps<{
  tasks: Task[]
}>()

const emit = defineEmits<{
  complete: [task: Task]
  defer: [task: Task]
  delete: [task: Task]
  detail: [task: Task]
}>()

function getPriorityClass(priority: TaskPriority): string {
  const classMap = {
    normal: 'priority-bar-normal',
    medium: 'priority-bar-medium',
    urgent: 'priority-bar-urgent'
  }
  return classMap[priority] || 'priority-bar-normal'
}

function formatDate(date: string | null) {
  if (!date) return '-'
  return new Date(date).toLocaleString('zh-CN')
}
</script>

<template>
  <Table>
    <TableHeader>
      <TableRow>
        <TableHead class="w-4"></TableHead>
        <TableHead>任务名称</TableHead>
        <TableHead>优先级</TableHead>
        <TableHead>登记时间</TableHead>
        <TableHead>发布人</TableHead>
        <TableHead>备注</TableHead>
        <TableHead class="text-right">操作</TableHead>
      </TableRow>
    </TableHeader>
    <TableBody>
      <TableRow
        v-for="task in tasks"
        :key="task.id"
        :class="['transition-colors hover:bg-accent/30', getPriorityClass(task.priority)]"
      >
        <TableCell></TableCell>
        <TableCell class="font-medium">{{ task.name }}</TableCell>
        <TableCell>
          <Badge :class="['badge-' + task.priority]">
            {{ task.priority === 'normal' ? '正常' : task.priority === 'medium' ? '中' : '紧急' }}
          </Badge>
        </TableCell>
        <TableCell>{{ formatDate(task.register_time) }}</TableCell>
        <TableCell>{{ task.publisher }}</TableCell>
        <TableCell>{{ task.remark || '-' }}</TableCell>
        <TableCell class="text-right space-x-2">
          <Button variant="ghost" size="sm" class="btn-glow" @click="emit('detail', task)">详情</Button>
          <template v-if="!task.is_completed">
            <Button variant="ghost" size="sm" class="btn-glow" @click="emit('complete', task)">完成</Button>
            <Button variant="ghost" size="sm" class="btn-glow" @click="emit('defer', task)">顺延</Button>
            <Button variant="destructive" size="sm" class="btn-glow" @click="emit('delete', task)">删除</Button>
          </template>
        </TableCell>
      </TableRow>
      <TableRow v-if="tasks.length === 0">
        <TableCell colspan="7" class="text-center text-muted-foreground py-8">
          暂无数据
        </TableCell>
      </TableRow>
    </TableBody>
  </Table>
</template>
```

- [ ] **Step 2: 提交变更**

```bash
git add src/components/TaskTable.vue
git commit -m "feat: add priority color bar to TaskTable"
```

---

### Task 9: 更新 TasksView 添加查询面板和优先级选择

**Files:**
- Modify: `frontend/src/views/TasksView.vue`

- [ ] **Step 1: 添加查询面板和优先级选择**

```vue
<script setup lang="ts">
import { ref } from 'vue'
import type { TaskPriority } from '@/types'

// 查询相关状态
const startDate = ref('')
const endDate = ref('')

// 优先级选项
const priorityOptions = [
  { label: '全部', value: '' },
  { label: '正常', value: 'normal' },
  { label: '中', value: 'medium' },
  { label: '紧急', value: 'urgent' }
]
const selectedPriority = ref('')

// 新任务默认值
const newTask = ref({
  name: '',
  register_time: new Date().toISOString().slice(0, 16),
  publisher: authStore.user?.username || '',
  remark: '',
  priority: 'normal' as TaskPriority
})

// 查询方法
function handleQuery() {
  taskStore.fetchTasks({
    is_completed: activeTab.value === 'completed',
    start_date: startDate.value || undefined,
    end_date: endDate.value || undefined,
    priority: selectedPriority.value || undefined
  })
}

function handleReset() {
  startDate.value = ''
  endDate.value = ''
  selectedPriority.value = ''
  loadTasks()
}
</script>

<template>
  <!-- 查询面板 -->
  <div class="flex items-center gap-4 mb-6 p-4 glass-card rounded-lg">
    <div class="flex items-center gap-2">
      <label class="text-sm font-medium">开始日期</label>
      <Input v-model="startDate" type="date" class="w-36" />
    </div>
    <div class="flex items-center gap-2">
      <label class="text-sm font-medium">结束日期</label>
      <Input v-model="endDate" type="date" class="w-36" />
    </div>
    <div class="flex items-center gap-2">
      <label class="text-sm font-medium">优先级</label>
      <select v-model="selectedPriority" class="h-8 rounded-lg border bg-transparent px-2">
        <option v-for="opt in priorityOptions" :key="opt.value" :value="opt.value">
          {{ opt.label }}
        </option>
      </select>
    </div>
    <Button class="btn-glow" @click="handleQuery">查询</Button>
    <Button variant="outline" class="btn-glow" @click="handleReset">重置</Button>
  </div>
</template>
```

- [ ] **Step 2: 更新新增任务表单添加优先级**

在新增任务表单中添加优先级选择：

```vue
<FormField name="priority">
  <FormItem>
    <FormLabel>优先级</FormLabel>
    <FormControl>
      <select v-model="newTask.priority" class="h-8 rounded-lg border bg-transparent px-2 w-full">
        <option value="normal">正常</option>
        <option value="medium">中</option>
        <option value="urgent">紧急</option>
      </select>
    </FormControl>
  </FormItem>
</FormField>
```

- [ ] **Step 3: 提交变更**

```bash
git add src/views/TasksView.vue
git commit -m "feat: add query panel and priority selector to TasksView"
```

---

### Task 10: 数据库迁移

**Files:**
- Execute: SQL migration on MySQL

- [ ] **Step 1: 执行 SQL 迁移**

```sql
-- MySQL 执行
ALTER TABLE sys_task ADD COLUMN priority ENUM('normal', 'medium', 'urgent') DEFAULT 'normal' COMMENT '优先级';

-- 更新现有数据
UPDATE sys_task SET priority = 'normal' WHERE priority IS NULL;
```

---

## 验收检查

- [ ] 后端 API 支持 start_date, end_date, priority 参数
- [ ] 数据库 priority 字段已添加
- [ ] 前端查询面板可按日期范围筛选
- [ ] 任务列表显示优先级色条（正常无、中橙、紧急红）
- [ ] 新增任务可选择优先级
- [ ] 按钮有 hover/press 动画效果
- [ ] 卡片有悬浮效果
- [ ] 视觉效果柔和不刺眼

---

**Plan complete and saved to `docs/superpowers/plans/2026-06-10-task-management-ui-plan.md`**

**Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**