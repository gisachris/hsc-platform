import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.authentication.models import User, Organization, Role, OrganizationMembership
from app.modules.authentication.service import AuthenticationService
from app.modules.authentication.repository import AuthenticationRepository


@pytest.fixture
def auth_repository(db: AsyncSession) -> AuthenticationRepository:
    return AuthenticationRepository(db)


@pytest.fixture
def auth_service(auth_repository: AuthenticationRepository) -> AuthenticationService:
    return AuthenticationService(auth_repository)


@pytest_asyncio.fixture
async def test_role(db: AsyncSession) -> Role:
    role = Role(
        name="test_organizer",
        description="Test Organizer Role",
        permissions=["event:create", "event:publish"]
    )
    db.add(role)
    await db.commit()
    await db.refresh(role)
    return role


@pytest_asyncio.fixture
async def test_org(db: AsyncSession) -> Organization:
    org = Organization(
        name="Test Org",
        slug="test-org"
    )
    db.add(org)
    await db.commit()
    await db.refresh(org)
    return org


@pytest_asyncio.fixture
async def test_user(db: AsyncSession) -> User:
    user = User(
        email="test_auth@example.com",
        password_hash=AuthenticationService.hash_password("ComplexP@ss123!"),
        first_name="Test",
        last_name="User",
        status="active",
        email_verified=True
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@pytest_asyncio.fixture
async def test_membership(
    db: AsyncSession, test_user: User, test_org: Organization, test_role: Role
) -> OrganizationMembership:
    membership = OrganizationMembership(
        user_id=test_user.id,
        organization_id=test_org.id,
        role_id=test_role.id
    )
    db.add(membership)
    await db.commit()
    await db.refresh(membership)
    return membership
