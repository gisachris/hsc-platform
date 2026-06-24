from fastapi import APIRouter, status
from app.schemas.response import APIResponse

router = APIRouter()


@router.post(
    "/login",
    response_model=APIResponse[dict],
    status_code=status.HTTP_200_OK,
    summary="User authentication login",
)
async def login():
    """Authenticates user credentials and returns a Bearer JWT token."""
    return {
        "success": True,
        "message": "Login successful",
        "data": {
            "access_token": "mock_jwt_token_payload",
            "token_type": "bearer",
        },
    }


@router.post(
    "/register",
    response_model=APIResponse[dict],
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user account",
)
async def register():
    """Creates a new user profile with standard attendee privileges."""
    return {
        "success": True,
        "message": "User registered successfully",
        "data": {"id": "mock_user_uuid", "email": "user@example.com"},
    }


@router.post(
    "/refresh-token",
    response_model=APIResponse[dict],
    summary="Refresh authorization token",
)
async def refresh_token():
    """Generates a new Bearer JWT using a valid refresh token."""
    return {
        "success": True,
        "message": "Token refreshed successfully",
        "data": {"access_token": "new_mock_jwt_token_payload"},
    }


@router.post(
    "/forgot-password",
    response_model=APIResponse[dict],
    summary="Request password recovery",
)
async def forgot_password():
    """Sends a password reset notification email to the registered address."""
    return {
        "success": True,
        "message": "Password recovery email dispatched",
        "data": None,
    }
