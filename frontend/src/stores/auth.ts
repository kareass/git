import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { User } from '@/types'
import { authApi } from '@/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const user = ref<User | null>(null)

  async function login(username: string, password: string) {
    const { data } = await authApi.login({ username, password })
    token.value = data.access_token
    user.value = data.user
    localStorage.setItem('token', data.access_token)
    return data
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
  }

  return { token, user, login, logout }
})