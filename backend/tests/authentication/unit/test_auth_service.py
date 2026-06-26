import pytest
from app.modules.authentication.service import AuthenticationService
from app.modules.authentication.schemas import UserRegister, UserLogin
from app.modules.authentication.exceptions import InvalidCredentials


def test_password_hashing():
    password = "MyComplexPassword123!"
    hashed = AuthenticationService.hash_password(password)
    assert hashed != password
    assert AuthenticationService.verify_password(password, hashed) is True
    assert AuthenticationService.verify_password("wrong_password", hashed) is False


@pytest.mark.asyncio
async def test_register_user_success(auth_service: AuthenticationService):
    schema = UserRegister(
        email="new_unit_test@example.com",
        password="ComplexPassword123!",
        first_name="New",
        last_name="User"
    )
    user = await auth_service.register_user(schema)
    assert user.email == "new_unit_test@example.com"
    assert user.first_name == "New"
    assert user.status == "active"


@pytest.mark.asyncio
async def test_login_user_invalid_credentials(auth_service: AuthenticationService):
    schema = UserLogin(
        email="nonexistent@example.com",
        password="SomePassword123!"
    )
    with pytest.raises(InvalidCredentials):
        await auth_service.login_user(schema, ip_address="127.0.0.1", user_agent="pytest")
