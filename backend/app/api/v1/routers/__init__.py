from fastapi import APIRouter
from app.api.v1.routers import health

api_router = APIRouter()

# Main API v1 routes
api_router.include_router(health.router, tags=["Health"])

# Placeholders for future milestones:
# api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
# api_router.include_router(users.router, prefix="/users", tags=["Users"])
# api_router.include_router(events.router, prefix="/events", tags=["Events"])
# api_router.include_router(organizations.router, prefix="/organizations", tags=["Organizations"])
# api_router.include_router(attendance.router, prefix="/attendance", tags=["Attendance"])
# api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
