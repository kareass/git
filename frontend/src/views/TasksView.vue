<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useTaskStore } from '@/stores/task'
import { useAuthStore } from '@/stores/auth'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogFooter } from '@/components/ui/dialog'
import { Form, FormControl, FormField, FormItem, FormLabel } from '@/components/ui/form'
import { Badge } from '@/components/ui/badge'
import Sidebar from '@/components/Sidebar.vue'
import TaskTable from '@/components/TaskTable.vue'
import type { Task, TaskDetail, TaskPriority } from '@/types'

const taskStore = useTaskStore()
const authStore = useAuthStore()

const activeTab = ref<'pending' | 'completed'>('pending')
const showAddDialog = ref(false)
const selectedTask = ref<Task | null>(null)
const showDetailDialog = ref(false)
const showAddDetailDialog = ref(false)
const editingDetail = ref<TaskDetail | null>(null)

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

const newTask = ref({
  name: '',
  register_time: new Date().toISOString().slice(0, 16),
  publisher: authStore.user?.username || '',
  remark: '',
  priority: 'normal' as TaskPriority
})

const newDetail = ref({
  name: '',
  progress: '',
  time: new Date().toISOString().slice(0, 16),
  remark: ''
})

onMounted(() => {
  loadTasks()
})

async function loadTasks() {
  await taskStore.fetchTasks({
    is_completed: activeTab.value === 'completed',
    start_date: startDate.value || undefined,
    end_date: endDate.value || undefined,
    priority: selectedPriority.value || undefined
  })
}

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

function onTabChange(value: string) {
  activeTab.value = value as 'pending' | 'completed'
  loadTasks()
}

async function handleAddTask() {
  await taskStore.createTask({
    name: newTask.value.name,
    register_time: newTask.value.register_time.replace('T', ' '),
    publisher: newTask.value.publisher,
    remark: newTask.value.remark,
    priority: newTask.value.priority
  })
  showAddDialog.value = false
  newTask.value = { name: '', register_time: new Date().toISOString().slice(0, 16), publisher: authStore.user?.username || '', remark: '', priority: 'normal' as TaskPriority }
  loadTasks()
}

async function handleComplete(task: Task) {
  await taskStore.completeTask(task.id)
  loadTasks()
}

async function handleDefer(task: Task) {
  await taskStore.deferTask(task.id)
  loadTasks()
}

async function handleDelete(task: Task) {
  if (confirm('确定要删除这个任务吗？')) {
    await taskStore.deleteTask(task.id)
    loadTasks()
  }
}

async function openDetail(task: Task) {
  selectedTask.value = task
  showDetailDialog.value = true
  await taskStore.fetchTaskDetails(task.id)
}

function openAddDetail() {
  editingDetail.value = null
  newDetail.value = { name: '', progress: '', time: new Date().toISOString().slice(0, 16), remark: '' }
  showAddDetailDialog.value = true
}

function openEditDetail(detail: TaskDetail) {
  editingDetail.value = detail
  newDetail.value = {
    name: detail.name,
    progress: detail.progress,
    time: detail.time ? detail.time.slice(0, 16) : new Date().toISOString().slice(0, 16),
    remark: detail.remark || ''
  }
  showAddDetailDialog.value = true
}

async function handleSaveDetail() {
  if (!selectedTask.value) return
  if (editingDetail.value) {
    await taskStore.updateTaskDetail(selectedTask.value.id, editingDetail.value.id, {
      name: newDetail.value.name,
      progress: newDetail.value.progress,
      time: newDetail.value.time.replace('T', ' '),
      remark: newDetail.value.remark
    })
  } else {
    await taskStore.createTaskDetail(selectedTask.value.id, {
      name: newDetail.value.name,
      progress: newDetail.value.progress,
      time: newDetail.value.time.replace('T', ' '),
      remark: newDetail.value.remark
    })
  }
  showAddDetailDialog.value = false
  await taskStore.fetchTaskDetails(selectedTask.value.id)
}

async function handleDeleteDetail(detailId: number) {
  if (!selectedTask.value) return
  if (confirm('确定要删除这条明细吗？')) {
    await taskStore.deleteTaskDetail(selectedTask.value.id, detailId)
    await taskStore.fetchTaskDetails(selectedTask.value.id)
  }
}

