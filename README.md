# Smart Hybrid Conference Management Platform

Welcome to the foundation of the Smart Hybrid Conference Management Platform. This repository serves as a modular, scalable architecture blueprint designed for interactive physical, virtual, and hybrid event management.

## Project Structure

```
.
├── backend/            # FastAPI Async Web Server
├── frontend/           # Vite + React + TS Interface
├── docs/               # Architecture and Setup documentation
├── .github/            # CI/CD Workflows
└── docker-compose.yml  # Local Container Orchestration Setup
```

## Quick Start

1. **Setup Local Environment Variables**:
   ```bash
   cp .env.example .env
   ```
2. **Setup and Run Backend**:
   ```bash
   cd backend
   poetry install
   poetry run uvicorn app.main:app --reload
   ```
3. **Setup and Run Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
4. **Access Applications**:
   - Frontend Application: [http://localhost:5173](http://localhost:5173)
   - Backend API Docs: [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs)
