import secrets
import uuid
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.modules.authentication.exceptions import (
    AccountSuspended,
    DeviceSessionExpired,
    ExpiredToken,
    InvalidCredentials,
    InvalidToken,
    OrganizationNotSelected,
    PermissionDenied,
    RefreshTokenRevoked,
)
from app.modules.authentication.models import User, DeviceSession
from app.modules.authentication.repository import AuthenticationRepository
from app.modules.authentication.schemas import (
    UserRegister,
    UserLogin,
    TokenResponse,
)
from app.modules.authentication.events import (
    dispatcher,
    UserRegistered,
    UserLoggedIn,
    UserLoggedOut,
    PasswordChanged,
    OrganizationChanged,
    DeviceSessionCreated,
    DeviceSessionRevoked,
)

# Initialize Passlib with Argon2 hasher
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class AuthenticationService:
    def __init__(self, repository: AuthenticationRepository):
        self.repository = repository

    # Password Crypt Helpers
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception:
            return False

    @staticmethod
    def hash_token(token: str) -> str:
        """Securely hash a token using SHA-256 for database storage."""
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    # JWT Generation
    def generate_access_token(
        self,
        user_id: uuid.UUID,
        organization_id: Optional[uuid.UUID] = None,
        role: Optional[str] = None,
        permissions: Optional[List[str]] = None,
    ) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        claims = {
            "sub": str(user_id),
            "org_id": str(organization_id) if organization_id else None,
            "role": role,
            "permissions": permissions or [],
            "exp": expire,
            "iat": datetime.now(timezone.utc),
            "jti": str(uuid.uuid4()),
        }
        return jwt.encode(claims, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    def generate_refresh_token(self) -> str:
        """Generates a cryptographically secure random token string."""
        return secrets.token_hex(32)

    # Core Flows
    async def register_user(self, schema: UserRegister) -> User:
        # 1. Verify email uniqueness
        existing_user = await self.repository.get_user_by_email(schema.email)
        if existing_user:
            raise InvalidCredentials("Email address is already registered")

        # 2. Hash and create user entity
        user = User(
            email=schema.email,
            password_hash=self.hash_password(schema.password),
            first_name=schema.first_name,
            last_name=schema.last_name,
            status="active",
            email_verified=False,
        )

        # 3. Persist user
        created_user = await self.repository.create_user(user)

        # 4. Dispatch domain event
        dispatcher.dispatch(
            UserRegistered(user_id=str(created_user.id), email=created_user.email)
        )

        return created_user

    async def login_user(
        self, schema: UserLogin, ip_address: Optional[str], user_agent: Optional[str]
    ) -> TokenResponse:
        # 1. Fetch and validate user
        user = await self.repository.get_user_by_email(schema.email)
        if not user or not self.verify_password(schema.password, user.password_hash):
            raise InvalidCredentials()

        if user.status == "suspended":
            raise AccountSuspended()

        # 2. Setup Device Session
        refresh_token = self.generate_refresh_token()
        refresh_token_hash = self.hash_token(refresh_token)

        device_session = DeviceSession(
            user_id=user.id,
            refresh_token_hash=refresh_token_hash,
            device_name=schema.device_name,
            device_type=schema.device_type,
            ip_address=ip_address,
            user_agent=user_agent,
            is_active=True,
            expires_at=datetime.now(timezone.utc) + timedelta(days=30),
        )

        session = await self.repository.create_device_session(device_session)

        # 3. Resolve base context membership
        org_id, role, permissions = None, None, []
        memberships = await self.repository.get_user_memberships(user.id)
        if memberships:
            # Pick first joined membership as default organization context
            default_mem = memberships[0]
            org_id = default_mem.organization_id
            role = default_mem.role.name
            permissions = default_mem.role.permissions

        # 4. Generate Access Token
        access_token = self.generate_access_token(
            user_id=user.id, organization_id=org_id, role=role, permissions=permissions
        )

        # 5. Update user state
        user.last_login = datetime.now(timezone.utc)
        await self.repository.update_user(user)

        # 6. Dispatch events
        dispatcher.dispatch(
            DeviceSessionCreated(user_id=str(user.id), session_id=str(session.id))
        )
        dispatcher.dispatch(
            UserLoggedIn(
                user_id=str(user.id),
                session_id=str(session.id),
                ip_address=ip_address or "unknown",
            )
        )

        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    async def logout_user(self, token: str) -> None:
        # Invalidate current device session using refresh token or current session context
        token_hash = self.hash_token(token)
        session = await self.repository.get_device_session_by_token_hash(token_hash)
        if session:
            session.is_active = False
            await self.repository.db.commit()
            dispatcher.dispatch(
                DeviceSessionRevoked(user_id=str(session.user_id), session_id=str(session.id))
            )
            dispatcher.dispatch(
                UserLoggedOut(user_id=str(session.user_id), session_id=str(session.id))
            )

    async def refresh_tokens(self, refresh_token: str) -> TokenResponse:
        token_hash = self.hash_token(refresh_token)
        session = await self.repository.get_device_session_by_token_hash(token_hash)

        if not session or not session.is_active:
            raise RefreshTokenRevoked()

        if session.expires_at < datetime.now(timezone.utc):
            session.is_active = False
            await self.repository.db.commit()
            raise DeviceSessionExpired()

        # Generate rotated refresh token
        new_refresh_token = self.generate_refresh_token()
        session.refresh_token_hash = self.hash_token(new_refresh_token)
        session.last_activity = datetime.now(timezone.utc)
        await self.repository.db.commit()

        # Resolve context
        org_id, role, permissions = None, None, []
        memberships = await self.repository.get_user_memberships(session.user_id)
        if memberships:
            default_mem = memberships[0]
            org_id = default_mem.organization_id
            role = default_mem.role.name
            permissions = default_mem.role.permissions

        access_token = self.generate_access_token(
            user_id=session.user_id, organization_id=org_id, role=role, permissions=permissions
        )

        return TokenResponse(access_token=access_token, refresh_token=new_refresh_token)

    async def select_organization(
        self, user_id: uuid.UUID, organization_id: uuid.UUID
    ) -> str:
        membership = await self.repository.get_membership_for_user_and_org(
            user_id, organization_id
        )
        if not membership:
            raise PermissionDenied("You are not a member of this organization")

        # Resolve new permissions profile
        role = membership.role.name
        permissions = membership.role.permissions

        # Dispatch organization changed event
        dispatcher.dispatch(
            OrganizationChanged(
                user_id=str(user_id),
                organization_id=str(organization_id),
                role=role,
            )
        )

        # Issue new Access token containing selected org claims
        return self.generate_access_token(
            user_id=user_id,
            organization_id=organization_id,
            role=role,
            permissions=permissions,
        )

    async def change_password(self, user_id: uuid.UUID, schema: Any) -> None:
        user = await self.repository.get_user_by_id(user_id)
        if not user or not self.verify_password(schema.current_password, user.password_hash):
            raise InvalidCredentials()

        user.password_hash = self.hash_password(schema.new_password)
        await self.repository.update_user(user)

        # Revoke all other device sessions
        await self.repository.revoke_all_device_sessions_for_user(user_id)
        dispatcher.dispatch(PasswordChanged(user_id=str(user_id)))