function handleLogout() {
  authStore.logout()
  window.location.href = '/login'
}
</script>

<template>
  <div class="flex min-h-screen bg-gradient-to-br from-slate-100 via-slate-50 to-slate-200 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900">
    <Sidebar />

    <div class="flex-1 flex flex-col">
      <!-- Header -->
      <header class="h-16 border-b glass flex items-center justify-between px-6">
        <div class="flex items-center gap-4">
          <h1 class="text-xl font-semibold">任务管理</h1>
          <Badge variant="secondary" class="text-xs">MVP</Badge>
        </div>
        <div class="flex items-center gap-4">
          <div class="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-accent/50">
            <span class="text-sm text-muted-foreground">当前用户</span>
            <span class="text-sm font-medium">{{ authStore.user?.username }}</span>
          </div>
          <Button variant="outline" size="sm" class="btn-glow" @click="handleLogout">退出</Button>
        </div>
      </header>

      <!-- Main Content -->
      <main class="flex-1 p-6">
        <Card class="border-0 shadow-md bg-card/50" glass>
          <CardContent class="p-6">
            <Tabs :model-value="activeTab" @update:model-value="onTabChange">
              <div class="flex items-center justify-between mb-6">
                <div class="flex items-center gap-3">
                  <TabsList class="bg-accent/50">
                    <TabsTrigger value="pending" class="data-[state=active]:bg-background">待处理</TabsTrigger>
                    <TabsTrigger value="completed" class="data-[state=active]:bg-background">已完成</TabsTrigger>
                  </TabsList>
                  <Badge variant="outline" class="text-xs">
                    {{ taskStore.tasks.length }} 条记录
                  </Badge>
                </div>
                <Dialog :open="showAddDialog" @update:open="(val) => showAddDialog = val">
                  <DialogTrigger as-child>
                    <Button class="gap-2 btn-glow">
                      <span>+</span> 新增任务
                    </Button>
                  </DialogTrigger>
                  <DialogContent glass>
                    <DialogHeader>
                      <DialogTitle class="text-lg">新增任务</DialogTitle>
                    </DialogHeader>
                    <form @submit.prevent="handleAddTask" class="space-y-4">
                      <FormField name="name">
                        <FormItem>
                          <FormLabel>任务名称</FormLabel>
                          <FormControl>
                            <Input v-model="newTask.name" placeholder="请输入任务名称" required />
                          </FormControl>
                        </FormItem>
                      </FormField>
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
                      <FormField name="register_time">
                        <FormItem>
                          <FormLabel>登记时间</FormLabel>
                          <FormControl>
                            <Input v-model="newTask.register_time" type="datetime-local" required />
                          </FormControl>
                        </FormItem>
                      </FormField>
                      <FormField name="publisher">
                        <FormItem>
                          <FormLabel>发布人</FormLabel>
                          <FormControl>
                            <Input v-model="newTask.publisher" required />
                          </FormControl>
                        </FormItem>
                      </FormField>
                      <FormField name="remark">
                        <FormItem>
                          <FormLabel>备注</FormLabel>
                          <FormControl>
                            <Input v-model="newTask.remark" placeholder="可选" />
                          </FormControl>
                        </FormItem>
                      </FormField>
                      <Button type="submit" class="w-full">保存</Button>
                    </form>
                  </DialogContent>
                </Dialog>

                <!-- 任务详情弹窗 -->
                <Dialog :open="showDetailDialog" @update:open="(val) => showDetailDialog = val">
                  <DialogContent glass class="max-w-2xl max-h-[80vh] overflow-hidden flex flex-col">
                    <DialogHeader>
                      <DialogTitle class="text-lg">任务详情 - {{ selectedTask?.name }}</DialogTitle>
                    </DialogHeader>
                    <div class="flex-1 overflow-y-auto space-y-4 py-4">
                      <!-- 基本信息 -->
                      <div class="grid grid-cols-2 gap-4 text-sm">
                        <div>
                          <span class="text-muted-foreground">登记时间：</span>
                          <span>{{ selectedTask?.register_time ? new Date(selectedTask.register_time).toLocaleString('zh-CN') : '-' }}</span>
                        </div>
                        <div>
                          <span class="text-muted-foreground">发布人：</span>
                          <span>{{ selectedTask?.publisher }}</span>
                        </div>
                        <div>
                          <span class="text-muted-foreground">状态：</span>
                          <Badge :variant="selectedTask?.is_completed ? 'default' : 'secondary'">
                            {{ selectedTask?.is_completed ? '已完成' : '待处理' }}
                          </Badge>
                        </div>
                        <div v-if="selectedTask?.complete_time">
                          <span class="text-muted-foreground">完成时间：</span>
                          <span>{{ new Date(selectedTask.complete_time).toLocaleString('zh-CN') }}</span>
                        </div>
                      </div>
                      <div v-if="selectedTask?.remark" class="text-sm">
                        <span class="text-muted-foreground">备注：</span>
                        <span>{{ selectedTask.remark }}</span>
                      </div>

                      <!-- 明细列表 -->
                      <div class="border-t pt-4">
                        <div class="flex items-center justify-between mb-3">
                          <h4 class="font-medium text-sm">任务明细</h4>
                          <Button variant="outline" size="sm" @click="openAddDetail">+ 添加明细</Button>
                        </div>
                        <div v-if="taskStore.taskDetails.length === 0" class="text-center text-muted-foreground py-4 text-sm">
                          暂无明细
                        </div>
                        <div v-else class="space-y-2">
                          <div v-for="detail in taskStore.taskDetails" :key="detail.id" class="flex items-center justify-between p-3 bg-accent/30 rounded-lg text-sm">
                            <div class="flex-1">
                              <div class="font-medium">{{ detail.name }}</div>
                              <div class="text-muted-foreground text-xs mt-1">
                                进度: {{ detail.progress }} <span v-if="detail.time"> | 时间: {{ new Date(detail.time).toLocaleString('zh-CN') }}</span>
                              </div>
                              <div v-if="detail.remark" class="text-muted-foreground text-xs mt-1">备注: {{ detail.remark }}</div>
                            </div>
                            <div class="flex items-center gap-2">
                              <Button variant="ghost" size="sm" @click="openEditDetail(detail)">编辑</Button>
                              <Button variant="destructive" size="sm" @click="handleDeleteDetail(detail.id)">删除</Button>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </DialogContent>
                </Dialog>

                <!-- 添加/编辑明细弹窗 -->
                <Dialog :open="showAddDetailDialog" @update:open="(val) => showAddDetailDialog = val">
                  <DialogContent glass>
                    <DialogHeader>
                      <DialogTitle>{{ editingDetail ? '编辑明细' : '添加明细' }}</DialogTitle>
                    </DialogHeader>
                    <form @submit.prevent="handleSaveDetail" class="space-y-4">
                      <FormField name="name">
                        <FormItem>
                          <FormLabel>明细名称</FormLabel>
                          <FormControl>
                            <Input v-model="newDetail.name" placeholder="请输入明细名称" required />
                          </FormControl>
                        </FormItem>
                      </FormField>
                      <FormField name="progress">
                        <FormItem>
                          <FormLabel>进度</FormLabel>
                          <FormControl>
                            <Input v-model="newDetail.progress" placeholder="如: 80%" required />
                          </FormControl>
                        </FormItem>
                      </FormField>
                      <FormField name="time">
                        <FormItem>
                          <FormLabel>时间</FormLabel>
                          <FormControl>
                            <Input v-model="newDetail.time" type="datetime-local" />
                          </FormControl>
                        </FormItem>
                      </FormField>
                      <FormField name="remark">
                        <FormItem>
                          <FormLabel>备注</FormLabel>
                          <FormControl>
                            <Input v-model="newDetail.remark" placeholder="可选" />
                          </FormControl>
                        </FormItem>
                      </FormField>
                      <Button type="submit" class="w-full">保存</Button>
                    </form>
                  </DialogContent>
                </Dialog>
              </div>

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

              <TabsContent value="pending">
                <TaskTable :tasks="taskStore.tasks" @complete="handleComplete" @defer="handleDefer" @delete="handleDelete" @detail="openDetail" />
              </TabsContent>
              <TabsContent value="completed">
                <TaskTable :tasks="taskStore.tasks" @detail="openDetail" />
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>
      </main>
    </div>
  </div>
</template>