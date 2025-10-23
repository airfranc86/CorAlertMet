"""
Configuración de logging para CorAlertIntel
Sistema simple y robusto de logging siguiendo mejores prácticas
"""
import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

class LoggingConfig:
    """Configuración centralizada de logging"""

    def __init__(self):
        # Directorio de logs
        self.logs_dir = Path("logs")
        self.logs_dir.mkdir(exist_ok=True)

        # Configuración de archivos de log
        self.log_files = {
            'app': self.logs_dir / 'coralert.log',
            'auth': self.logs_dir / 'auth.log',
            'error': self.logs_dir / 'error.log'
        }

        # Configuración de rotación
        self.rotation_config = {
            'max_bytes': 5 * 1024 * 1024,  # 5MB
            'backup_count': 3
        }

        # Formato de logs
        self.log_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def setup_logger(self, name: str, level: int = logging.INFO) -> logging.Logger:
        """Configura un logger específico"""
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # Evitar duplicar handlers
        if logger.handlers:
            return logger

        # Handler para consola (solo errores en producción)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR)
        console_handler.setFormatter(self.log_format)
        # Configurar encoding para Windows
        console_handler.stream.reconfigure(encoding='utf-8')
        logger.addHandler(console_handler)

        # Handler para archivo principal
        file_handler = RotatingFileHandler(
            self.log_files['app'],
            maxBytes=self.rotation_config['max_bytes'],
            backupCount=self.rotation_config['backup_count'],
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(self.log_format)
        logger.addHandler(file_handler)

        # Handler específico para errores
        error_handler = RotatingFileHandler(
            self.log_files['error'],
            maxBytes=self.rotation_config['max_bytes'],
            backupCount=self.rotation_config['backup_count'],
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(self.log_format)
        logger.addHandler(error_handler)

        return logger

    def setup_auth_logger(self) -> logging.Logger:
        """Configura logger específico para autenticación"""
        logger = logging.getLogger('auth')
        logger.setLevel(logging.INFO)

        if logger.handlers:
            return logger

        # Handler para archivo de auth
        auth_handler = RotatingFileHandler(
            self.log_files['auth'],
            maxBytes=self.rotation_config['max_bytes'],
            backupCount=self.rotation_config['backup_count'],
            encoding='utf-8'
        )
        auth_handler.setLevel(logging.INFO)
        auth_handler.setFormatter(self.log_format)
        logger.addHandler(auth_handler)

        return logger

# Instancia global de configuración
_logging_config = LoggingConfig()

def get_logger(name: str) -> logging.Logger:
    """Obtiene un logger configurado"""
    return _logging_config.setup_logger(name)

def get_auth_logger() -> logging.Logger:
    """Obtiene el logger de autenticación"""
    return _logging_config.setup_auth_logger()

def setup_logging():
    """Configura el sistema de logging global"""
    # Configurar niveles de módulos externos
    logging.getLogger('streamlit').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)

    return _logging_config
