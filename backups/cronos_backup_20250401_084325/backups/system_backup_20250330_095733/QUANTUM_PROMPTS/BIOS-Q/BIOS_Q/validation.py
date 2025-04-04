#!/usr/bin/env python3
"""
EVA & GUARANI - Validation
-----------------------
This module provides input validation for the
EVA & GUARANI BIOS-Q system.

Version: 7.5
Created: 2025-03-26
"""

import re
from typing import Any, Dict, List, Optional, Union, Pattern, Callable, TypeVar
from datetime import datetime
from uuid import UUID

from .errors import ValidationError
from .constants import PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH, MAX_TEXT_LENGTH

# Type variable for generic item validation
T = TypeVar("T")

# Common validation patterns
EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{3,32}$")
UUID_PATTERN = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$")
LANGUAGE_CODE_PATTERN = re.compile(r"^[a-z]{2}(-[A-Z]{2})?$")


def validate_string(
    value: Any,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    pattern: Optional[Union[str, Pattern]] = None,
    field_name: str = "value",
) -> str:
    """Validate a string value."""
    if not isinstance(value, str):
        raise ValidationError(f"{field_name} must be a string")

    if min_length is not None and len(value) < min_length:
        raise ValidationError(f"{field_name} must be at least {min_length} characters long")

    if max_length is not None and len(value) > max_length:
        raise ValidationError(f"{field_name} must be at most {max_length} characters long")

    if pattern:
        if isinstance(pattern, str):
            pattern = re.compile(pattern)
        if not pattern.match(value):
            raise ValidationError(f"{field_name} has invalid format")

    return value


def validate_integer(
    value: Any,
    min_value: Optional[int] = None,
    max_value: Optional[int] = None,
    field_name: str = "value",
) -> int:
    """Validate an integer value."""
    try:
        if isinstance(value, str):
            value = int(value)
        elif not isinstance(value, int):
            raise ValueError
    except ValueError:
        raise ValidationError(f"{field_name} must be an integer")

    if min_value is not None and value < min_value:
        raise ValidationError(f"{field_name} must be at least {min_value}")

    if max_value is not None and value > max_value:
        raise ValidationError(f"{field_name} must be at most {max_value}")

    return value


def validate_float(
    value: Any,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    field_name: str = "value",
) -> float:
    """Validate a float value."""
    try:
        if isinstance(value, str):
            value = float(value)
        elif not isinstance(value, (int, float)):
            raise ValueError
        value = float(value)
    except ValueError:
        raise ValidationError(f"{field_name} must be a number")

    if min_value is not None and value < min_value:
        raise ValidationError(f"{field_name} must be at least {min_value}")

    if max_value is not None and value > max_value:
        raise ValidationError(f"{field_name} must be at most {max_value}")

    return value


def validate_boolean(value: Any, field_name: str = "value") -> bool:
    """Validate a boolean value."""
    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        value = value.lower()
        if value in ("true", "1", "yes", "on"):
            return True
        if value in ("false", "0", "no", "off"):
            return False

    raise ValidationError(f"{field_name} must be a boolean")


def validate_datetime(
    value: Any,
    min_date: Optional[datetime] = None,
    max_date: Optional[datetime] = None,
    field_name: str = "value",
) -> datetime:
    """Validate a datetime value."""
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            raise ValidationError(f"{field_name} must be a valid ISO format datetime")
    elif not isinstance(value, datetime):
        raise ValidationError(f"{field_name} must be a datetime")

    if min_date and value < min_date:
        raise ValidationError(f"{field_name} must be after {min_date}")

    if max_date and value > max_date:
        raise ValidationError(f"{field_name} must be before {max_date}")

    return value


def validate_uuid(value: Any, field_name: str = "value") -> UUID:
    """Validate a UUID value."""
    if isinstance(value, UUID):
        return value

    try:
        if isinstance(value, str) and UUID_PATTERN.match(value):
            return UUID(value)
    except ValueError:
        pass

    raise ValidationError(f"{field_name} must be a valid UUID")


def validate_email(value: Any, field_name: str = "email") -> str:
    """Validate an email address."""
    value = validate_string(value, field_name=field_name)
    if not EMAIL_PATTERN.match(value):
        raise ValidationError(f"{field_name} must be a valid email address")
    return value


def validate_username(value: Any, field_name: str = "username") -> str:
    """Validate a username."""
    value = validate_string(value, field_name=field_name)
    if not USERNAME_PATTERN.match(value):
        raise ValidationError(
            f"{field_name} must be 3-32 characters long and contain only "
            "letters, numbers, underscores, and hyphens"
        )
    return value


def validate_password(value: Any, field_name: str = "password") -> str:
    """Validate a password."""
    value = validate_string(
        value, min_length=PASSWORD_MIN_LENGTH, max_length=PASSWORD_MAX_LENGTH, field_name=field_name
    )

    # Check for minimum complexity
    if not any(c.isupper() for c in value):
        raise ValidationError(f"{field_name} must contain at least one uppercase letter")
    if not any(c.islower() for c in value):
        raise ValidationError(f"{field_name} must contain at least one lowercase letter")
    if not any(c.isdigit() for c in value):
        raise ValidationError(f"{field_name} must contain at least one number")
    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in value):
        raise ValidationError(f"{field_name} must contain at least one special character")

    return value


def validate_language_code(value: Any, field_name: str = "language") -> str:
    """Validate a language code."""
    value = validate_string(value, field_name=field_name)
    if not LANGUAGE_CODE_PATTERN.match(value):
        raise ValidationError(f"{field_name} must be a valid language code (e.g., 'en' or 'en-US')")
    return value


def validate_text(value: Any, field_name: str = "text") -> str:
    """Validate text content."""
    return validate_string(value, max_length=MAX_TEXT_LENGTH, field_name=field_name)


def validate_dict(
    value: Any,
    required_keys: Optional[List[str]] = None,
    optional_keys: Optional[List[str]] = None,
    field_name: str = "value",
) -> Dict:
    """Validate a dictionary."""
    if not isinstance(value, dict):
        raise ValidationError(f"{field_name} must be a dictionary")

    if required_keys:
        missing_keys = [key for key in required_keys if key not in value]
        if missing_keys:
            raise ValidationError(
                f"{field_name} is missing required keys: {', '.join(missing_keys)}"
            )

    if required_keys or optional_keys:
        allowed_keys = set(required_keys or []) | set(optional_keys or [])
        extra_keys = [key for key in value if key not in allowed_keys]
        if extra_keys:
            raise ValidationError(f"{field_name} contains invalid keys: {', '.join(extra_keys)}")

    return value


def validate_list(
    value: Any,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    item_validator: Optional[Callable[[Any], T]] = None,
    field_name: str = "value",
) -> List[T]:
    """Validate a list."""
    if not isinstance(value, (list, tuple)):
        raise ValidationError(f"{field_name} must be a list")

    # Convert tuple to list if necessary
    value = list(value)

    if min_length is not None and len(value) < min_length:
        raise ValidationError(f"{field_name} must contain at least {min_length} items")

    if max_length is not None and len(value) > max_length:
        raise ValidationError(f"{field_name} must contain at most {max_length} items")

    if item_validator:
        try:
            value = [item_validator(item) for item in value]
        except ValidationError as e:
            raise ValidationError(f"Invalid item in {field_name}: {str(e)}")

    return value
