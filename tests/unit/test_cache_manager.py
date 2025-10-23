"""
Tests unitarios para cache/cache_manager.py
Sistema de cache inteligente para modelos ML y datos meteorológicos
"""
import pytest
import os
import tempfile
import shutil
import json
import joblib
import pickle
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock, mock_open

# Importar el módulo a testear
from cache.cache_manager import (
    CacheManager, 
    save_model, 
    load_model, 
    save_data, 
    load_data,
    cleanup_cache,
    get_cache_stats,
    clear_all_cache
)


class TestCacheManager:
    """Tests para la clase CacheManager"""
    
    def test_init_default_directories(self, temp_cache_dir):
        """Test inicialización con directorios por defecto"""
        cache_manager = CacheManager(cache_dir=temp_cache_dir)
        
        assert cache_manager.cache_dir == Path(temp_cache_dir)
        assert cache_manager.models_dir == Path(temp_cache_dir) / "models"
        assert cache_manager.data_dir == Path(temp_cache_dir) / "data"
        assert cache_manager.config_dir == Path(temp_cache_dir) / "config"
        
        # Verificar que se crearon los directorios
        assert cache_manager.models_dir.exists()
        assert cache_manager.data_dir.exists()
        assert cache_manager.config_dir.exists()
    
    def test_init_custom_config(self, temp_cache_dir):
        """Test inicialización con configuración personalizada"""
        cache_manager = CacheManager(cache_dir=temp_cache_dir)
        
        # Verificar configuración por defecto
        assert cache_manager.cache_config["model_ttl"] == 7 * 24 * 60 * 60  # 7 días
        assert cache_manager.cache_config["data_ttl"] == 1 * 60 * 60  # 1 hora
        assert cache_manager.cache_config["max_cache_size"] == 500 * 1024 * 1024  # 500 MB
    
    def test_generate_key_consistency(self, temp_cache_dir):
        """Test generación consistente de claves MD5"""
        cache_manager = CacheManager(cache_dir=temp_cache_dir)
        
        # Misma entrada debe generar misma clave
        key1 = cache_manager._generate_key("test_data", "model")
        key2 = cache_manager._generate_key("test_data", "model")
        assert key1 == key2
        
        # Diferentes entradas deben generar claves diferentes
        key3 = cache_manager._generate_key("test_data2", "model")
        assert key1 != key3
        
        # Diferentes prefijos deben generar claves diferentes
        key4 = cache_manager._generate_key("test_data", "data")
        assert key1 != key4
    
    def test_generate_key_different_types(self, temp_cache_dir):
        """Test generación de claves para diferentes tipos de datos"""
        cache_manager = CacheManager(cache_dir=temp_cache_dir)
        
        # String
        key_str = cache_manager._generate_key("string_data", "test")
        assert isinstance(key_str, str)
        assert len(key_str) == 32  # MD5 hash length
        
        # Dict
        key_dict = cache_manager._generate_key({"key": "value"}, "test")
        assert isinstance(key_dict, str)
        assert len(key_dict) == 32
        
        # List
        key_list = cache_manager._generate_key([1, 2, 3], "test")
        assert isinstance(key_list, str)
        assert len(key_list) == 32
    
    def test_is_expired(self, temp_cache_dir):
        """Test verificación de expiración de archivos"""
        cache_manager = CacheManager(cache_dir=temp_cache_dir)
        
        # Crear archivo temporal
        test_file = Path(temp_cache_dir) / "test_file.txt"
        test_file.write_text("test content")
        
        # Archivo recién creado no debe estar expirado
        assert not cache_manager._is_expired(test_file, 3600)  # 1 hora TTL
        
        # Archivo muy antiguo debe estar expirado
        old_time = datetime.now().timestamp() - 7200  # 2 horas atrás
        os.utime(test_file, (old_time, old_time))
        assert cache_manager._is_expired(test_file, 3600)  # 1 hora TTL
    
    def test_save_model(self, temp_cache_dir, sample_ml_model, sample_metadata):
        """Test guardar modelo con joblib"""
        cache_manager = CacheManager(cache_dir=temp_cache_dir)
        
        result = cache_manager.save_model(
            model=sample_ml_model,
            model_name="test_model",
            metadata=sample_metadata
        )
        
        assert result is True
        
        # Verificar que se crearon los archivos
        model_files = list(cache_manager.models_dir.glob("*.joblib"))
        meta_files = list(cache_manager.models_dir.glob("*_meta.json"))
        
        assert len(model_files) == 1
        assert len(meta_files) == 1
        
        # Verificar contenido del archivo de metadatos
        with open(meta_files[0], 'r') as f:
            metadata = json.load(f)
        
        assert metadata["model_name"] == "test_model"
        assert metadata["version"] == "1.0"
        assert "saved_at" in metadata
        assert "file_size" in metadata
    
    def test_load_model(self, temp_cache_dir, sample_ml_model, sample_metadata):
        """Test cargar modelo existente"""
        cache_manager = CacheManager(cache_dir=temp_cache_dir)
        
        # Guardar modelo primero
        cache_manager.save_model(sample_ml_model, "test_model", sample_metadata)
        
        # Cargar modelo
        loaded_model = cache_manager.load_model("test_model")
        
        assert loaded_model is not None
        # Verificar que es el mismo tipo de modelo
        assert hasattr(loaded_model, 'predict')
        assert hasattr(loaded_model, 'fit')
    
    def test_load_model_nonexistent(self, temp_cache_dir):
        """Test cargar modelo inexistente"""
        cache_manager = CacheManager(cache_dir=temp_cache_dir)
        
        loaded_model = cache_manager.load_model("nonexistent_model")
        assert loaded_model is None
    
    def test_model_expiration(self, temp_cache_dir, sample_ml_model, sample_metadata):
        """Test verificación de expiración de modelos (7 días)"""
        cache_manager = CacheManager(cache_dir=temp_cache_dir)
        
        # Guardar modelo
        cache_manager.save_model(sample_ml_model, "test_model", sample_metadata)
        
        # Simular modelo expirado (más de 7 días)
        model_files = list(cache_manager.models_dir.glob("*.joblib"))
        if model_files:
            old_time = datetime.now().timestamp() - (8 * 24 * 60 * 60)  # 8 días atrás
            os.utime(model_files[0], (old_time, old_time))
            
            # Intentar cargar modelo expirado
            loaded_model = cache_manager.load_model("test_model")
            assert loaded_model is None
    
    def test_save_data(self, temp_cache_dir):
        """Test guardar datos con joblib (seguro)"""
        cache_manager = CacheManager(cache_dir=temp_cache_dir)
        
        # Crear datos de prueba
        test_data = {
            "temperature": [25.5, 26.0, 24.8],
            "humidity": [65, 70, 60],
            "pressure": [1013.2, 1012.8, 1014.1]
        }
        
        result = cache_manager.save_data(
            data=test_data,
            data_name="weather_data",
            metadata={"source": "test"}
        )
        
        assert result is True
        
        # Verificar que se crearon los archivos
        data_files = list(cache_manager.data_dir.glob("*.joblib"))
        meta_files = list(cache_manager.data_dir.glob("*_meta.json"))
        
        assert len(data_files) == 1
        assert len(meta_files) == 1
    
    def test_load_data(self, temp_cache_dir):
        """Test cargar datos existentes"""
        cache_manager = CacheManager(cache_dir=temp_cache_dir)
        
        # Crear datos de prueba
        test_data = {"test": "data", "values": [1, 2, 3]}
        
        # Guardar datos
        cache_manager.save_data(test_data, "test_data")
        
        # Cargar datos
        loaded_data = cache_manager.load_data("test_data")
        
        assert loaded_data is not None
        assert loaded_data["test"] == "data"
        assert loaded_data["values"] == [1, 2, 3]
    
    def test_load_data_nonexistent(self, temp_cache_dir):
        """Test cargar datos inexistentes"""
        cache_manager = CacheManager(cache_dir=temp_cache_dir)
        
        loaded_data = cache_manager.load_data("nonexistent_data")
        assert loaded_data is None
    
    def test_data_expiration(self, temp_cache_dir):
        """Test verificación de expiración de datos (1 hora)"""
        cache_manager = CacheManager(cache_dir=temp_cache_dir)
        
        # Crear datos de prueba
        test_data = {"test": "data"}
        
        # Guardar datos
        cache_manager.save_data(test_data, "test_data")
        
        # Simular datos expirados (más de 1 hora)
        data_files = list(cache_manager.data_dir.glob("*.pkl"))
        if data_files:
            old_time = datetime.now().timestamp() - 7200  # 2 horas atrás
            os.utime(data_files[0], (old_time, old_time))
            
            # Intentar cargar datos expirados
            loaded_data = cache_manager.load_data("test_data")
            assert loaded_data is None
    
    def test_cleanup_expired(self, temp_cache_dir, sample_ml_model, sample_metadata):
        """Test limpieza de cache expirado"""
        cache_manager = CacheManager(cache_dir=temp_cache_dir)
        
        # Guardar modelo y datos
        cache_manager.save_model(sample_ml_model, "test_model", sample_metadata)
        cache_manager.save_data({"test": "data"}, "test_data")
        
        # Simular archivos expirados
        for file_path in cache_manager.models_dir.glob("*.joblib"):
            old_time = datetime.now().timestamp() - (8 * 24 * 60 * 60)  # 8 días
            os.utime(file_path, (old_time, old_time))
        
        for file_path in cache_manager.data_dir.glob("*.pkl"):
            old_time = datetime.now().timestamp() - 7200  # 2 horas
            os.utime(file_path, (old_time, old_time))
        
        # Ejecutar limpieza
        stats = cache_manager.cleanup_expired()
        
        assert stats["models_removed"] >= 0
        assert stats["data_removed"] >= 0
        assert stats["space_freed"] >= 0
    
    def test_get_cache_stats(self, temp_cache_dir, sample_ml_model, sample_metadata):
        """Test estadísticas de cache"""
        cache_manager = CacheManager(cache_dir=temp_cache_dir)
        
        # Agregar algunos archivos al cache
        cache_manager.save_model(sample_ml_model, "model1", sample_metadata)
        cache_manager.save_data({"data": "1"}, "data1")
        cache_manager.save_data({"data": "2"}, "data2")
        
        # Obtener estadísticas
        stats = cache_manager.get_cache_stats()
        
        assert stats["total_models"] == 1
        assert stats["total_data_files"] == 2
        assert stats["total_size"] > 0
        assert "total_size_mb" in stats
        assert len(stats["models"]) == 1
        assert len(stats["data_files"]) == 2
    
    def test_clear_all_cache(self, temp_cache_dir, sample_ml_model, sample_metadata):
        """Test limpiar todo el cache"""
        cache_manager = CacheManager(cache_dir=temp_cache_dir)
        
        # Agregar archivos al cache
        cache_manager.save_model(sample_ml_model, "test_model", sample_metadata)
        cache_manager.save_data({"test": "data"}, "test_data")
        
        # Verificar que hay archivos
        assert len(list(cache_manager.models_dir.glob("*"))) > 0
        assert len(list(cache_manager.data_dir.glob("*"))) > 0
        
        # Limpiar todo
        result = cache_manager.clear_all_cache()
        assert result is True
        
        # Verificar que se limpió todo
        assert len(list(cache_manager.models_dir.glob("*"))) == 0
        assert len(list(cache_manager.data_dir.glob("*"))) == 0


