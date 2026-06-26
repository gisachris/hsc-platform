import uuid
from typing import List, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.modules.authentication.exceptions import InvalidToken, ExpiredToken
from app.modules.authentication.models import User
from app.modules.authentication.repository import AuthenticationRepository

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)


async def get_auth_repository(db: AsyncSession = Depends(get_db)) -> AuthenticationRepository:
    return AuthenticationRepository(db)


async def get_token_claims(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        raise InvalidToken("Could not validate authorization credentials")


async def get_current_user(
    claims: dict = Depends(get_token_claims),
    repo: AuthenticationRepository = Depends(get_auth_repository),
) -> User:
    user_id = claims.get("sub")
    if not user_id:
        raise InvalidToken("Subject claim missing in token")

    user = await repo.get_user_by_id(uuid.UUID(user_id))
    if not user:
        raise InvalidToken("User profile matching token not found")

    if user.status == "suspended":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account has been suspended",
        )

    return user


async def get_current_organization_id(claims: dict = Depends(get_token_claims)) -> Optional[uuid.UUID]:
    org_id = claims.get("org_id")
    return uuid.UUID(org_id) if org_id else None


async def get_current_permissions(claims: dict = Depends(get_token_claims)) -> List[str]:
    permissions = claims.get("permissions", [])
    return permissions
