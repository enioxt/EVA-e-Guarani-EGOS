#!/usr/bin/env python3
"""
EVA & GUARANI - Error Handling
---------------------------
This module provides standardized error handling for the
EVA & GUARANI BIOS-Q system.

Version: 7.5
Created: 2025-03-26
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timezone
import traceback
import uuid
import json

from .logging import get_logger

logger = get_logger(__name__)


@dataclass
class ErrorContext:
    """Context information for an error."""

    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    error_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    component: str = ""
    operation: str = ""
    user_id: Optional[str] = None
    correlation_id: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


class BiosQError(Exception):
    """Base exception class for EVA & GUARANI BIOS-Q system."""

    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_ERROR",
        http_status: int = 500,
        context: Optional[ErrorContext] = None,
        cause: Optional[Exception] = None,
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.http_status = http_status
        self.context = context or ErrorContext()
        self.cause = cause

        # Log error with context
        self._log_error()

    def _log_error(self):
        """Log error with context information."""
        error_info = {
            "error_id": self.context.error_id,
            "code": self.code,
            "message": self.message,
            "component": self.context.component,
            "operation": self.context.operation,
            "timestamp": self.context.timestamp.isoformat(),
            "user_id": self.context.user_id,
            "correlation_id": self.context.correlation_id,
        }

        if self.context.additional_data:
            error_info["details"] = str(self.context.additional_data)

        if self.cause:
            error_info["cause_type"] = type(self.cause).__name__
            error_info["cause_message"] = str(self.cause)
            error_info["traceback"] = traceback.format_exc()

        logger.error(f"Error occurred: {self.code}", extra=error_info)

    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary format."""
        error_dict = {
            "error": {
                "code": self.code,
                "message": self.message,
                "error_id": self.context.error_id,
                "timestamp": self.context.timestamp.isoformat(),
            }
        }

        # Add optional context information
        if self.context.component:
            error_dict["error"]["component"] = self.context.component
        if self.context.operation:
            error_dict["error"]["operation"] = self.context.operation
        if self.context.correlation_id:
            error_dict["error"]["correlation_id"] = self.context.correlation_id
        if self.context.additional_data:
            error_dict["error"]["details"] = self.context.additional_data

        return error_dict


# Authentication Errors
class AuthenticationError(BiosQError):
    """Raised when authentication fails."""

    def __init__(
        self,
        message: str,
        context: Optional[ErrorContext] = None,
        cause: Optional[Exception] = None,
    ):
        super().__init__(
            message=message,
            code="AUTHENTICATION_ERROR",
            http_status=401,
            context=context,
            cause=cause,
        )


class AuthorizationError(BiosQError):
    """Raised when authorization fails."""

    def __init__(
        self,
        message: str,
        context: Optional[ErrorContext] = None,
        cause: Optional[Exception] = None,
    ):
        super().__init__(
            message=message,
            code="AUTHORIZATION_ERROR",
            http_status=403,
            context=context,
            cause=cause,
        )


# Validation Errors
class ValidationError(BiosQError):
    """Raised when input validation fails."""

    def __init__(
        self,
        message: str,
        context: Optional[ErrorContext] = None,
        cause: Optional[Exception] = None,
    ):
        super().__init__(
            message=message, code="VALIDATION_ERROR", http_status=400, context=context, cause=cause
        )


# Resource Errors
class ResourceNotFoundError(BiosQError):
    """Raised when a requested resource is not found."""

    def __init__(
        self,
        message: str,
        context: Optional[ErrorContext] = None,
        cause: Optional[Exception] = None,
    ):
        super().__init__(
            message=message,
            code="RESOURCE_NOT_FOUND",
            http_status=404,
            context=context,
            cause=cause,
        )


class ResourceConflictError(BiosQError):
    """Raised when there is a conflict with existing resources."""

    def __init__(
        self,
        message: str,
        context: Optional[ErrorContext] = None,
        cause: Optional[Exception] = None,
    ):
        super().__init__(
            message=message, code="RESOURCE_CONFLICT", http_status=409, context=context, cause=cause
        )


# System Errors
class ConfigurationError(BiosQError):
    """Raised when there is a configuration error."""

    def __init__(
        self,
        message: str,
        context: Optional[ErrorContext] = None,
        cause: Optional[Exception] = None,
    ):
        super().__init__(
            message=message,
            code="CONFIGURATION_ERROR",
            http_status=500,
            context=context,
            cause=cause,
        )


class DependencyError(BiosQError):
    """Raised when there is an error with a system dependency."""

    def __init__(
        self,
        message: str,
        context: Optional[ErrorContext] = None,
        cause: Optional[Exception] = None,
    ):
        super().__init__(
            message=message, code="DEPENDENCY_ERROR", http_status=503, context=context, cause=cause
        )


# Rate Limiting Errors
class RateLimitError(BiosQError):
    """Raised when rate limit is exceeded."""

    def __init__(
        self,
        message: str,
        context: Optional[ErrorContext] = None,
        cause: Optional[Exception] = None,
    ):
        super().__init__(
            message=message,
            code="RATE_LIMIT_EXCEEDED",
            http_status=429,
            context=context,
            cause=cause,
        )


def handle_error(error: Exception) -> Dict[str, Any]:
    """Convert any exception to a standardized error response."""
    if isinstance(error, BiosQError):
        return error.to_dict()

    # Convert unknown errors to BiosQError
    context = ErrorContext(
        component="system",
        operation="unknown",
        additional_data={"error_type": type(error).__name__},
    )

    bios_error = BiosQError(
        message=str(error), code="INTERNAL_ERROR", http_status=500, context=context, cause=error
    )

    return bios_error.to_dict()
