# Environment Setup Guide

The application loads runtime properties from the local `.env` configuration file using Pydantic Settings.

## Variable Reference

| Variable Name | Description | Default / Example |
|---|---|---|
| `PROJECT_NAME` | Branding title of the conference instance | `Smart Hybrid Conference Management Platform` |
| `ENV` | Execution flag (`development`, `staging`, `production`) | `development` |
| `DEBUG` | Verbose exceptions tracing and database echo toggle | `true` |
| `SECRET_KEY` | Hex-encoded key for generating secure JWT payloads | `918db4bb4b553e198642cd02a832c3...` |
| `ALGORITHM` | JWT Signature algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Lifecycle limit for authorization headers (minutes) | `11520` (8 days) |
| `DATABASE_URL` | SQLAlchemy connection string | `postgresql+asyncpg://postgres:secret@db:5432/db` |
| `BACKEND_CORS_ORIGINS` | Array of authorized client origins | `["http://localhost:5173"]` |
| `PGADMIN_DEFAULT_EMAIL` | Database panel login credential | `admin@conference-platform.com` |
| `PGADMIN_DEFAULT_PASSWORD` | Database panel login credential | `admin_secret_password` |
