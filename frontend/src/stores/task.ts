import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Task, TaskDetail, CreateTaskRequest, UpdateTaskRequest } from '@/types'
import { taskApi, taskDetailApi } from '@/api'

export const useTaskStore = defineStore('task', () => {
  const tasks = ref<Task[]>([])
  const currentTask = ref<Task | null>(null)
  const taskDetails = ref<TaskDetail[]>([])
  const loading = ref(false)
  const total = ref(0)
  const page = ref(1)
  const pageSize = ref(20)

  async function fetchTasks(params: { is_completed?: boolean; keyword?: string; sort?: string } = {}) {
    loading.value = true
    try {
      const { data } = await taskApi.list({ ...params, page: page.value, page_size: pageSize.value })
      tasks.value = data.items
      total.value = data.total
    } finally {
      loading.value = false
    }
  }

  async function createTask(task: CreateTaskRequest) {
    const { data } = await taskApi.create(task)
    tasks.value.unshift(data)
    return data
  }

  async function updateTask(id: number, task: UpdateTaskRequest) {
    const { data } = await taskApi.update(id, task)
    const index = tasks.value.findIndex(t => t.id === id)
    if (index !== -1) tasks.value[index] = data
    return data
  }

  async function deleteTask(id: number) {
    await taskApi.delete(id)
    tasks.value = tasks.value.filter(t => t.id !== id)
  }

  async function completeTask(id: number) {
    const { data } = await taskApi.complete(id)
    const index = tasks.value.findIndex(t => t.id === id)
    if (index !== -1) tasks.value.splice(index, 1)
    return data
  }

  async function deferTask(id: number) {
    const { data } = await taskApi.defer(id)
    tasks.value.unshift(data)
    return data
  }

  async function fetchTaskDetails(taskId: number) {
    const { data } = await taskDetailApi.list(taskId)
    taskDetails.value = data
  }

  async function createTaskDetail(taskId: number, detail: { name: string; progress: string; time?: string; remark?: string }) {
    const { data } = await taskDetailApi.create(taskId, detail)
    taskDetails.value.push(data)
    return data
  }

  async function updateTaskDetail(taskId: number, detailId: number, detail: { name?: string; progress?: string; time?: string; remark?: string }) {
    const { data } = await taskDetailApi.update(taskId, detailId, detail)
    const index = taskDetails.value.findIndex(d => d.id === detailId)
    if (index !== -1) taskDetails.value[index] = data
    return data
  }

  async function deleteTaskDetail(taskId: number, detailId: number) {
    await taskDetailApi.delete(taskId, detailId)
    taskDetails.value = taskDetails.value.filter(d => d.id !== detailId)
  }

  return {
    tasks,
    currentTask,
    taskDetails,
    loading,
    total,
    page,
    pageSize,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    completeTask,
    deferTask,
    fetchTaskDetails,
    createTaskDetail,
    updateTaskDetail,
    deleteTaskDetail,
  }
})