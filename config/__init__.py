"""
Paquete de configuración para CorAlertIntel
Configuraciones centralizadas del sistema
"""

from .logging_config import get_logger, get_auth_logger, setup_logging

__all__ = [
    'get_logger',
    'get_auth_logger',
    'setup_logging'
]
