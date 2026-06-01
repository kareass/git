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

export interface Task {
  id: number
  name: string
  register_time: string
  complete_time: string | null
  publisher: string
  is_completed: boolean
  remark: string | null
  user_id: number
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
}

export interface UpdateTaskRequest {
  name?: string
  register_time?: string
  publisher?: string
  is_completed?: boolean
  remark?: string
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