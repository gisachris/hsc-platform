from typing import List
from fastapi import Depends, HTTPException, status
from app.modules.authentication.dependencies import get_token_claims, get_current_user
from app.modules.authentication.models import User


class PermissionChecker:
    def __init__(self, required_permission: str):
        self.required_permission = required_permission

    async def __call__(self, claims: dict = Depends(get_token_claims)) -> None:
        permissions: List[str] = claims.get("permissions", [])
        # Admin wildcard bypass or direct match check
        if "*" in permissions or self.required_permission in permissions:
            return
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Missing required permission scope: {self.required_permission}",
        )


class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    async def __call__(
        self,
        claims: dict = Depends(get_token_claims),
        user: User = Depends(get_current_user),
    ) -> None:
        user_role = claims.get("role")
        # Global Admin override
        if user_role == "admin" or user_role in self.allowed_roles:
            return
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation restricted to authorized roles only",
        )


# Role dependencies
RequireAuthenticated = Depends(get_current_user)
RequireAdmin = Depends(RoleChecker(["admin"]))
RequireOrganizer = Depends(RoleChecker(["admin", "organizer"]))
RequireModerator = Depends(RoleChecker(["admin", "organizer", "moderator"]))
RequireSpeaker = Depends(RoleChecker(["admin", "organizer", "speaker"]))


# Reusable generic permission checker generator function
def RequirePermission(permission_name: str):
    return Depends(PermissionChecker(permission_name))
