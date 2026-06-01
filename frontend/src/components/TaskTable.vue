<script setup lang="ts">
import type { Task } from '@/types'
import { Button } from '@/components/ui/button'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'

defineProps<{
  tasks: Task[]
}>()

const emit = defineEmits<{
  complete: [task: Task]
  defer: [task: Task]
  delete: [task: Task]
  detail: [task: Task]
}>()

function formatDate(date: string | null) {
  if (!date) return '-'
  return new Date(date).toLocaleString('zh-CN')
}
</script>

<template>
  <Table>
    <TableHeader>
      <TableRow>
        <TableHead>任务名称</TableHead>
        <TableHead>登记时间</TableHead>
        <TableHead>发布人</TableHead>
        <TableHead>备注</TableHead>
        <TableHead class="text-right">操作</TableHead>
      </TableRow>
    </TableHeader>
    <TableBody>
      <TableRow v-for="task in tasks" :key="task.id">
        <TableCell>{{ task.name }}</TableCell>
        <TableCell>{{ formatDate(task.register_time) }}</TableCell>
        <TableCell>{{ task.publisher }}</TableCell>
        <TableCell>{{ task.remark || '-' }}</TableCell>
        <TableCell class="text-right space-x-2">
          <Button variant="ghost" size="sm" @click="emit('detail', task)">详情</Button>
          <template v-if="!task.is_completed">
            <Button variant="ghost" size="sm" @click="emit('complete', task)">完成</Button>
            <Button variant="ghost" size="sm" @click="emit('defer', task)">顺延</Button>
            <Button variant="destructive" size="sm" @click="emit('delete', task)">删除</Button>
          </template>
        </TableCell>
      </TableRow>
      <TableRow v-if="tasks.length === 0">
        <TableCell colspan="5" class="text-center text-muted-foreground py-8">
          暂无数据
        </TableCell>
      </TableRow>
    </TableBody>
  </Table>
</template>