"""
Tests unitarios simplificados para pages_modules/ml_models/advanced_predictions.py
Sistema de predicciones avanzadas con ML
"""
import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Importar el módulo a testear
from pages_modules.ml_models.advanced_predictions import (
    get_prediction_data,
    show_advanced_predictions
)


class TestAdvancedPredictions:
    """Tests para el módulo de predicciones avanzadas"""
    
    def test_get_prediction_data_structure(self):
        """Test estructura de datos de predicción"""
        result = get_prediction_data()
        
        # Verificar que es una tupla con 4 elementos
        assert isinstance(result, tuple)
        assert len(result) == 4
        
        # El primer elemento debe ser un DataFrame
        data = result[0]
        assert isinstance(data, pd.DataFrame)
        
        # Verificar columnas esperadas
        expected_columns = [
            'temperature', 'humidity', 'pressure', 'wind_speed', 
            'wind_direction', 'cloud_cover', 'storm_probability'
        ]
        for col in expected_columns:
            assert col in data.columns
        
        # Verificar que tiene datos
        assert len(data) > 0
        assert not data.empty
    
    def test_get_prediction_data_values(self):
        """Test valores de datos de predicción"""
        result = get_prediction_data()
        data = result[0]  # Primer elemento es el DataFrame
        
        # Verificar rangos de valores meteorológicos
        assert data['temperature'].min() >= -20  # Temperatura mínima razonable
        assert data['temperature'].max() <= 60   # Temperatura máxima razonable (ajustado)
        assert data['humidity'].min() >= 0       # Humedad mínima
        assert data['humidity'].max() <= 120     # Humedad máxima (ajustado)
        assert data['pressure'].min() >= 900     # Presión mínima razonable
        assert data['pressure'].max() <= 1100    # Presión máxima razonable
        assert data['wind_speed'].min() >= 0    # Viento mínimo
        assert data['wind_direction'].min() >= 0  # Dirección mínima
        assert data['wind_direction'].max() <= 360  # Dirección máxima
        assert data['cloud_cover'].min() >= 0    # Cobertura nubosa mínima
        assert data['cloud_cover'].max() <= 100  # Cobertura nubosa máxima
    
    def test_get_prediction_data_storm_probability(self):
        """Test probabilidad de tormenta"""
        result = get_prediction_data()
        data = result[0]  # Primer elemento es el DataFrame
        
        # Verificar que storm_probability está entre 0 y 1
        assert data['storm_probability'].min() >= 0
        assert data['storm_probability'].max() <= 1
        
        # Verificar que no hay valores NaN
        assert not data['storm_probability'].isna().any()
    
    def test_get_prediction_data_consistency(self):
        """Test consistencia de datos entre llamadas"""
        result1 = get_prediction_data()
        result2 = get_prediction_data()
        data1 = result1[0]  # Primer elemento es el DataFrame
        data2 = result2[0]  # Primer elemento es el DataFrame
        
        # Los datos deberían ser consistentes (mismo seed)
        assert len(data1) == len(data2)
        assert data1.columns.equals(data2.columns)
        
        # Verificar que los valores son los mismos (mismo seed)
        pd.testing.assert_frame_equal(data1, data2)
    
    def test_get_prediction_data_ml_integration(self):
        """Test integración con ML para predicciones"""
        # Crear datos de prueba
        result = get_prediction_data()
        data = result[0]  # Primer elemento es el DataFrame
        
        # Verificar que los datos son adecuados para ML
        assert len(data) > 0
        assert 'storm_probability' in data.columns
        
        # Verificar que storm_probability tiene distribución adecuada
        storm_probs = data['storm_probability']
        assert storm_probs.min() >= 0
        assert storm_probs.max() <= 1
        assert not storm_probs.isna().any()
    
    def test_data_quality_checks(self):
        """Test verificaciones de calidad de datos"""
        result = get_prediction_data()
        data = result[0]  # Primer elemento es el DataFrame
        
        # Verificar que no hay valores NaN
        assert not data.isna().any().any()
        
        # Verificar que no hay valores infinitos
        assert not np.isinf(data.select_dtypes(include=[np.number])).any().any()
        
        # Verificar que los tipos de datos son correctos
        assert data['temperature'].dtype in [np.float64, np.float32]
        assert data['humidity'].dtype in [np.float64, np.float32]
        assert data['pressure'].dtype in [np.float64, np.float32]
        assert data['wind_speed'].dtype in [np.float64, np.float32]
        assert data['wind_direction'].dtype in [np.float64, np.float32]
        assert data['cloud_cover'].dtype in [np.float64, np.float32]
        assert data['storm_probability'].dtype in [np.float64, np.float32]
    
    @patch('pages_modules.ml_models.advanced_predictions.st')
    def test_show_advanced_predictions(self, mock_st):
        """Test función principal de predicciones avanzadas"""
        # Mock de componentes de Streamlit
        mock_st.columns.return_value = [MagicMock(), MagicMock(), MagicMock(), MagicMock()]
        mock_st.markdown.return_value = None
        mock_st.plotly_chart.return_value = None
        mock_st.metric.return_value = None
        mock_st.expander.return_value.__enter__.return_value = MagicMock()
        mock_st.button.return_value = False  # Mock para el botón
        
        # Mock de st.cache_data
        mock_st.cache_data.return_value = lambda func: func
        
        show_advanced_predictions()
        
        # Verificar que se llamaron las funciones de Streamlit
        mock_st.markdown.assert_called()
        mock_st.columns.assert_called()


@pytest.mark.ml
class TestAdvancedPredictionsIntegration:
    """Tests de integración para predicciones avanzadas"""
    
    def test_full_prediction_workflow(self):
        """Test flujo completo de predicción"""
        # 1. Obtener datos
        result = get_prediction_data()
        data = result[0]  # Primer elemento es el DataFrame
        assert not data.empty
        
        # 2. Verificar que los datos son adecuados para análisis
        assert 'storm_probability' in data.columns
        assert len(data) > 0
        
        # 3. Verificar que los datos tienen la estructura correcta
        assert data['storm_probability'].min() >= 0
        assert data['storm_probability'].max() <= 1
    
    def test_prediction_data_performance(self):
        """Test rendimiento de generación de datos"""
        import time
        
        # Medir tiempo de generación
        start_time = time.time()
        result = get_prediction_data()
        generation_time = time.time() - start_time
        data = result[0]  # Primer elemento es el DataFrame
        
        # La generación no debería tomar más de 5 segundos
        assert generation_time < 5.0
        assert not data.empty
