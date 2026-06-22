export interface User {
  id: number
  username: string
  role: 'admin' | 'user'
}

export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
  user: User
}

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

export interface TaskDetail {
  id: number
  task_id: number
  name: string
  progress: string
  time: string | null
  remark: string | null
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

export interface CreateTaskDetailRequest {
  name: string
  progress: string
  time?: string
  remark?: string
}

export interface UpdateTaskDetailRequest {
  name?: string
  progress?: string
  time?: string
  remark?: string
}

export interface PageResult<T> {
  items: T[]
  total: number
  page: number
  page_size: number
}

// WorkOrder types
export interface WorkOrder {
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

export interface WorkOrderDetail {
  id: number
  work_order_id: number
  name: string
  progress: string
  time: string | null
  remark: string | null
  created_at: string
  updated_at: string
}

export interface CreateWorkOrderRequest {
  name: string
  register_time: string
  publisher: string
  remark?: string
  priority?: TaskPriority
}

export interface UpdateWorkOrderRequest {
  name?: string
  register_time?: string
  publisher?: string
  is_completed?: boolean
  remark?: string
  priority?: TaskPriority
}

export interface CreateWorkOrderDetailRequest {
  name: string
  progress: string
  time?: string
  remark?: string
}

export interface UpdateWorkOrderDetailRequest {
  name?: string
  progress?: string
  time?: string
  remark?: string
}