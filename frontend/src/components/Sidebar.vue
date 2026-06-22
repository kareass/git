<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { cn } from '@/lib/utils'

const router = useRouter()
const route = useRoute()

const menuItems = [
  { icon: '📋', label: '任务管理', path: '/tasks' },
  { icon: '📄', label: '工单管理', path: '/work-orders' },
  { icon: '📊', label: '需求统计', path: '/demands', badge: '预' },
  { icon: '👤', label: '用户管理', path: '/users', badge: '预' },
  { icon: '⚙️', label: '系统设置', path: '/settings', badge: '预' },
]

const isCollapsed = ref(false)

const currentPath = computed(() => route.path)

function isActive(path: string): boolean {
  return currentPath.value === path
}

function navigate(path: string) {
  if (path !== '/tasks' && path !== '/work-orders') {
    alert('该功能模块正在开发中...')
    return
  }
  router.push(path)
}
</script>

<template>
  <aside
    :class="cn(
      'flex flex-col border-r bg-sidebar transition-all duration-300 glass-sidebar',
      isCollapsed ? 'w-16' : 'w-64'
    )"
  >
    <!-- Logo -->
    <div class="flex items-center h-16 px-4 border-b">
      <span class="text-xl font-bold bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent">
        {{ isCollapsed ? 'W' : 'WORK' }}
      </span>
      <span v-if="!isCollapsed" class="ml-2 text-sm text-muted-foreground">管理系统</span>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 p-3 space-y-1">
      <button
        v-for="item in menuItems"
        :key="item.path"
        @click="navigate(item.path)"
        :class="cn(
          'w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all',
          isActive(item.path)
            ? 'bg-primary text-primary-foreground shadow-sm'
            : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
        )"
      >
        <span class="text-lg">{{ item.icon }}</span>
        <span v-if="!isCollapsed" class="flex-1 text-left">{{ item.label }}</span>
        <Badge
          v-if="!isCollapsed && item.badge"
          variant="secondary"
          class="text-[10px] px-1.5 py-0.5"
        >
          {{ item.badge }}
        </Badge>
      </button>
    </nav>

    <!-- Collapse Button -->
    <div class="p-3 border-t">
      <Button
        variant="ghost"
        size="sm"
        class="w-full justify-center"
        @click="isCollapsed = !isCollapsed"
      >
        {{ isCollapsed ? '→' : '←' }}
      </Button>
    </div>
  </aside>
</template>