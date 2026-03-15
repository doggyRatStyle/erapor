import requests
import json
from config import GAS_URL


class GASService:
    def __init__(self):
        self.base_url = GAS_URL

    def register(self, nama_lengkap, nomor_hp, email, password):
        """Register user via GAS"""
        try:
            payload = {
                'action': 'register',
                'nama_lengkap': nama_lengkap,
                'nomor_hp': nomor_hp,
                'email': email,
                'password': password,
                'account_type': 'Free',
                'status': 'active',
                'verified': 'false',
                'registered_at': ''
            }

            response = requests.post(self.base_url, json=payload, timeout=30)
            result = response.json()

            if result.get('success'):
                return {'success': True, 'message': 'Registrasi berhasil. Silakan verifikasi OTP.'}
            else:
                return {'success': False, 'message': result.get('message', 'Registrasi gagal')}

        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}

    def verify_otp(self, email, otp):
        """Verify OTP via GAS"""
        try:
            payload = {
                'action': 'verify_otp',
                'email': email,
                'otp': otp
            }

            response = requests.post(self.base_url, json=payload, timeout=30)
            result = response.json()

            return result

        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}

    def login(self, email, password):
        """Login via GAS"""
        try:
            payload = {
                'action': 'login',
                'email': email,
                'password': password
            }

            response = requests.post(self.base_url, json=payload, timeout=30)
            result = response.json()

            if result.get('success'):
                return {
                    'success': True,
                    'token': result.get('token'),
                    'user': result.get('user')
                }
            else:
                return {'success': False, 'message': result.get('message', 'Login gagal')}

        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}

    def resend_otp(self, email):
        """Resend OTP"""
        try:
            payload = {
                'action': 'resend_otp',
                'email': email
            }

            response = requests.post(self.base_url, json=payload, timeout=30)
            return response.json()

        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}


gas_service = GASService()