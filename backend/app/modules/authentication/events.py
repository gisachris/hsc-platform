import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Type

logger = logging.getLogger("auth.events")


@dataclass(kw_only=True)
class DomainEvent:
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


@dataclass(kw_only=True)
class UserRegistered(DomainEvent):
    user_id: str
    email: str


@dataclass(kw_only=True)
class UserLoggedIn(DomainEvent):
    user_id: str
    session_id: str
    ip_address: str


@dataclass(kw_only=True)
class UserLoggedOut(DomainEvent):
    user_id: str
    session_id: str


@dataclass(kw_only=True)
class PasswordChanged(DomainEvent):
    user_id: str


@dataclass(kw_only=True)
class OrganizationChanged(DomainEvent):
    user_id: str
    organization_id: str
    role: str


@dataclass(kw_only=True)
class DeviceSessionCreated(DomainEvent):
    user_id: str
    session_id: str


@dataclass(kw_only=True)
class DeviceSessionRevoked(DomainEvent):
    user_id: str
    session_id: str


class EventDispatcher:
    _listeners: Dict[Type[DomainEvent], List[Callable[[Any], None]]] = {}

    @classmethod
    def register(
        cls, event_type: Type[DomainEvent], listener: Callable[[Any], None]
    ):
        if event_type not in cls._listeners:
            cls._listeners[event_type] = []
        cls._listeners[event_type].append(listener)

    @classmethod
    def dispatch(cls, event: DomainEvent):
        event_type = type(event)
        logger.info(f"Dispatching domain event: {event_type.__name__}")
        if event_type in cls._listeners:
            for listener in cls._listeners[event_type]:
                try:
                    listener(event)
                except Exception as e:
                    logger.error(
                        f"Error executing listener {listener.__name__} for event {event_type.__name__}: {e}"
                    )


# Default global dispatcher instance
dispatcher = EventDispatcher()
