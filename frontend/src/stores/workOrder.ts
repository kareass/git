import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { WorkOrder, WorkOrderDetail, CreateWorkOrderRequest, UpdateWorkOrderRequest } from '@/types'
import { workOrderApi, workOrderDetailApi } from '@/api'

export const useWorkOrderStore = defineStore('workOrder', () => {
  const workOrders = ref<WorkOrder[]>([])
  const currentWorkOrder = ref<WorkOrder | null>(null)
  const workOrderDetails = ref<WorkOrderDetail[]>([])
  const loading = ref(false)
  const total = ref(0)
  const page = ref(1)
  const pageSize = ref(20)

  async function fetchWorkOrders(params: {
    is_completed?: boolean
    start_date?: string
    end_date?: string
    priority?: string
    name?: string
  } = {}) {
    loading.value = true
    try {
      const { data } = await workOrderApi.list({
        ...params,
        page: page.value,
        page_size: pageSize.value
      })
      workOrders.value = data.items
      total.value = data.total
    } finally {
      loading.value = false
    }
  }

  async function createWorkOrder(workOrder: CreateWorkOrderRequest) {
    const { data } = await workOrderApi.create(workOrder)
    workOrders.value.unshift(data)
    return data
  }

  async function updateWorkOrder(id: number, workOrder: UpdateWorkOrderRequest) {
    const { data } = await workOrderApi.update(id, workOrder)
    const index = workOrders.value.findIndex(wo => wo.id === id)
    if (index !== -1) workOrders.value[index] = data
    return data
  }

  async function deleteWorkOrder(id: number) {
    await workOrderApi.delete(id)
    workOrders.value = workOrders.value.filter(wo => wo.id !== id)
  }

  async function completeWorkOrder(id: number) {
    const { data } = await workOrderApi.complete(id)
    const index = workOrders.value.findIndex(wo => wo.id === id)
    if (index !== -1) workOrders.value.splice(index, 1)
    return data
  }

  async function deferWorkOrder(id: number) {
    const { data } = await workOrderApi.defer(id)
    workOrders.value.unshift(data)
    return data
  }

  async function fetchWorkOrderDetails(workOrderId: number) {
    const { data } = await workOrderDetailApi.list(workOrderId)
    workOrderDetails.value = data
  }

  async function createWorkOrderDetail(workOrderId: number, detail: { name: string; progress: string; time?: string; remark?: string }) {
    const { data } = await workOrderDetailApi.create(workOrderId, detail)
    workOrderDetails.value.push(data)
    return data
  }

  async function updateWorkOrderDetail(workOrderId: number, detailId: number, detail: { name?: string; progress?: string; time?: string; remark?: string }) {
    const { data } = await workOrderDetailApi.update(workOrderId, detailId, detail)
    const index = workOrderDetails.value.findIndex(d => d.id === detailId)
    if (index !== -1) workOrderDetails.value[index] = data
    return data
  }

  async function deleteWorkOrderDetail(workOrderId: number, detailId: number) {
    await workOrderDetailApi.delete(workOrderId, detailId)
    workOrderDetails.value = workOrderDetails.value.filter(d => d.id !== detailId)
  }

  return {
    workOrders,
    currentWorkOrder,
    workOrderDetails,
    loading,
    total,
    page,
    pageSize,
    fetchWorkOrders,
    createWorkOrder,
    updateWorkOrder,
    deleteWorkOrder,
    completeWorkOrder,
    deferWorkOrder,
    fetchWorkOrderDetails,
    createWorkOrderDetail,
    updateWorkOrderDetail,
    deleteWorkOrderDetail,
  }
})