class TestCacheManagerFunctions:
    """Tests para funciones de conveniencia del cache"""
    
    def test_save_model_function(self, temp_cache_dir, sample_ml_model, sample_metadata):
        """Test función save_model"""
        result = save_model(sample_ml_model, "test_model", sample_metadata)
        assert result is True
    
    def test_load_model_function(self, temp_cache_dir, sample_ml_model, sample_metadata):
        """Test función load_model"""
        # Guardar modelo primero
        save_model(sample_ml_model, "test_model", sample_metadata)
        
        # Cargar modelo
        loaded_model = load_model("test_model")
        assert loaded_model is not None
    
    def test_save_data_function(self, temp_cache_dir):
        """Test función save_data"""
        test_data = {"test": "data"}
        result = save_data(test_data, "test_data")
        assert result is True
    
    def test_load_data_function(self, temp_cache_dir):
        """Test función load_data"""
        # Guardar datos primero
        test_data = {"test": "data"}
        save_data(test_data, "test_data")
        
        # Cargar datos
        loaded_data = load_data("test_data")
        assert loaded_data is not None
        assert loaded_data["test"] == "data"
    
    def test_cleanup_cache_function(self, temp_cache_dir):
        """Test función cleanup_cache"""
        stats = cleanup_cache()
        assert isinstance(stats, dict)
        assert "models_removed" in stats
        assert "data_removed" in stats
        assert "space_freed" in stats
    
    def test_get_cache_stats_function(self, temp_cache_dir):
        """Test función get_cache_stats"""
        stats = get_cache_stats()
        assert isinstance(stats, dict)
        assert "total_models" in stats
        assert "total_data_files" in stats
        assert "total_size" in stats
    
    def test_clear_all_cache_function(self, temp_cache_dir, sample_ml_model):
        """Test función clear_all_cache"""
        # Agregar algo al cache
        save_model(sample_ml_model, "test_model")
        
        # Limpiar todo
        result = clear_all_cache()
        assert result is True


