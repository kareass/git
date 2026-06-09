import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { User } from '@/types'
import { authApi } from '@/api'

const TOKEN_EXPIRE_MS = 12 * 60 * 60 * 1000 // 12小时

export const useAuthStore = defineStore('auth', () => {
  const initToken = localStorage.getItem('token')
  const initTime = localStorage.getItem('token_time')

  // 检查token是否过期
  const isTokenExpired = initToken && initTime &&
    (Date.now() - Number(initTime)) > TOKEN_EXPIRE_MS

  const token = ref<string | null>(isTokenExpired ? null : initToken)
  const user = ref<User | null>(null)

  // 如果token已过期，清除存储
  if (isTokenExpired) {
    localStorage.removeItem('token')
    localStorage.removeItem('token_time')
  }

  async function login(username: string, password: string) {
    const { data } = await authApi.login({ username, password })
    token.value = data.access_token
    user.value = data.user
    localStorage.setItem('token', data.access_token)
    localStorage.setItem('token_time', Date.now().toString())
    return data
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('token_time')
  }

  return { token, user, login, logout }
})