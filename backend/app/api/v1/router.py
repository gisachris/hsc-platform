from fastapi import APIRouter
from app.api.v1.routers import (
    analytics,
    attendance,
    audit,
    events,
    health,
    invitations,
    meetings,
    organization_members,
    organizations,
    polls,
    questions,
    registrations,
    roles,
    sessions,
    summaries,
    transcripts,
    users,
)

from app.modules.authentication.api import router as auth_router

api_router = APIRouter()

# Registering all 18 routers (including health checks)
api_router.include_router(health.router, tags=["Health Checks"])
api_router.include_router(auth_router.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(roles.router, prefix="/roles", tags=["Roles & Permissions"])
api_router.include_router(
    organizations.router, prefix="/organizations", tags=["Organizations"]
)
api_router.include_router(
    organization_members.router, tags=["Organization Members"]
)
api_router.include_router(events.router, prefix="/events", tags=["Events"])
api_router.include_router(sessions.router, prefix="/sessions", tags=["Sessions"])
api_router.include_router(meetings.router, prefix="/meetings", tags=["Meetings"])
api_router.include_router(
    registrations.router, prefix="/registrations", tags=["Registrations"]
)
api_router.include_router(
    invitations.router, prefix="/invitations", tags=["Invitations"]
)
api_router.include_router(
    attendance.router, prefix="/attendance", tags=["Attendance"]
)
api_router.include_router(
    questions.router, prefix="/questions", tags=["Q&A Audience Interaction"]
)
api_router.include_router(
    polls.router, prefix="/polls", tags=["Audience Live Polling"]
)
api_router.include_router(
    transcripts.router, prefix="/transcripts", tags=["AI Transcription"]
)
api_router.include_router(
    summaries.router, prefix="/summaries", tags=["AI Summarization"]
)
api_router.include_router(
    analytics.router, prefix="/analytics", tags=["Performance Analytics"]
)
api_router.include_router(audit.router, prefix="/audit", tags=["Security Auditing"])
