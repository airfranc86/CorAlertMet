"""
Paquete de autenticación para CorAlertIntel
Sistema simple de autenticación con admin e invitado
"""

from .simple_auth import SimpleAuth, show_login_form, show_logout_section, require_auth, auth_system

__all__ = [
    'SimpleAuth',
    'show_login_form',
    'show_logout_section',
    'require_auth',
    'auth_system'
]
