<script setup lang="ts">
import type { WorkOrder, TaskPriority } from '@/types'
import { Button } from '@/components/ui/button'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Badge } from '@/components/ui/badge'

defineProps<{
  workOrders: WorkOrder[]
}>()

const emit = defineEmits<{
  complete: [workOrder: WorkOrder]
  defer: [workOrder: WorkOrder]
  delete: [workOrder: WorkOrder]
  detail: [workOrder: WorkOrder]
}>()

function getPriorityClass(priority: TaskPriority): string {
  const classMap = {
    normal: 'priority-bar-normal',
    medium: 'priority-bar-medium',
    urgent: 'priority-bar-urgent'
  }
  return classMap[priority] || 'priority-bar-normal'
}

function formatDate(date: string | null) {
  if (!date) return '-'
  return new Date(date).toLocaleString('zh-CN')
}
</script>

<template>
  <Table>
    <TableHeader>
      <TableRow>
        <TableHead class="w-4"></TableHead>
        <TableHead>工单名称</TableHead>
        <TableHead>优先级</TableHead>
        <TableHead>登记时间</TableHead>
        <TableHead>发布人</TableHead>
        <TableHead>备注</TableHead>
        <TableHead class="text-right">操作</TableHead>
      </TableRow>
    </TableHeader>
    <TableBody>
      <TableRow
        v-for="workOrder in workOrders"
        :key="workOrder.id"
        :class="['transition-colors hover:bg-accent/30', getPriorityClass(workOrder.priority)]"
      >
        <TableCell></TableCell>
        <TableCell class="font-medium">{{ workOrder.name }}</TableCell>
        <TableCell>
          <Badge :class="['badge-' + workOrder.priority]">
            {{ workOrder.priority === 'normal' ? '正常' : workOrder.priority === 'medium' ? '中' : '紧急' }}
          </Badge>
        </TableCell>
        <TableCell>{{ formatDate(workOrder.register_time) }}</TableCell>
        <TableCell>{{ workOrder.publisher }}</TableCell>
        <TableCell>{{ workOrder.remark || '-' }}</TableCell>
        <TableCell class="text-right space-x-2">
          <Button variant="ghost" size="sm" class="btn-glow" @click="emit('detail', workOrder)">详情</Button>
          <template v-if="!workOrder.is_completed">
            <Button variant="ghost" size="sm" class="btn-glow" @click="emit('complete', workOrder)">完成</Button>
            <Button variant="ghost" size="sm" class="btn-glow" @click="emit('defer', workOrder)">顺延</Button>
            <Button variant="destructive" size="sm" class="btn-glow" @click="emit('delete', workOrder)">删除</Button>
          </template>
        </TableCell>
      </TableRow>
      <TableRow v-if="workOrders.length === 0">
        <TableCell colspan="7" class="text-center text-muted-foreground py-8">
          暂无数据
        </TableCell>
      </TableRow>
    </TableBody>
  </Table>
</template>
