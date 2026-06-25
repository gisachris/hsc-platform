# Backend Architecture – FastAPI Server

This directory contains the production-ready FastAPI backend architecture.

## Structure Overview

* **`app/core/`**: Central configs, logging configuration, async DB sessions, password hashing, and token dependencies.
* **`app/api/v1/`**: Routing versions, custom endpoints error boundaries, request processing middleware and response encoders.
* **`app/models/`**: SQLAlchemy ORM declarations.
* **`app/schemas/`**: Pydantic input/output parsing schemas.
* **`app/repositories/`**: Repository layer abstractions isolating database transactions.
* **`app/services/`**: Feature coordination logic boundaries.

## Local Setup

1. **Install Poetry** (if not already installed):
   Refer to official poetry installation instructions.

2. **Install Dependencies**:
   ```bash
   poetry install
   ```
3. **Run Dev Server**:
   ```bash
   poetry run uvicorn app.main:app --reload
   ```
4. **Run Unit Tests**:
   ```bash
   poetry run pytest
   ```
