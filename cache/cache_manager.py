"""
Sistema de gestión de cache para CorAlertMet Intelligence
Reemplaza pickle por joblib para mayor seguridad
"""
import os
import json
import joblib
import hashlib
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional, Union
import pandas as pd
import numpy as np

# Configurar logging
logger = logging.getLogger(__name__)

class CacheManager:
    """Gestor de cache con joblib para serialización segura"""
    
    def __init__(self, cache_dir: str = "cache"):
        """
        Inicializar el gestor de cache
        
        Args:
            cache_dir: Directorio base para el cache
        """
        self.cache_dir = Path(cache_dir)
        self.models_dir = self.cache_dir / "models"
        self.data_dir = self.cache_dir / "data"
        self.config_dir = self.cache_dir / "config"
        
        # Crear directorios si no existen
        self._create_directories()
        
        # Configuración por defecto
        self.config = {
            "model_ttl_hours": 168,  # 7 días
            "data_ttl_hours": 1,     # 1 hora
            "max_cache_size_mb": 1000,
            "compression_level": 3
        }
        
        # Cargar configuración existente
        self._load_config()
    
    def _create_directories(self):
        """Crear directorios necesarios"""
        for directory in [self.models_dir, self.data_dir, self.config_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _load_config(self):
        """Cargar configuración desde archivo"""
        config_file = self.config_dir / "cache_config.json"
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    self.config.update(saved_config)
            except Exception as e:
                logger.warning(f"Error cargando configuración: {e}")
    
    def _save_config(self):
        """Guardar configuración actual"""
        config_file = self.config_dir / "cache_config.json"
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            logger.error(f"Error guardando configuración: {e}")
    
    def _generate_key(self, name: str, data_type: str = "model") -> str:
        """Generar clave única para el cache"""
        timestamp = datetime.now().isoformat()
        key_string = f"{name}_{data_type}_{timestamp}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _is_expired(self, file_path: Path, ttl_hours: int) -> bool:
        """Verificar si un archivo ha expirado"""
        if not file_path.exists():
            return True
        
        file_age = datetime.now() - datetime.fromtimestamp(file_path.stat().st_mtime)
        return file_age > timedelta(hours=ttl_hours)
    
    def save_model(self, model: Any, model_name: str, metadata: Optional[Dict] = None) -> bool:
        """
        Guardar modelo ML usando joblib
        
        Args:
            model: Modelo a guardar
            model_name: Nombre del modelo
            metadata: Metadatos adicionales
            
        Returns:
            bool: True si se guardó exitosamente
        """
        try:
            if model is None:
                logger.error("No se puede guardar un modelo None")
                return False
            
            # Generar nombre de archivo con extensión .joblib
            model_file = self.models_dir / f"{model_name}.joblib"
            meta_file = self.models_dir / f"{model_name}_meta.json"
            
            # Guardar modelo con joblib
            joblib.dump(model, model_file, compress=self.config["compression_level"])
            
            # Guardar metadatos
            if metadata is None:
                metadata = {}
            
            metadata.update({
                "model_name": model_name,
                "created_at": datetime.now().isoformat(),
                "file_size": model_file.stat().st_size,
                "compression": "joblib"
            })
            
            with open(meta_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            
            logger.info(f"Modelo {model_name} guardado exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error guardando modelo {model_name}: {e}")
            return False
    
    def load_model(self, model_name: str) -> Optional[Any]:
        """
        Cargar modelo ML usando joblib
        
        Args:
            model_name: Nombre del modelo
            
        Returns:
            Modelo cargado o None si no existe/expiró
        """
        try:
            model_file = self.models_dir / f"{model_name}.joblib"
            
            if not model_file.exists():
                logger.warning(f"Modelo {model_name} no encontrado")
                return None
            
            # Verificar expiración
            if self._is_expired(model_file, self.config["model_ttl_hours"]):
                logger.info(f"Modelo {model_name} ha expirado")
                model_file.unlink(missing_ok=True)
                return None
            
            # Cargar modelo con joblib
            model = joblib.load(model_file)
            logger.info(f"Modelo {model_name} cargado exitosamente")
            return model
            
        except Exception as e:
            logger.error(f"Error cargando modelo {model_name}: {e}")
            return None
    
    def save_data(self, data: Any, data_name: str, metadata: Optional[Dict] = None) -> bool:
        """
        Guardar datos usando joblib
        
        Args:
            data: Datos a guardar
            data_name: Nombre de los datos
            metadata: Metadatos adicionales
            
        Returns:
            bool: True si se guardó exitosamente
        """
        try:
            if data is None:
                logger.error("No se pueden guardar datos None")
                return False
            
            # Generar nombre de archivo con extensión .joblib
            data_file = self.data_dir / f"{data_name}.joblib"
            meta_file = self.data_dir / f"{data_name}_meta.json"
            
            # Guardar datos con joblib
            joblib.dump(data, data_file, compress=self.config["compression_level"])
            
            # Guardar metadatos
            if metadata is None:
                metadata = {}
            
            metadata.update({
                "data_name": data_name,
                "created_at": datetime.now().isoformat(),
                "file_size": data_file.stat().st_size,
                "compression": "joblib"
            })
            
            with open(meta_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            
            logger.info(f"Datos {data_name} guardados exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error guardando datos {data_name}: {e}")
            return False
    
    def load_data(self, data_name: str) -> Optional[Any]:
        """
        Cargar datos usando joblib
        
        Args:
            data_name: Nombre de los datos
            
        Returns:
            Datos cargados o None si no existen/expiraron
        """
        try:
            data_file = self.data_dir / f"{data_name}.joblib"
            
            if not data_file.exists():
                logger.warning(f"Datos {data_name} no encontrados")
                return None
            
            # Verificar expiración
            if self._is_expired(data_file, self.config["data_ttl_hours"]):
                logger.info(f"Datos {data_name} han expirado")
                data_file.unlink(missing_ok=True)
                return None
            
            # Cargar datos con joblib
            data = joblib.load(data_file)
            logger.info(f"Datos {data_name} cargados exitosamente")
            return data
            
        except Exception as e:
            logger.error(f"Error cargando datos {data_name}: {e}")
            return None
    
    def cleanup_expired(self) -> Dict[str, int]:
        """
        Limpiar archivos expirados
        
        Returns:
            Dict con estadísticas de limpieza
        """
        stats = {"models_removed": 0, "data_removed": 0}
        
        try:
            # Limpiar modelos expirados
            for model_file in self.models_dir.glob("*.joblib"):
                if self._is_expired(model_file, self.config["model_ttl_hours"]):
                    model_file.unlink(missing_ok=True)
                    stats["models_removed"] += 1
            
            # Limpiar datos expirados
            for data_file in self.data_dir.glob("*.joblib"):
                if self._is_expired(data_file, self.config["data_ttl_hours"]):
                    data_file.unlink(missing_ok=True)
                    stats["data_removed"] += 1
            
            logger.info(f"Limpieza completada: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"Error en limpieza: {e}")
            return stats
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Obtener estadísticas del cache
        
        Returns:
            Dict con estadísticas del cache
        """
        try:
            stats = {
                "total_models": 0,
                "total_data_files": 0,
                "total_size": 0,
                "models": [],
                "data_files": []
            }
            
            # Contar modelos
            for model_file in self.models_dir.glob("*.joblib"):
                if model_file.exists():
                    stats["total_models"] += 1
                    stats["total_size"] += model_file.stat().st_size
                    stats["models"].append({
                        "name": model_file.stem,
                        "size": model_file.stat().st_size,
                        "modified": datetime.fromtimestamp(model_file.stat().st_mtime).isoformat()
                    })
            
            # Contar datos
            for data_file in self.data_dir.glob("*.joblib"):
                if data_file.exists():
                    stats["total_data_files"] += 1
                    stats["total_size"] += data_file.stat().st_size
                    stats["data_files"].append({
                        "name": data_file.stem,
                        "size": data_file.stat().st_size,
                        "modified": datetime.fromtimestamp(data_file.stat().st_mtime).isoformat()
                    })
            
            return stats
            
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {e}")
            return {"error": str(e)}
    
    def clear_all_cache(self) -> bool:
        """
        Limpiar todo el cache
        
        Returns:
            bool: True si se limpió exitosamente
        """
        try:
            # Limpiar modelos
            for file in self.models_dir.glob("*"):
                if file.is_file():
                    file.unlink()
            
            # Limpiar datos
            for file in self.data_dir.glob("*"):
                if file.is_file():
                    file.unlink()
            
            logger.info("Cache limpiado completamente")
            return True
            
        except Exception as e:
            logger.error(f"Error limpiando cache: {e}")
            return False


# Funciones de conveniencia para uso directo
def save_model(model: Any, model_name: str, metadata: Optional[Dict] = None) -> bool:
    """Función de conveniencia para guardar modelo"""
    cache_manager = CacheManager()
    return cache_manager.save_model(model, model_name, metadata)

def load_model(model_name: str) -> Optional[Any]:
    """Función de conveniencia para cargar modelo"""
    cache_manager = CacheManager()
    return cache_manager.load_model(model_name)

def save_data(data: Any, data_name: str, metadata: Optional[Dict] = None) -> bool:
    """Función de conveniencia para guardar datos"""
    cache_manager = CacheManager()
    return cache_manager.save_data(data, data_name, metadata)

def load_data(data_name: str) -> Optional[Any]:
    """Función de conveniencia para cargar datos"""
    cache_manager = CacheManager()
    return cache_manager.load_data(data_name)

def cleanup_cache() -> Dict[str, int]:
    """Función de conveniencia para limpiar cache"""
    cache_manager = CacheManager()
    return cache_manager.cleanup_expired()

def get_cache_stats() -> Dict[str, Any]:
    """Función de conveniencia para obtener estadísticas"""
    cache_manager = CacheManager()
    return cache_manager.get_cache_stats()

def clear_all_cache() -> bool:
    """Función de conveniencia para limpiar todo el cache"""
    cache_manager = CacheManager()
    return cache_manager.clear_all_cache()
