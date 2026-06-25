# Installation & Running Guide

This guide details steps to set up the Smart Hybrid Conference Management Platform in your development workspace.

## Prerequisites

- [Node.js v20+](https://nodejs.org) and [npm](https://www.npmjs.com).
- [Python 3.11+](https://www.python.org) and [Poetry](https://python-poetry.org).

## Step-by-Step

### 1. Configure Local Environment
Clone the `.env.example` file to `.env`:
```bash
cp .env.example .env
```

### 2. Stand Up Backend (Poetry)
Run:
```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload
```

### 3. Stand Up Frontend (NPM)
Run:
```bash
cd frontend
npm install
npm run dev
```

## Verify System Operations
- Front-End Live Preview: [http://localhost:5173](http://localhost:5173)
- API OpenAPI Swagger Docs: [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs)
