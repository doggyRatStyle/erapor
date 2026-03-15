import json
import os
import hashlib
import secrets
from datetime import datetime, timedelta
from database import db
from config import SESSION_FILE


class AuthManager:
    def __init__(self):
        self.token_expiry_hours = 24

    def generate_token(self, email):
        """Generate secure token for session"""
        timestamp = datetime.now().isoformat()
        random_string = secrets.token_hex(16)
        token_string = f"{email}:{timestamp}:{random_string}"

        # Create hash
        token = hashlib.sha256(token_string.encode()).hexdigest()
        return token

    def verify_token(self, token):
        """Verify if token is valid"""
        session = db.load_session()
        if not session:
            return False

        if session.get('token') != token:
            return False

        # Check expiry
        login_at = datetime.fromisoformat(session.get('login_at', datetime.now().isoformat()))
        expiry = login_at + timedelta(hours=self.token_expiry_hours)

        if datetime.now() > expiry:
            db.clear_session()
            return False

        return True

    def get_current_user(self):
        """Get current logged in user data"""
        session = db.load_session()
        if not session:
            return None

        # Verify token still valid
        if not self.verify_token(session.get('token')):
            return None

        return {
            'email': session.get('email'),
            'nama_lengkap': session.get('nama_lengkap'),
            'account_type': session.get('account_type', 'Free'),
            'token': session.get('token')
        }

    def is_premium_user(self):
        """Check if current user is premium"""
        user = self.get_current_user()
        if not user:
            return False
        return user.get('account_type') == 'Premium'

    def is_free_user(self):
        """Check if current user is free tier"""
        user = self.get_current_user()
        if not user:
            return False
        return user.get('account_type') == 'Free'

    def require_auth(self, page, callback=None):
        """Decorator-like function to require authentication"""
        user = self.get_current_user()
        if not user:
            if callback:
                callback()
            else:
                page.go("/login")
            return None
        return user

    def logout(self, page):
        """Clear session and logout"""
        db.clear_session()
        page.go("/login")


# Global instance
auth_manager = AuthManager()