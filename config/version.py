"""
Configuración de versión centralizada para CorAlertIntel Intelligence
"""

__version__ = "2.3.0"
__version_info__ = (2, 3, 0)
__author__ = "Francisco Aucar"
__email__ = "franciscoaucar@ajconsultingit.com"
__description__ = "Sistema de Alertas Meteorológicas con Machine Learning"

def get_version():
    """Obtener la versión actual del sistema"""
    return __version__

def get_version_info():
    """Obtener información detallada de la versión"""
    return {
        "version": __version__,
        "version_info": __version_info__,
        "author": __author__,
        "email": __email__,
        "description": __description__
    }

def get_build_info():
    """Obtener información de build para despliegue"""
    return {
        "version": __version__,
        "build_date": "2025-01-23",
        "python_version": "3.8+",
        "streamlit_version": "1.28.0+",
        "status": "production_ready"
    }
