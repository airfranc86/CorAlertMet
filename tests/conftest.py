"""
Configuración global de pytest para CorAlertMet Intelligence
"""
import pytest
import os
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

# Agregar el directorio raíz al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

@pytest.fixture(scope="session")
def project_root_path():
    """Ruta del directorio raíz del proyecto"""
    return project_root

@pytest.fixture(scope="session")
def temp_cache_dir():
    """Directorio temporal para cache durante tests"""
    temp_dir = tempfile.mkdtemp(prefix="coralert_test_cache_")
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)

@pytest.fixture(scope="session")
def temp_logs_dir():
    """Directorio temporal para logs durante tests"""
    temp_dir = tempfile.mkdtemp(prefix="coralert_test_logs_")
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)

@pytest.fixture
def mock_streamlit_session():
    """Mock de session_state de Streamlit"""
    mock_session = MagicMock()
    mock_session.authenticated = False
    mock_session.user_role = None
    mock_session.get = MagicMock(return_value=None)
    with patch('streamlit.session_state', mock_session) as mock_session:
        yield mock_session

@pytest.fixture
def mock_streamlit_st():
    """Mock de funciones de Streamlit"""
    with patch('streamlit.st') as mock_st:
        yield mock_st

@pytest.fixture
def sample_weather_data():
    """Datos meteorológicos de ejemplo para tests"""
    return {
        "temperature": 25.5,
        "humidity": 65.0,
        "pressure": 1013.2,
        "wind_speed": 12.3,
        "wind_direction": 180,
        "description": "Parcialmente nublado",
        "visibility": 10.0,
        "cloudiness": 45.0,
        "source": "OpenWeatherMap",
        "station": {
            "name": "Córdoba",
            "country": "AR",
            "coordinates": "31.42°N, 64.19°O"
        }
    }

@pytest.fixture
def sample_ml_model():
    """Modelo ML de ejemplo para tests"""
    from sklearn.ensemble import RandomForestClassifier
    import numpy as np
    
    # Crear modelo simple para tests
    X = np.random.rand(100, 5)
    y = np.random.randint(0, 2, 100)
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(X, y)
    return model

@pytest.fixture
def sample_metadata():
    """Metadatos de ejemplo para tests"""
    return {
        "model_name": "test_model",
        "version": "1.0",
        "accuracy": 0.85,
        "created_at": "2024-01-01T00:00:00",
        "features": ["temp", "humidity", "pressure", "wind_speed", "cloudiness"]
    }

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Configurar entorno de test automáticamente"""
    # Variables de entorno para tests
    os.environ['ADMIN_PASSWORD'] = 'test_admin_password'
    os.environ['GUEST_PASSWORD'] = 'test_guest_password'
    os.environ['ENCRYPTION_KEY'] = 'test_encryption_key_32_chars_long'
    
    yield
    
    # Limpiar variables de entorno después del test
    for key in ['ADMIN_PASSWORD', 'GUEST_PASSWORD', 'ENCRYPTION_KEY']:
        os.environ.pop(key, None)

@pytest.fixture
def mock_cache_manager():
    """Mock del CacheManager para tests"""
    with patch('cache.cache_manager.CacheManager') as mock_cm:
        mock_instance = MagicMock()
        mock_cm.return_value = mock_instance
        yield mock_instance
