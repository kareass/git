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
const editingTaskPriority = ref(false)
const editingPriorityValue = ref<TaskPriority>('normal')

// 查询相关状态
const startDate = ref('')
const endDate = ref('')
const taskName = ref('')

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
    priority: selectedPriority.value || undefined,
    name: taskName.value || undefined
  })
}

// 查询方法
function handleQuery() {
  taskStore.fetchTasks({
    is_completed: activeTab.value === 'completed',
    start_date: startDate.value || undefined,
    end_date: endDate.value || undefined,
    priority: selectedPriority.value || undefined,
    name: taskName.value || undefined
  })
}

function handleReset() {
  startDate.value = ''
  endDate.value = ''
  selectedPriority.value = ''
  taskName.value = ''
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
  editingTaskPriority.value = false
  showDetailDialog.value = true
  await taskStore.fetchTaskDetails(task.id)
}

function startEditPriority() {
  if (selectedTask.value) {
    editingPriorityValue.value = selectedTask.value.priority
    editingTaskPriority.value = true
  }
}

async function saveTaskPriority() {
  if (!selectedTask.value) return
  await taskStore.updateTask(selectedTask.value.id, {
    priority: editingPriorityValue.value
  })
  selectedTask.value.priority = editingPriorityValue.value
  editingTaskPriority.value = false
  loadTasks()
}

