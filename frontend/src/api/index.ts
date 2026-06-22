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
  PageResult,
  WorkOrder,
  CreateWorkOrderRequest,
  UpdateWorkOrderRequest,
  WorkOrderDetail,
  CreateWorkOrderDetailRequest,
  UpdateWorkOrderDetailRequest,
} from '@/types'

// Auth APIs
export const authApi = {
  login: (data: LoginRequest) => api.post<LoginResponse>('/auth/login', data),
  refresh: () => api.post('/auth/refresh'),
}

// Task APIs
export const taskApi = {
  list: (params: {
    is_completed?: boolean
    start_date?: string
    end_date?: string
    priority?: string
    name?: string
    page?: number
    page_size?: number
  }) => api.get<PageResult<Task>>('/tasks', { params }),

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

// WorkOrder APIs
export const workOrderApi = {
  list: (params: {
    is_completed?: boolean
    start_date?: string
    end_date?: string
    priority?: string
    name?: string
    page?: number
    page_size?: number
  }) => api.get<PageResult<WorkOrder>>('/work-orders', { params }),

  get: (id: number) => api.get<WorkOrder>(`/work-orders/${id}`),

  create: (data: CreateWorkOrderRequest) => api.post<WorkOrder>('/work-orders', data),

  update: (id: number, data: UpdateWorkOrderRequest) => api.put<WorkOrder>(`/work-orders/${id}`, data),

  delete: (id: number) => api.delete(`/work-orders/${id}`),

  complete: (id: number) => api.post<WorkOrder>(`/work-orders/${id}/complete`),

  defer: (id: number) => api.post<WorkOrder>(`/work-orders/${id}/defer`),
}

// WorkOrder Detail APIs
export const workOrderDetailApi = {
  list: (workOrderId: number) => api.get<WorkOrderDetail[]>(`/work-orders/${workOrderId}/details`),

  create: (workOrderId: number, data: CreateWorkOrderDetailRequest) =>
    api.post<WorkOrderDetail>(`/work-orders/${workOrderId}/details`, data),

  update: (workOrderId: number, detailId: number, data: UpdateWorkOrderDetailRequest) =>
    api.put<WorkOrderDetail>(`/work-orders/${workOrderId}/details/${detailId}`, data),

  delete: (workOrderId: number, detailId: number) =>
    api.delete(`/work-orders/${workOrderId}/details/${detailId}`),
}