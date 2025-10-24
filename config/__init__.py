"""
Paquete de configuración para CorAlertIntel
Configuraciones centralizadas del sistema
"""

# Funciones dummy para evitar errores de importación
def get_logger():
    return None

def get_auth_logger():
    return None

def setup_logging():
    pass

__all__ = [
    'get_logger',
    'get_auth_logger',
    'setup_logging'
]