function cancelEditPriority() {
  editingTaskPriority.value = false
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
                  <DialogContent glass class="max-w-4xl max-h-[99vh] min-h-[70vh]">
                    <DialogHeader class="flex-shrink-0 pb-4 border-b border-border/50">
                      <div class="flex items-center gap-3">
                        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500/20 to-teal-500/20 flex items-center justify-center">
                          <svg class="w-5 h-5 text-emerald-600 dark:text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
                        </div>
                        <div>
                          <DialogTitle class="text-xl font-semibold">新增任务</DialogTitle>
                          <p class="text-sm text-muted-foreground mt-0.5">创建新的任务</p>
                        </div>
                      </div>
                    </DialogHeader>
                    <div class="flex-1 min-h-0 overflow-y-auto py-5">
                      <form @submit.prevent="handleAddTask" class="space-y-5">
                        <div class="bg-gradient-to-r from-slate-50/80 to-slate-100/50 dark:from-slate-800/50 dark:to-slate-800/30 rounded-2xl p-5 border border-slate-200/50 dark:border-slate-700/50 space-y-4">
                          <FormField name="name">
                            <FormItem>
                              <FormLabel class="text-sm font-medium flex items-center gap-2">
                                <svg class="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"></path></svg>
                                任务名称
                              </FormLabel>
                              <FormControl>
                                <Input v-model="newTask.name" placeholder="请输入任务名称" required class="h-11 bg-white/80 dark:bg-slate-900/80 border-slate-200 dark:border-slate-700 rounded-xl focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500" />
                              </FormControl>
                            </FormItem>
                          </FormField>
                          <FormField name="priority">
                            <FormItem>
                              <FormLabel class="text-sm font-medium flex items-center gap-2">
                                <svg class="w-4 h-4 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                                优先级
                              </FormLabel>
                              <FormControl>
                                <select v-model="newTask.priority" class="h-11 rounded-xl border border-slate-200 dark:border-slate-700 bg-white/80 dark:bg-slate-900/80 px-3 w-full focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500">
                                  <option value="normal">正常</option>
                                  <option value="medium">中</option>
                                  <option value="urgent">紧急</option>
                                </select>
                              </FormControl>
                            </FormItem>
                          </FormField>
                          <FormField name="register_time">
                            <FormItem>
                              <FormLabel class="text-sm font-medium flex items-center gap-2">
                                <svg class="w-4 h-4 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                                登记时间
                              </FormLabel>
                              <FormControl>
                                <Input v-model="newTask.register_time" type="datetime-local" required class="h-11 bg-white/80 dark:bg-slate-900/80 border-slate-200 dark:border-slate-700 rounded-xl focus:ring-2 focus:ring-amber-500/20 focus:border-amber-500" />
                              </FormControl>
                            </FormItem>
                          </FormField>
                          <FormField name="publisher">
                            <FormItem>
                              <FormLabel class="text-sm font-medium flex items-center gap-2">
                                <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
                                发布人
                              </FormLabel>
                              <FormControl>
                                <Input v-model="newTask.publisher" required class="h-11 bg-white/80 dark:bg-slate-900/80 border-slate-200 dark:border-slate-700 rounded-xl focus:ring-2 focus:ring-slate-500/20 focus:border-slate-500" />
                              </FormControl>
                            </FormItem>
                          </FormField>
                          <FormField name="remark">
                            <FormItem>
                              <FormLabel class="text-sm font-medium flex items-center gap-2">
                                <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"></path></svg>
                                备注
                              </FormLabel>
                              <FormControl>
                                <Input v-model="newTask.remark" placeholder="可选" class="h-11 bg-white/80 dark:bg-slate-900/80 border-slate-200 dark:border-slate-700 rounded-xl focus:ring-2 focus:ring-slate-500/20 focus:border-slate-500" />
                              </FormControl>
                            </FormItem>
                          </FormField>
                        </div>
                        <div class="flex gap-3 pt-2">
                          <Button type="button" variant="outline" class="flex-1 h-11 rounded-xl" @click="showAddDialog = false">取消</Button>
                          <Button type="submit" class="flex-1 h-11 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-600 hover:to-teal-600 text-white border-0 shadow-lg shadow-emerald-500/25">
                            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                            保存
                          </Button>
                        </div>
                      </form>
                    </div>
                  </DialogContent>
                </Dialog>

                <!-- 任务详情弹窗 -->
                <Dialog :open="showDetailDialog" @update:open="(val) => showDetailDialog = val">
                  <DialogContent glass class="max-w-4xl max-h-[99vh] min-h-[70vh]">
                    <DialogHeader class="flex-shrink-0 pb-4 border-b border-border/50">
                      <div class="flex items-center gap-3">
                        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500/20 to-purple-500/20 flex items-center justify-center">
                          <svg class="w-5 h-5 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"></path></svg>
                        </div>
                        <div>
                          <DialogTitle class="text-xl font-semibold">任务详情</DialogTitle>
                          <p class="text-sm text-muted-foreground mt-0.5">{{ selectedTask?.name }}</p>
                        </div>
                      </div>
                    </DialogHeader>
                    <div class="flex-1 min-h-0 overflow-y-auto py-5 flex flex-col gap-5">
                      <!-- 基本信息卡片 -->
                      <div class="bg-gradient-to-r from-slate-50/80 to-slate-100/50 dark:from-slate-800/50 dark:to-slate-800/30 rounded-2xl p-5 border border-slate-200/50 dark:border-slate-700/50">
                        <h3 class="text-sm font-medium text-muted-foreground mb-4 flex items-center gap-2">
                          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                          基本信息
                        </h3>
                        <div class="grid grid-cols-2 gap-x-8 gap-y-4 text-sm">
                          <div class="flex items-center justify-between py-2 px-4 bg-white/60 dark:bg-slate-900/60 rounded-xl">
                            <span class="text-muted-foreground flex items-center gap-2">
                              <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                              登记时间
                            </span>
                            <span class="font-medium">{{ selectedTask?.register_time ? new Date(selectedTask.register_time).toLocaleString('zh-CN') : '-' }}</span>
                          </div>
                          <div class="flex items-center justify-between py-2 px-4 bg-white/60 dark:bg-slate-900/60 rounded-xl">
                            <span class="text-muted-foreground flex items-center gap-2">
                              <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
                              发布人
                            </span>
                            <span class="font-medium">{{ selectedTask?.publisher }}</span>
                          </div>
                          <div class="flex items-center justify-between py-2 px-4 bg-white/60 dark:bg-slate-900/60 rounded-xl">
                            <span class="text-muted-foreground flex items-center gap-2">
                              <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                              状态
                            </span>
                            <Badge :variant="selectedTask?.is_completed ? 'default' : 'secondary'" :class="selectedTask?.is_completed ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/50 dark:text-emerald-400' : 'bg-amber-100 text-amber-700 dark:bg-amber-900/50 dark:text-amber-400'">
                              {{ selectedTask?.is_completed ? '已完成' : '待处理' }}
                            </Badge>
                          </div>
                          <div class="flex items-center justify-between py-2 px-4 bg-white/60 dark:bg-slate-900/60 rounded-xl">
                            <span class="text-muted-foreground flex items-center gap-2">
                              <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                              优先级
                            </span>
                            <div class="flex items-center gap-2">
                              <template v-if="!editingTaskPriority">
                                <Badge :class="`badge-${selectedTask?.priority}`">
                                  {{ selectedTask?.priority === 'urgent' ? '紧急' : selectedTask?.priority === 'medium' ? '中' : '正常' }}
                                </Badge>
                                <Button variant="ghost" size="sm" class="h-7 px-3 text-xs hover:bg-slate-200 dark:hover:bg-slate-700" @click="startEditPriority">修改</Button>
                              </template>
                              <template v-else>
                                <select v-model="editingPriorityValue" class="h-8 rounded-lg border bg-white dark:bg-slate-900 px-2 text-sm">
                                  <option value="normal">正常</option>
                                  <option value="medium">中</option>
                                  <option value="urgent">紧急</option>
                                </select>
                                <Button variant="default" size="sm" class="h-7 px-3 text-xs bg-blue-600 hover:bg-blue-700" @click="saveTaskPriority">保存</Button>
                                <Button variant="ghost" size="sm" class="h-7 px-3 text-xs" @click="cancelEditPriority">取消</Button>
                              </template>
                            </div>
                          </div>
                          <div v-if="selectedTask?.complete_time" class="flex items-center justify-between py-2 px-4 bg-white/60 dark:bg-slate-900/60 rounded-xl">
                            <span class="text-muted-foreground flex items-center gap-2">
                              <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                              完成时间
                            </span>
                            <span class="font-medium text-emerald-600 dark:text-emerald-400">{{ new Date(selectedTask.complete_time).toLocaleString('zh-CN') }}</span>
                          </div>
                        </div>
                        <div v-if="selectedTask?.remark" class="mt-4 p-4 bg-white/60 dark:bg-slate-900/60 rounded-xl">
                          <span class="text-muted-foreground text-sm flex items-center gap-2 mb-2">
                            <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"></path></svg>
                            备注
                          </span>
                          <span class="text-sm font-medium">{{ selectedTask.remark }}</span>
                        </div>
                      </div>

                      <!-- 明细列表 -->
                      <div class="border border-slate-200/50 dark:border-slate-700/50 rounded-2xl p-5">
                        <div class="flex items-center justify-between mb-4">
                          <h3 class="font-medium flex items-center gap-2">
                            <svg class="w-4 h-4 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"></path></svg>
                            任务明细
                            <span class="text-xs text-muted-foreground font-normal">({{ taskStore.taskDetails.length }})</span>
                          </h3>
                          <Button variant="outline" size="sm" class="gap-2 bg-gradient-to-r from-blue-500 to-purple-500 text-white border-0 hover:from-blue-600 hover:to-purple-600" @click="openAddDetail">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
                            添加明细
                          </Button>
                        </div>
                        <div v-if="taskStore.taskDetails.length === 0" class="text-center py-12">
                          <div class="w-16 h-16 mx-auto mb-4 rounded-full bg-slate-100 dark:bg-slate-800 flex items-center justify-center">
                            <svg class="w-8 h-8 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"></path></svg>
                          </div>
                          <p class="text-muted-foreground text-sm">暂无明细，点击上方按钮添加</p>
                        </div>
                        <div v-else class="space-y-3 flex-1">
                          <div v-for="detail in taskStore.taskDetails" :key="detail.id" class="group flex items-center justify-between p-4 bg-gradient-to-r from-slate-50 to-slate-100/50 dark:from-slate-800/50 dark:to-slate-800/30 rounded-xl hover:from-blue-50 hover:to-purple-50 dark:hover:from-blue-900/20 dark:hover:to-purple-900/20 transition-all duration-200 border border-transparent hover:border-blue-200 dark:hover:border-blue-800">
                            <div class="flex items-center gap-4 flex-1">
                              <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500/10 to-purple-500/10 flex items-center justify-center flex-shrink-0">
                                <svg class="w-5 h-5 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path></svg>
                              </div>
                              <div class="flex-1 min-w-0">
                                <div class="font-medium text-sm">{{ detail.name }}</div>
                                <div class="flex items-center gap-4 mt-1.5 text-xs text-muted-foreground">
                                  <span v-if="detail.progress" class="flex items-center gap-1">
                                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                                    {{ detail.progress }}
                                  </span>
                                  <span v-if="detail.time" class="flex items-center gap-1">
                                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                                    {{ new Date(detail.time).toLocaleString('zh-CN') }}
                                  </span>
                                </div>
                                <div v-if="detail.remark" class="text-xs text-muted-foreground mt-1 truncate">{{ detail.remark }}</div>
                              </div>
                            </div>
                            <div class="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                              <Button variant="ghost" size="sm" class="h-8 px-3 text-xs hover:bg-blue-100 dark:hover:bg-blue-900/50 text-blue-600 dark:text-blue-400" @click="openEditDetail(detail)">编辑</Button>
                              <Button variant="ghost" size="sm" class="h-8 px-3 text-xs hover:bg-red-100 dark:hover:bg-red-900/50 text-red-600 dark:text-red-400" @click="handleDeleteDetail(detail.id)">删除</Button>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </DialogContent>
                </Dialog>

                <!-- 添加/编辑明细弹窗 -->
                <Dialog :open="showAddDetailDialog" @update:open="(val) => showAddDetailDialog = val">
                  <DialogContent glass class="max-w-2xl max-h-[99vh] min-h-[60vh]">
                    <DialogHeader class="flex-shrink-0 pb-4 border-b border-border/50">
                      <div class="flex items-center gap-3">
                        <div :class="editingDetail ? 'bg-gradient-to-br from-amber-500/20 to-orange-500/20' : 'bg-gradient-to-br from-emerald-500/20 to-teal-500/20'" class="w-10 h-10 rounded-xl flex items-center justify-center">
                          <svg v-if="editingDetail" class="w-5 h-5 text-amber-600 dark:text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>
                          <svg v-else class="w-5 h-5 text-emerald-600 dark:text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
                        </div>
                        <div>
                          <DialogTitle class="text-xl font-semibold">{{ editingDetail ? '编辑明细' : '添加明细' }}</DialogTitle>
                          <p class="text-sm text-muted-foreground mt-0.5">{{ editingDetail ? '修改任务明细信息' : '创建新的任务明细' }}</p>
                        </div>
                      </div>
                    </DialogHeader>
                    <div class="flex-1 min-h-0 overflow-y-auto py-5">
                      <form @submit.prevent="handleSaveDetail" class="space-y-5">
                        <div class="bg-gradient-to-r from-slate-50 to-slate-100/50 dark:from-slate-800/50 dark:to-slate-800/30 rounded-2xl p-5 space-y-4">
                          <FormField name="name">
                            <FormItem>
                              <FormLabel class="text-sm font-medium flex items-center gap-2">
                                <svg class="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"></path></svg>
                                明细名称
                              </FormLabel>
                              <FormControl>
                                <Input v-model="newDetail.name" placeholder="请输入明细名称" required class="h-11 bg-white/80 dark:bg-slate-900/80 border-slate-200 dark:border-slate-700 rounded-xl focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500" />
                              </FormControl>
                            </FormItem>
                          </FormField>
                          <FormField name="progress">
                            <FormItem>
                              <FormLabel class="text-sm font-medium flex items-center gap-2">
                                <svg class="w-4 h-4 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                                进度
                              </FormLabel>
                              <FormControl>
                                <Input v-model="newDetail.progress" placeholder="如: 80%" class="h-11 bg-white/80 dark:bg-slate-900/80 border-slate-200 dark:border-slate-700 rounded-xl focus:ring-2 focus:ring-purple-500/20 focus:border-purple-500" />
                              </FormControl>
                            </FormItem>
                          </FormField>
                          <FormField name="time">
                            <FormItem>
                              <FormLabel class="text-sm font-medium flex items-center gap-2">
                                <svg class="w-4 h-4 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                                时间
                              </FormLabel>
                              <FormControl>
                                <Input v-model="newDetail.time" type="datetime-local" class="h-11 bg-white/80 dark:bg-slate-900/80 border-slate-200 dark:border-slate-700 rounded-xl focus:ring-2 focus:ring-amber-500/20 focus:border-amber-500" />
                              </FormControl>
                            </FormItem>
                          </FormField>
                          <FormField name="remark">
                            <FormItem>
                              <FormLabel class="text-sm font-medium flex items-center gap-2">
                                <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"></path></svg>
                                备注
                              </FormLabel>
                              <FormControl>
                                <Input v-model="newDetail.remark" placeholder="可选" class="h-11 bg-white/80 dark:bg-slate-900/80 border-slate-200 dark:border-slate-700 rounded-xl focus:ring-2 focus:ring-slate-500/20 focus:border-slate-500" />
                              </FormControl>
                            </FormItem>
                          </FormField>
                        </div>
                        <div class="flex gap-3 pt-2">
                          <Button type="button" variant="outline" class="flex-1 h-11 rounded-xl" @click="showAddDetailDialog = false">取消</Button>
                          <Button type="submit" class="flex-1 h-11 rounded-xl bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 text-white border-0 shadow-lg shadow-blue-500/25">
                            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                            保存
                          </Button>
                        </div>
                      </form>
                    </div>
                  </DialogContent>
                </Dialog>
              </div>

              <!-- 查询面板 -->
              <div class="flex items-center gap-4 mb-6 p-4 glass-card rounded-lg">
                <div class="flex items-center gap-2">
                  <label class="text-sm font-medium">任务名称</label>
                  <Input v-model="taskName" placeholder="请输入任务名称" class="w-40" />
                </div>
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