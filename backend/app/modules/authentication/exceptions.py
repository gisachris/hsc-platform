from fastapi import status
from app.api.v1.exceptions import APIException


class AuthenticationException(APIException):
    def __init__(
        self,
        message: str = "Authentication failed",
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        errors: any = None,
    ):
        super().__init__(message=message, status_code=status_code, errors=errors)


class InvalidCredentials(AuthenticationException):
    def __init__(self, message: str = "Invalid email or password"):
        super().__init__(message=message, status_code=status.HTTP_401_UNAUTHORIZED)


class InvalidToken(AuthenticationException):
    def __init__(self, message: str = "Invalid access or refresh token"):
        super().__init__(message=message, status_code=status.HTTP_401_UNAUTHORIZED)


class ExpiredToken(AuthenticationException):
    def __init__(self, message: str = "Token has expired"):
        super().__init__(message=message, status_code=status.HTTP_401_UNAUTHORIZED)


class RefreshTokenRevoked(AuthenticationException):
    def __init__(self, message: str = "Refresh token has been revoked"):
        super().__init__(message=message, status_code=status.HTTP_401_UNAUTHORIZED)


class DeviceSessionExpired(AuthenticationException):
    def __init__(self, message: str = "Device session has expired"):
        super().__init__(message=message, status_code=status.HTTP_401_UNAUTHORIZED)


class AccountLocked(AuthenticationException):
    def __init__(self, message: str = "Account is temporarily locked"):
        super().__init__(message=message, status_code=status.HTTP_403_FORBIDDEN)


class AccountSuspended(AuthenticationException):
    def __init__(self, message: str = "Account has been suspended"):
        super().__init__(message=message, status_code=status.HTTP_403_FORBIDDEN)


class OrganizationNotSelected(AuthenticationException):
    def __init__(self, message: str = "Active organization context not selected"):
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST)


class PermissionDenied(AuthenticationException):
    def __init__(self, message: str = "Permission denied"):
        super().__init__(message=message, status_code=status.HTTP_403_FORBIDDEN)

