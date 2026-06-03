# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Internal work management system (需求开发事项统计) with MVP scope: Login + Task Registration module.

- **Frontend**: Vue 3 + Vite + TypeScript + Shadcn UI + Tailwind CSS v4
- **Backend**: Python + FastAPI + SQLAlchemy 2.0 (async)
- **Database**: MySQL 8.0

## Project Structure

```
需求开发事项统计/
├── frontend/               # Vue 3 SPA
│   ├── src/
│   │   ├── api/           # Axios API client with JWT interceptor
│   │   ├── components/     # Shadcn UI components + custom (Sidebar, TaskTable)
│   │   ├── stores/        # Pinia stores (auth, task)
│   │   ├── views/         # Page components (LoginView, TasksView)
│   │   ├── router/        # Vue Router with auth guards
│   │   └── types/         # TypeScript interfaces
│   ├── vite.config.ts     # Vite config with /api proxy to backend :8000
│   └── package.json
├── backend/                # FastAPI
│   ├── app/
│   │   ├── api/routes/    # Auth + Task REST endpoints
│   │   ├── core/          # JWT + bcrypt security
│   │   ├── models/        # SQLAlchemy models (User, Task, TaskDetail)
│   │   ├── schemas/       # Pydantic request/response models
│   │   ├── services/      # Business logic (AuthService, TaskService)
│   │   ├── config.py      # Settings via pydantic-settings
│   │   └── database.py    # Async MySQL connection
│   └── requirements.txt
├── docs/
│   ├── sql/init.sql       # MySQL schema + seed data
│   └── backend-design.md  # API design documentation
└── 项目设计方案.md
```

## Commands

### Frontend
```bash
cd frontend
npm run dev          # Start dev server (localhost:5173)
npm run build        # Production build
npm run preview      # Preview production build
```

### Backend
```bash
cd backend
# Install dependencies
pip install -r requirements.txt

# Start server (requires MySQL running)
E:/anaconda/file/python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Database
```bash
# MySQL is installed at PHPStudy - start via PHPStudy tray
# Initialize database
E:/wangluoanq1/PHP/phpstudy_pro/Extensions/MySQL8.0.12/bin/mysql.exe -u root -proot < docs/sql/init.sql
```

## API Endpoints

### Auth
- `POST /api/auth/login` - Login (returns JWT)
- `POST /api/auth/register` - Register user (admin only)
- `GET /api/auth/me` - Get current user

### Tasks
- `GET /api/tasks` - List tasks (supports `is_completed`, `page`, `page_size`)
- `GET /api/tasks/{id}` - Get single task
- `POST /api/tasks` - Create task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task
- `POST /api/tasks/{id}/complete` - Mark complete
- `POST /api/tasks/{id}/defer` - Defer to tomorrow

### Task Details
- `GET /api/tasks/{task_id}/details` - List details
- `POST /api/tasks/{task_id}/details` - Add detail
- `PUT /api/tasks/{task_id}/details/{id}` - Update detail
- `DELETE /api/tasks/{task_id}/details/{id}` - Delete detail

## Test Credentials

- Username: `admin` / Password: `admin123`
- Username: `user1` / Password: `admin123`

## Key Implementation Details

- JWT token stored in localStorage, sent via `Authorization: Bearer <token>` header
- Frontend proxies `/api/*` requests to `localhost:8000` (Vite proxy)
- All `/api/*` endpoints require authentication except `/api/auth/login`
- Task defer creates new task for tomorrow and marks original as complete
- Passwords hashed with bcrypt (cost factor 12)

## Testing

```bash
cd frontend
npm test                    # Run all tests
npx playwright test         # Run Playwright E2E tests
npx playwright test tests/app.spec.ts --reporter=line  # Run specific test file
npx playwright show-report  # View HTML test report
```

**Playwright test coverage:**
- Login page loading
- User login (admin/admin123)
- Task list page
- Create new task
- Task detail dialog

## Git

```bash
git status                  # Check status
git log --oneline -5        # View recent commits
git push origin main        # Push to remote
```

**Remote:** `https://github.com/kareass/git.git`