import api from './client'
import type {
  LoginRequest,
  LoginResponse,
  Task,
  CreateTaskRequest,
  UpdateTaskRequest,
  TaskDetail,
  CreateTaskDetailRequest,
  UpdateTaskDetailRequest,
  PageResult
} from '@/types'

// Auth APIs
export const authApi = {
  login: (data: LoginRequest) => api.post<LoginResponse>('/auth/login', data),
  refresh: () => api.post('/auth/refresh'),
}

// Task APIs
export const taskApi = {
  list: (params: { page?: number; page_size?: number; is_completed?: boolean; keyword?: string; sort?: string }) =>
    api.get<PageResult<Task>>('/tasks', { params }),

  get: (id: number) => api.get<Task>(`/tasks/${id}`),

  create: (data: CreateTaskRequest) => api.post<Task>('/tasks', data),

  update: (id: number, data: UpdateTaskRequest) => api.put<Task>(`/tasks/${id}`, data),

  delete: (id: number) => api.delete(`/tasks/${id}`),

  complete: (id: number) => api.post<Task>(`/tasks/${id}/complete`),

  defer: (id: number) => api.post<Task>(`/tasks/${id}/defer`),
}

// Task Detail APIs
export const taskDetailApi = {
  list: (taskId: number) => api.get<TaskDetail[]>(`/tasks/${taskId}/details`),

  create: (taskId: number, data: CreateTaskDetailRequest) =>
    api.post<TaskDetail>(`/tasks/${taskId}/details`, data),

  update: (taskId: number, detailId: number, data: UpdateTaskDetailRequest) =>
    api.put<TaskDetail>(`/tasks/${taskId}/details/${detailId}`, data),

  delete: (taskId: number, detailId: number) =>
    api.delete(`/tasks/${taskId}/details/${detailId}`),
}