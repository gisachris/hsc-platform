# Architecture Overview

This project uses a modular monolith design, separating application features into clear logical tiers to facilitate decoupling and testing.

## Design Patterns

### Repository Pattern & Service Layer
1. **Controller Layer (Routers)**: Translates incoming REST queries, validates request bodies using Pydantic, and forwards instructions to the service layer.
2. **Service Layer**: Handles coordination, transactional state boundary validation, and orchestration logic.
3. **Repository Layer**: Provides abstraction for data access and queries, allowing switching of database backends without touching core logic.

```
Request ────> Router ────> Service ────> Repository ────> Database
```

## Frontend Design Layer

### Feature-Based Organization
The frontend uses feature-centric modularity. Instead of putting all components in a global `/components` folder, they are split by domain context:
- `/features/auth` (future milestones)
- `/features/events` (future milestones)
Common shared controls (Buttons, inputs, containers) stay in `/components/ui`.
Layout components live in `/layouts/`.
Routing configurations map routes in `/routes/`.
Theme configurations and state queries wrapper in `/contexts/` and `/app/`.