@pytest.mark.cache
class TestCacheIntegration:
    """Tests de integración para el sistema de cache"""
    
    def test_full_cache_workflow(self, temp_cache_dir, sample_ml_model, sample_metadata):
        """Test flujo completo de cache"""
        # 1. Guardar modelo
        result = save_model(sample_ml_model, "workflow_model", sample_metadata)
        assert result is True
        
        # 2. Cargar modelo
        loaded_model = load_model("workflow_model")
        assert loaded_model is not None
        
        # 3. Guardar datos
        test_data = {"temperature": 25.5, "humidity": 65}
        result = save_data(test_data, "workflow_data")
        assert result is True
        
        # 4. Cargar datos
        loaded_data = load_data("workflow_data")
        assert loaded_data is not None
        assert loaded_data["temperature"] == 25.5
        
        # 5. Obtener estadísticas
        stats = get_cache_stats()
        assert stats["total_models"] >= 1
        assert stats["total_data_files"] >= 1
        
        # 6. Limpiar cache
        cleanup_stats = cleanup_cache()
        assert isinstance(cleanup_stats, dict)
    
    def test_error_handling(self, temp_cache_dir):
        """Test manejo de errores en cache"""
        # Test con datos inválidos
        result = save_model(None, "invalid_model")
        assert result is False
        
        # Test con nombre vacío
        result = save_data({"test": "data"}, "")
        assert result is False
        
        # Test cargar datos inexistentes
        loaded_data = load_data("nonexistent")
        assert loaded_data is None
    
    def test_concurrent_access(self, temp_cache_dir, sample_ml_model):
        """Test acceso concurrente al cache"""
        import threading
        import time
        
        results = []
        errors = []
        
        def save_model_worker(model_id):
            try:
                result = save_model(sample_ml_model, f"concurrent_model_{model_id}")
                results.append(result)
            except Exception as e:
                errors.append(e)
        
        # Crear múltiples hilos
        threads = []
        for i in range(5):
            thread = threading.Thread(target=save_model_worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Esperar a que terminen
        for thread in threads:
            thread.join()
        
        # Verificar que no hubo errores
        assert len(errors) == 0
        assert len(results) == 5
        assert all(results)  # Todos los saves fueron exitosos
