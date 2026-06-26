import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.authentication.models import User, DeviceSession, OrganizationMembership, Role


class AuthenticationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_user_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.email == email.lower().strip()))
        return result.scalar_one_or_none()

    async def update_user(self, user: User) -> User:
        await self.db.commit()
        await self.db.refresh(user)
        return user

    # Device Sessions
    async def create_device_session(self, session: DeviceSession) -> DeviceSession:
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        return session

    async def get_device_session_by_id(self, session_id: uuid.UUID) -> Optional[DeviceSession]:
        result = await self.db.execute(select(DeviceSession).where(DeviceSession.id == session_id))
        return result.scalar_one_or_none()

    async def get_device_session_by_token_hash(self, token_hash: str) -> Optional[DeviceSession]:
        result = await self.db.execute(
            select(DeviceSession).where(
                DeviceSession.refresh_token_hash == token_hash,
                DeviceSession.is_active == True
            )
        )
        return result.scalar_one_or_none()

    async def get_active_device_sessions_for_user(self, user_id: uuid.UUID) -> List[DeviceSession]:
        result = await self.db.execute(
            select(DeviceSession).where(
                DeviceSession.user_id == user_id,
                DeviceSession.is_active == True
            )
        )
        return list(result.scalars().all())

    async def revoke_device_session(self, session_id: uuid.UUID) -> bool:
        session = await self.get_device_session_by_id(session_id)
        if session:
            session.is_active = False
            await self.db.commit()
            return True
        return False

    async def revoke_all_other_device_sessions_for_user(self, user_id: uuid.UUID, active_session_id: uuid.UUID) -> None:
        await self.db.execute(
            update(DeviceSession)
            .where(
                DeviceSession.user_id == user_id,
                DeviceSession.id != active_session_id
            )
            .values(is_active=False)
        )
        await self.db.commit()

    async def revoke_all_device_sessions_for_user(self, user_id: uuid.UUID) -> None:
        await self.db.execute(
            update(DeviceSession)
            .where(DeviceSession.user_id == user_id)
            .values(is_active=False)
        )
        await self.db.commit()

    # Memberships and Roles
    async def get_user_memberships(self, user_id: uuid.UUID) -> List[OrganizationMembership]:
        result = await self.db.execute(
            select(OrganizationMembership)
            .where(OrganizationMembership.user_id == user_id)
        )
        return list(result.scalars().all())

    async def get_membership_for_user_and_org(
        self, user_id: uuid.UUID, organization_id: uuid.UUID
    ) -> Optional[OrganizationMembership]:
        result = await self.db.execute(
            select(OrganizationMembership)
            .where(
                OrganizationMembership.user_id == user_id,
                OrganizationMembership.organization_id == organization_id
            )
        )
        return result.scalar_one_or_none()
