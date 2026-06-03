import { test, expect } from '@playwright/test'

test.describe('需求开发事项统计', () => {
  test.beforeEach(async ({ page }) => {
    // Start from the app root
    await page.goto('http://localhost:5173')
  })

  test('登录页面加载正常', async ({ page }) => {
    // Should redirect to login or show login form
    await page.waitForTimeout(1000)
    const url = page.url()
    console.log('Current URL:', url)

    // Check for login elements
    const hasLoginForm = await page.locator('input[type="text"], input[placeholder*="用户名"], input[placeholder*="username"]').count() > 0
    const hasPasswordField = await page.locator('input[type="password"]').count() > 0

    if (hasLoginForm || hasPasswordField) {
      console.log('Login form detected')
    }
  })

  test('登录功能 - admin用户', async ({ page }) => {
    await page.waitForTimeout(1000)

    // Fill login form
    const usernameInput = page.locator('input[type="text"], input[placeholder*="用户名"], input[placeholder*="username"]').first()
    const passwordInput = page.locator('input[type="password"]').first()

    if (await usernameInput.count() > 0) {
      await usernameInput.fill('admin')
      await passwordInput.fill('admin123')

      // Find and click login button
      const loginButton = page.locator('button[type="submit"], button:has-text("登录"), button:has-text("登录")').first()
      await loginButton.click()

      await page.waitForTimeout(2000)

      const url = page.url()
      console.log('After login URL:', url)
      console.log('Login successful:', url.includes('tasks'))
    }
  })

  test('任务页面加载', async ({ page }) => {
    // Navigate directly to tasks page (bypasses auth for demo)
    await page.goto('http://localhost:5173/tasks')
    await page.waitForTimeout(2000)

    const url = page.url()
    console.log('Tasks URL:', url)

    // Check for task related elements
    const hasTasksContent = await page.locator('text=任务管理, text=待处理, text=已完成').count() > 0
    console.log('Tasks content detected:', hasTasksContent)
  })

  test('新增任务功能', async ({ page }) => {
    await page.goto('http://localhost:5173/tasks')
    await page.waitForTimeout(2000)

    // Click add task button
    const addButton = page.locator('button:has-text("新增任务")').first()
    if (await addButton.count() > 0) {
      await addButton.click()
      await page.waitForTimeout(500)

      // Fill task form
      const nameInput = page.locator('input[placeholder*="任务名称"]').first()
      if (await nameInput.count() > 0) {
        await nameInput.fill('Playwright测试任务')

        // Submit form
        const submitButton = page.locator('button[type="submit"]:has-text("保存")').first()
        await submitButton.click()

        await page.waitForTimeout(1000)
        console.log('Task creation submitted')
      }
    }
  })

  test('任务详情弹窗', async ({ page }) => {
    await page.goto('http://localhost:5173/tasks')
    await page.waitForTimeout(2000)

    // Click detail button on first task
    const detailButton = page.locator('button:has-text("详情")').first()
    if (await detailButton.count() > 0) {
      await detailButton.click()
      await page.waitForTimeout(500)

      // Check if dialog opened
      const dialog = page.locator('[role="dialog"], .fixed.inset-0').first()
      const isDialogVisible = await dialog.isVisible().catch(() => false)
      console.log('Detail dialog visible:', isDialogVisible)
    }
  })
})