#!/usr/bin/env python3
"""
EVA & GUARANI - Security Module
-----------------------------
This module provides security features for the
EVA & GUARANI BIOS-Q system.

Version: 7.5
Created: 2025-03-26
"""

import os
import jwt
import bcrypt
import secrets
from typing import Dict, Optional, List
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass, field

from .logging import get_logger
from .config import config

logger = get_logger(__name__)

@dataclass
class User:
    """Represents a system user."""
    username: str
    password_hash: bytes
    roles: List[str] = field(default_factory=list)
    active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_login: Optional[datetime] = None

class SecurityManager:
    """Manages security operations including authentication and authorization."""
    
    def __init__(self):
        """Initialize security manager."""
        self.secret_key = config.get('security.secret_key', os.urandom(32).hex())
        self.token_expiry = config.get('security.token_expiry', 3600)  # 1 hour
        self.users: Dict[str, User] = {}
        self._load_default_users()
        
    def _load_default_users(self):
        """Load default users from configuration."""
        try:
            default_admin = config.get('security.default_admin', {})
            if default_admin:
                username = default_admin.get('username', 'admin')
                password = default_admin.get('password', secrets.token_urlsafe(16))
                
                if username not in self.users:
                    self.create_user(username, password, roles=['admin'])
                    logger.info(f"Created default admin user: {username}")
                    
        except Exception as e:
            logger.error(f"Error loading default users: {str(e)}")
            
    def create_user(self, username: str, password: str, roles: Optional[List[str]] = None) -> User:
        """Create a new user."""
        if username in self.users:
            raise ValueError(f"User {username} already exists")
            
        # Hash password with bcrypt
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        
        # Create user
        user = User(
            username=username,
            password_hash=password_hash,
            roles=roles or ['user']
        )
        
        self.users[username] = user
        logger.info(f"Created user: {username}")
        return user
        
    def authenticate(self, username: str, password: str) -> Optional[str]:
        """Authenticate user and return JWT token if successful."""
        user = self.users.get(username)
        
        if not user or not user.active:
            logger.warning(f"Authentication failed: User {username} not found or inactive")
            return None
            
        if not bcrypt.checkpw(password.encode(), user.password_hash):
            logger.warning(f"Authentication failed: Invalid password for user {username}")
            return None
            
        # Update last login time
        user.last_login = datetime.now(timezone.utc)
        
        # Generate JWT token
        token_data = {
            'sub': username,
            'roles': user.roles,
            'exp': datetime.now(timezone.utc) + timedelta(seconds=self.token_expiry)
        }
        
        token = jwt.encode(token_data, self.secret_key, algorithm='HS256')
        logger.info(f"User {username} authenticated successfully")
        return token
        
    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify JWT token and return payload if valid."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            username = payload.get('sub')
            
            if username not in self.users or not self.users[username].active:
                logger.warning(f"Token verification failed: User {username} not found or inactive")
                return None
                
            return payload
            
        except jwt.ExpiredSignatureError:
            logger.warning("Token verification failed: Token expired")
            return None
            
        except jwt.InvalidTokenError as e:
            logger.warning(f"Token verification failed: {str(e)}")
            return None
            
    def check_permission(self, token: str, required_roles: List[str]) -> bool:
        """Check if token has required roles."""
        payload = self.verify_token(token)
        if not payload:
            return False
            
        user_roles = set(payload.get('roles', []))
        return bool(user_roles & set(required_roles) or 'admin' in user_roles)
        
    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """Change user password."""
        user = self.users.get(username)
        
        if not user or not user.active:
            logger.warning(f"Password change failed: User {username} not found or inactive")
            return False
            
        if not bcrypt.checkpw(old_password.encode(), user.password_hash):
            logger.warning(f"Password change failed: Invalid old password for user {username}")
            return False
            
        # Update password hash
        user.password_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        logger.info(f"Password changed for user: {username}")
        return True
        
    def deactivate_user(self, username: str):
        """Deactivate a user account."""
        user = self.users.get(username)
        if user:
            user.active = False
            logger.info(f"User deactivated: {username}")
            
    def activate_user(self, username: str):
        """Activate a user account."""
        user = self.users.get(username)
        if user:
            user.active = True
            logger.info(f"User activated: {username}")

# Global security manager instance
manager = SecurityManager() 