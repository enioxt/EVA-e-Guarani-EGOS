#!/usr/bin/env python3
"""
EVA & GUARANI - Middleware
-----------------------
This module provides middleware components for the
EVA & GUARANI BIOS-Q system.

Version: 7.5
Created: 2025-03-26
"""

import time
from typing import Callable, Dict, Optional, Any
from functools import wraps
from datetime import datetime, timezone
import uuid
import asyncio

from aiohttp import web
from aiohttp.web import Request, Response, middleware

from .logging import get_logger
from .errors import AuthenticationError, AuthorizationError, RateLimitError, handle_error
from .security import manager as security_manager
from .metrics import collector as metrics_collector
from .utils import RateLimiter
from .constants import ContentType

logger = get_logger(__name__)

# Rate limiter instance
rate_limiter = RateLimiter()


@middleware
async def error_middleware(request: Request, handler: Callable) -> Response:
    """Handle exceptions and convert them to appropriate responses."""
    try:
        return await handler(request)
    except Exception as e:
        error_dict = handle_error(e)
        status = getattr(e, "http_status", 500)

        return web.json_response(error_dict, status=status, content_type=ContentType.JSON)


@middleware
async def logging_middleware(request: Request, handler: Callable) -> Response:
    """Log request and response details."""
    start_time = time.time()
    request_id = str(uuid.uuid4())

    # Extract request details
    request_info = {
        "request_id": request_id,
        "method": request.method,
        "path": request.path,
        "query": dict(request.query),
        "remote": request.remote,
        "user_agent": request.headers.get("User-Agent", "Unknown"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    # Log request
    logger.info(f"Request received: {request.method} {request.path}", extra=request_info)

    try:
        response = await handler(request)

        # Calculate duration
        duration = time.time() - start_time

        # Log response
        logger.info(
            f"Response sent: {response.status}",
            extra={**request_info, "status": response.status, "duration": duration},
        )

        # Add response headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Time"] = f"{duration:.3f}s"

        return response

    except Exception as e:
        # Log error
        logger.error(
            f"Request failed: {str(e)}",
            extra={**request_info, "error": str(e), "duration": time.time() - start_time},
        )
        raise


@middleware
async def metrics_middleware(request: Request, handler: Callable) -> Response:
    """Collect request metrics."""
    start_time = time.time()

    try:
        response = await handler(request)

        # Record metrics
        duration = time.time() - start_time
        metrics_collector.add_metric(
            "http_request_duration_seconds",
            duration,
            {"method": request.method, "path": request.path, "status": response.status},
        )
        metrics_collector.add_metric(
            "http_requests_total",
            1,
            {"method": request.method, "path": request.path, "status": response.status},
        )

        return response

    except Exception:
        # Record failure metrics
        metrics_collector.add_metric(
            "http_request_failures_total", 1, {"method": request.method, "path": request.path}
        )
        raise


@middleware
async def auth_middleware(request: Request, handler: Callable) -> Response:
    """Authenticate and authorize requests."""
    # Skip authentication for public endpoints
    if request.path.startswith(("/static/", "/docs/", "/api/v1/auth/")):
        return await handler(request)

    # Get token from header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise AuthenticationError("Missing or invalid authorization header")

    token = auth_header.split(" ")[1]

    # Verify token
    payload = security_manager.verify_token(token)
    if not payload:
        raise AuthenticationError("Invalid or expired token")

    # Add user info to request
    request["user"] = payload

    # Check required roles if specified
    required_roles = getattr(handler, "_required_roles", None)
    if required_roles and not security_manager.check_permission(token, required_roles):
        raise AuthorizationError("Insufficient permissions")

    return await handler(request)


@middleware
async def rate_limit_middleware(request: Request, handler: Callable) -> Response:
    """Apply rate limiting to requests."""
    # Skip rate limiting for static files
    if request.path.startswith("/static/"):
        return await handler(request)

    # Get client identifier (IP address or user ID)
    client_id = request.get("user", {}).get("sub") or request.remote

    # Check rate limit
    if not rate_limiter.check_rate_limit(client_id):
        raise RateLimitError("Rate limit exceeded")

    return await handler(request)


@middleware
async def cors_middleware(request: Request, handler: Callable) -> Response:
    """Handle CORS headers."""
    if request.method == "OPTIONS":
        response = Response(status=204)
    else:
        response = await handler(request)

    # Add CORS headers
    response.headers.update(
        {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Max-Age": "3600",
        }
    )

    return response


def requires_roles(*roles: str) -> Callable:
    """Decorator to specify required roles for a handler."""

    def decorator(handler: Callable) -> Callable:
        handler._required_roles = roles
        return handler

    return decorator


# Middleware configuration
def setup_middleware(app: web.Application):
    """Configure middleware for the application."""
    app.middlewares.extend(
        [
            error_middleware,
            logging_middleware,
            metrics_middleware,
            auth_middleware,
            rate_limit_middleware,
            cors_middleware,
        ]
    )
