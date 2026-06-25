import re
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class EmailValidator(BaseModel):
    email: str = Field(..., description="Target email address to validate")

    @field_validator("email")
    @classmethod
    def check_email_format(cls, value: str) -> str:
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, value):
            raise ValueError("Invalid email address format")
        return value.lower().strip()


class PasswordValidator(BaseModel):
    password: str = Field(..., description="Target password to validate strength")

    @field_validator("password")
    @classmethod
    def check_password_complexity(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one numerical digit")
        if not any(char in "!@#$%^&*()_+-=[]{}|;':\",./<>?" for char in value):
            raise ValueError("Password must contain at least one special character")
        return value
