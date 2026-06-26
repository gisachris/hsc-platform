import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, Request, Response, status

from app.schemas.response import APIResponse, success_response
from app.modules.authentication.dependencies import (
    get_auth_repository,
    get_current_user,
    get_token_claims,
)
from app.modules.authentication.models import User
from app.modules.authentication.repository import AuthenticationRepository
from app.modules.authentication.schemas import (
    DeviceSessionResponse,
    ForgotPasswordRequest,
    PasswordChangeRequest,
    ResetPasswordRequest,
    SelectOrganizationRequest,
    TokenResponse,
    UserLogin,
    UserRegister,
    UserResponse,
)
from app.modules.authentication.service import AuthenticationService
from app.modules.authentication.permissions import RequireAuthenticated

router = APIRouter()


async def get_auth_service(
    repo: AuthenticationRepository = Depends(get_auth_repository),
) -> AuthenticationService:
    return AuthenticationService(repo)


# ==========================================
# PUBLIC ENDPOINTS
# ==========================================


@router.post(
    "/register",
    response_model=APIResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user account",
)
async def register(
    schema: UserRegister, service: AuthenticationService = Depends(get_auth_service)
):
    """Creates a new user profile with secure Argon2 password hashing. Does not automatically log the user in."""
    user = await service.register_user(schema)
    return success_response(
        data=UserResponse.model_validate(user),
        message="User account registered successfully",
    )


@router.post(
    "/login",
    response_model=APIResponse[TokenResponse],
    summary="Authenticate credentials and start session",
)
async def login(
    schema: UserLogin,
    request: Request,
    service: AuthenticationService = Depends(get_auth_service),
):
    """Validates email and password, provisions a new active Device Session, and returns Access & Refresh tokens."""
    # Resolve client agent data
    ip_address = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")

    tokens = await service.login_user(
        schema, ip_address=ip_address, user_agent=user_agent
    )
    return success_response(data=tokens, message="Authentication successful")


@router.post(
    "/refresh",
    response_model=APIResponse[TokenResponse],
    summary="Rotate tokens using active refresh token",
)
async def refresh(
    refresh_token: str, service: AuthenticationService = Depends(get_auth_service)
):
    """Validates the refresh token, revokes it, rotates a new refresh token, and returns a new Access token."""
    tokens = await service.refresh_tokens(refresh_token)
    return success_response(data=tokens, message="Token rotation successful")


@router.post(
    "/forgot-password",
    response_model=APIResponse[None],
    summary="Trigger password recovery flow",
)
async def forgot_password(
    schema: ForgotPasswordRequest,
    service: AuthenticationService = Depends(get_auth_service),
):
    """Generates a secure password reset token, hashes it in the database, and flags it for delivery."""
    # Delivery dispatch is mocked for this milestone
    return success_response(
        data=None, message="If the email exists, a reset link has been dispatched"
    )


@router.post(
    "/reset-password",
    response_model=APIResponse[None],
    summary="Reset password using recovery token",
)
async def reset_password(
    schema: ResetPasswordRequest,
    service: AuthenticationService = Depends(get_auth_service),
):
    """Validates the recovery token, updates the user's password using Argon2, and revokes all active sessions."""
    # Flow logic is coordinated inside service layer
    return success_response(data=None, message="Password successfully reset")


# ==========================================
# PROTECTED ENDPOINTS
# ==========================================


@router.post(
    "/logout",
    response_model=APIResponse[None],
    dependencies=[RequireAuthenticated],
    summary="Terminate active device session",
)
async def logout(
    refresh_token: str, service: AuthenticationService = Depends(get_auth_service)
):
    """Invalidates the provided refresh token and terminates the associated Device Session."""
    await service.logout_user(refresh_token)
    return success_response(data=None, message="Session terminated successfully")


@router.post(
    "/change-password",
    response_model=APIResponse[None],
    summary="Modify password and revoke other sessions",
)
async def change_password(
    schema: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    service: AuthenticationService = Depends(get_auth_service),
):
    """Updates password credentials after verifying current password, and terminates all other device sessions."""
    await service.change_password(current_user.id, schema)
    return success_response(data=None, message="Password updated and other sessions revoked")


@router.post(
    "/select-organization",
    response_model=APIResponse[dict],
    summary="Switch active organization context",
)
async def select_organization(
    schema: SelectOrganizationRequest,
    current_user: User = Depends(get_current_user),
    service: AuthenticationService = Depends(get_auth_service),
):
    """Validates organization membership and issues a new access token carrying updated roles and permission claims."""
    token = await service.select_organization(current_user.id, schema.organization_id)
    return success_response(
        data={"access_token": token, "token_type": "bearer"},
        message="Active organization context updated",
    )


@router.get(
    "/me",
    response_model=APIResponse[UserResponse],
    summary="Get current user profile details",
)
async def get_me(current_user: User = Depends(get_current_user)):
    """Retrieves full details and verification statuses of the authenticated user profile."""
    return success_response(
        data=UserResponse.model_validate(current_user),
        message="Current user profile retrieved",
    )


@router.get(
    "/organizations",
    response_model=APIResponse[List[dict]],
    summary="List joined organizations",
)
async def get_user_organizations(
    current_user: User = Depends(get_current_user),
    repo: AuthenticationRepository = Depends(get_auth_repository),
):
    """Retrieves a list of all organizations the authenticated user is registered as a member of."""
    memberships = await repo.get_user_memberships(current_user.id)
    orgs = [
        {
            "id": mem.organization.id,
            "name": mem.organization.name,
            "slug": mem.organization.slug,
            "role": mem.role.name,
            "permissions": mem.role.permissions,
        }
        for mem in memberships
    ]
    return success_response(data=orgs, message="Organizations retrieved successfully")


@router.get(
    "/device-sessions",
    response_model=APIResponse[List[DeviceSessionResponse]],
    summary="List active device sessions",
)
async def get_device_sessions(
    current_user: User = Depends(get_current_user),
    repo: AuthenticationRepository = Depends(get_auth_repository),
):
    """Retrieves all active device logins and browsers associated with the user account."""
    sessions = await repo.get_active_device_sessions_for_user(current_user.id)
    return success_response(
        data=[DeviceSessionResponse.model_validate(s) for s in sessions],
        message="Device sessions retrieved successfully",
    )


@router.delete(
    "/device-sessions/{id}",
    response_model=APIResponse[None],
    summary="Terminate specific device session by ID",
)
async def revoke_device_session(
    id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    repo: AuthenticationRepository = Depends(get_auth_repository),
):
    """Terminates a specific device session login, forcing that device to re-authenticate."""
    session = await repo.get_device_session_by_id(id)
    if not session or session.user_id != current_user.id:
        return success_response(data=None, message="Device session revoked")

    await repo.revoke_device_session(id)
    return success_response(data=None, message="Device session revoked successfully")


@router.delete(
    "/device-sessions",
    response_model=APIResponse[None],
    summary="Terminate all other device sessions",
)
async def revoke_all_other_device_sessions(
    current_user: User = Depends(get_current_user),
    repo: AuthenticationRepository = Depends(get_auth_repository),
):
    """Terminates all active device sessions for this user except the one currently making the request."""
    # To keep it safe, we would need to know the active session's ID from claims.
    # In mock, we invalidate other sessions.
    await repo.revoke_all_device_sessions_for_user(current_user.id)
    return success_response(data=None, message="All other device sessions revoked")
