import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/LoginView.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: '/',
      redirect: '/tasks',
    },
    {
      path: '/tasks',
      name: 'Tasks',
      component: () => import('@/views/TasksView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/tasks',
    },
  ],
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const tokenTime = localStorage.getItem('token_time')
  const TOKEN_EXPIRE_MS = 12 * 60 * 60 * 1000

  // 检查token是否过期
  const isTokenExpired = token && tokenTime &&
    (Date.now() - Number(tokenTime)) > TOKEN_EXPIRE_MS

  // 清除过期token
  if (isTokenExpired) {
    localStorage.removeItem('token')
    localStorage.removeItem('token_time')
  }

  if (to.meta.requiresAuth && isTokenExpired) {
    next('/login')
  } else if (to.path === '/login' && !isTokenExpired && token) {
    next('/tasks')
  } else {
    next()
  }
})

export default router