from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime


@dataclass
class User:
    email: str
    nama_lengkap: str
    nomor_hp: str
    password_hash: Optional[str] = None
    account_type: str = "Free"  # Free, Premium
    status: str = "active"  # active, inactive
    verified: bool = False
    registered_at: Optional[str] = None
    token: Optional[str] = None

    def __post_init__(self):
        if self.registered_at is None:
            self.registered_at = datetime.now().isoformat()

    def to_dict(self):
        return asdict(self)

    def is_active(self):
        return self.status == "active"

    def is_verified(self):
        return self.verified

    def is_premium(self):
        return self.account_type == "Premium"

    @classmethod
    def from_gas_response(cls, data: dict):
        """Create User instance from GAS response"""
        return cls(
            email=data.get('email', ''),
            nama_lengkap=data.get('nama_lengkap', ''),
            nomor_hp=data.get('nomor_hp', ''),
            account_type=data.get('account_type', 'Free'),
            status=data.get('status', 'active'),
            verified=data.get('verified', 'false').lower() == 'true',
            registered_at=data.get('registered_at'),
            token=data.get('token')
        )