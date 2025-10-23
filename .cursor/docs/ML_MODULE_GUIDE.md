# 🤖 Guía del Módulo de Machine Learning - CorAlertMet Intelligence

## 📋 **Resumen del Módulo ML**

El módulo de Machine Learning de CorAlertMet Intelligence proporciona capacidades avanzadas de predicción meteorológica, forecasting y detección de anomalías. Está diseñado para funcionar tanto en la aplicación Kivy como en el dashboard Streamlit.

### 🎯 **Stack Tecnológico Actualizado**
- **Scikit-learn**: ML clásico (Random Forest, Gradient Boosting)
- **Darts**: Forecasting avanzado (ARIMA, ExponentialSmoothing, LinearRegression)
- **Plotly**: Visualizaciones interactivas
- **Streamlit**: Dashboard web
- **Pandas + NumPy**: Manipulación de datos

## 🏗️ **Arquitectura del Módulo**

### **Estructura de Directorios Actualizada**
```
pages_modules/ml_models/       # Módulos ML modulares
├── __init__.py               # Inicialización del módulo
├── precision_metrics.py      # Métricas de precisión de modelos
├── advanced_predictions.py   # Predicciones avanzadas con ML
├── intelligent_alerts.py     # Sistema de alertas inteligentes
└── model_validation.py       # Validación de modelos (Darts + Scikit-learn)

components/                    # Componentes reutilizables
├── footer.py                 # Footer modular
├── styles.py                 # Estilos corporativos
└── svg_icons_smooth.py       # Iconos SVG animados

models/                        # Directorio de modelos persistidos
├── models_metadata.json       # Metadatos de modelos
├── random_forest_model.pkl    # Modelo Random Forest
├── gradient_boosting_model.pkl # Modelo Gradient Boosting
├── scaler.pkl                # Escalador de características
└── alert_history.json        # Historial de alertas
```

### **Componentes Principales Actualizados**

#### **1. PrecisionMetrics**
- **Propósito**: Métricas detalladas de precisión de modelos meteorológicos
- **Funcionalidades**:
  - Precisión por horizonte temporal (24h, 48h, 72h)
  - Error cuadrático medio (RMSE) por variable
  - Skill de precipitación (POD, FAR, CSI)
  - Recomendaciones basadas en precisión
  - Estado de actualización de modelos

#### **2. AdvancedPredictions**
- **Propósito**: Predicciones avanzadas con algoritmos ML reales
- **Algoritmos**:
  - RandomForest Classifier para clasificación
  - GradientBoosting Regressor para regresión
- **Características**:
  - Entrenamiento automático con datos sintéticos
  - Predicción en tiempo real con modelos de Windy (HRRR, ECMWF, GFS27)
  - Validación cruzada temporal
  - Importancia de características
  - Gestión de modelos persistidos

#### **3. IntelligentAlerts**
- **Propósito**: Sistema de alertas inteligentes basado en ML
- **Algoritmos**:
  - Isolation Forest para detección de anomalías
  - Clasificación automática de severidad
- **Características**:
  - Detección automática de anomalías
  - Generación de alertas contextuales
  - Recomendaciones automáticas
  - Visualizaciones interactivas
  - Exportación de alertas

#### **4. ModelValidation**
- **Propósito**: Validación robusta usando Darts + Scikit-learn
- **Tecnologías**:
  - Darts: ARIMA, ExponentialSmoothing, LinearRegression
  - Scikit-learn: Cross-validation temporal
- **Características**:
  - Comparación de modelos de Windy
  - Métricas avanzadas (MAE, MSE, MAPE, R²)
  - Ranking de modelos
  - Fallback system si Darts no está disponible
  - Visualizaciones comparativas

## 🚀 **Instalación y Configuración**

### **Dependencias Requeridas**
```bash
# Dependencias ML (ya incluidas en requirements.txt)
scikit-learn>=1.3.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.15.0
joblib>=1.3.0
streamlit>=1.28.0

# Dependencias Opcionales (para validación avanzada)
darts>=0.24.0  # Para validación de modelos de Windy
```

### **Configuración de Variables de Entorno**
```env
# Configuración ML
ML_ENABLED=true
ML_MODELS_DIR=models
ML_CACHE_ENABLED=true

# Configuración Darts (opcional)
DARTS_AVAILABLE=true
DARTS_MODEL_TYPES=ARIMA,ExponentialSmoothing,LinearRegression

# Configuración de anomalías
ANOMALY_CONTAMINATION=0.05
ANOMALY_THRESHOLD=2.5

# Umbrales de predicción de tormentas
STORM_THRESHOLD_LOW=0.3
STORM_THRESHOLD_MEDIUM=0.5
STORM_THRESHOLD_HIGH=0.7
STORM_THRESHOLD_CRITICAL=0.85

# Modelos de Windy
WINDY_MODELS=HRRR,ECMWF,GFS27
WINDY_WEIGHTS=0.5,0.3,0.2
```

## 📊 **Uso del Módulo Actualizado**

### **1. Predicciones Avanzadas con ML**

```python
from pages_modules.ml_models.advanced_predictions import show_advanced_predictions

# En Streamlit
show_advanced_predictions()

# Uso programático
import streamlit as st
from pages_modules.ml_models.advanced_predictions import show_advanced_predictions

# Mostrar predicciones con modelos de Windy
st.title("Predicciones Avanzadas")
show_advanced_predictions()
```

### **2. Métricas de Precisión**

```python
from pages_modules.ml_models.precision_metrics import show_precision_metrics

# Mostrar métricas detalladas
show_precision_metrics()

# Incluye:
# - Precisión por horizonte temporal
# - RMSE por variable meteorológica
# - Skill de precipitación
# - Recomendaciones basadas en precisión
```

### **3. Alertas Inteligentes**

```python
from pages_modules.ml_models.intelligent_alerts import show_intelligent_alerts

# Mostrar sistema de alertas
show_intelligent_alerts()

# Características:
# - Detección automática de anomalías
# - Clasificación de severidad (CRITICAL, HIGH, MEDIUM, LOW)
# - Recomendaciones contextuales
# - Visualizaciones interactivas
# - Exportación de alertas
```

### **4. Validación de Modelos**

```python
from pages_modules.ml_models.model_validation import show_model_validation

# Validación completa con Darts + Scikit-learn
show_model_validation()

# Incluye:
# - Validación cruzada temporal
# - Comparación de modelos de Windy
# - Métricas avanzadas (MAE, MSE, MAPE, R²)
# - Ranking de modelos
# - Fallback si Darts no está disponible
```

## 🎓 **Entrenamiento Automático de Modelos**

### **1. Entrenamiento Automático con Datos Sintéticos**

```python
# Los modelos se entrenan automáticamente con datos sintéticos realistas
# No requiere configuración manual

# En advanced_predictions.py:
# - 1000 muestras de datos meteorológicos
# - Variables: temperatura, humedad, presión, viento, nubosidad
# - Entrenamiento automático de Random Forest y Gradient Boosting
# - Validación cruzada temporal con 5 folds
```

### **2. Predicción con Modelos de Windy**

```python
# Predicción automática usando 3 modelos de Windy:
windy_models = {
    "HRRR": {"temp": 28.5, "humidity": 75, "pressure": 1008, "wind": 15, "cloud": 60},
    "ECMWF": {"temp": 26.2, "humidity": 78, "pressure": 1012, "wind": 12, "cloud": 55},
    "GFS27": {"temp": 27.8, "humidity": 72, "pressure": 1005, "wind": 18, "cloud": 65}
}

# Predicción combinada con pesos ponderados:
# HRRR: 50%, ECMWF: 30%, GFS27: 20%
```

### **3. Detección Automática de Anomalías**

```python
# Entrenamiento automático de Isolation Forest:
# - 500 muestras de datos meteorológicos
# - 5% de anomalías inyectadas artificialmente
# - Detección automática con puntuación de anomalía
# - Clasificación de severidad automática
```

## 📈 **Dashboard Streamlit Actualizado**

### **Acceso al Dashboard**
1. Ejecutar aplicación: `streamlit run app.py`
2. Navegar a la pestaña "🤖 Dashboard de Machine Learning"
3. Explorar las 4 secciones disponibles:
   - **Predicción**: Predicciones avanzadas con ML
   - **Pronóstico**: Métricas de precisión de modelos
   - **Anomalías**: Sistema de alertas inteligentes
   - **Entrenamiento**: Validación de modelos

### **Características del Dashboard Actualizado**
- **Interfaz modular**: Componentes reutilizables
- **Visualizaciones interactivas**: Gráficos con Plotly
- **Predicción automática**: Sin configuración manual
- **Validación robusta**: Darts + Scikit-learn
- **Alertas inteligentes**: Detección automática de anomalías
- **Iconos SVG animados**: Interfaz moderna y profesional

## 🔧 **Configuración Avanzada**

### **Personalización de Modelos de Windy**

```python
# Configurar modelos de Windy en advanced_predictions.py
windy_models = {
    "HRRR": {"temp": 28.5, "humidity": 75, "pressure": 1008, "wind": 15, "cloud": 60},
    "ECMWF": {"temp": 26.2, "humidity": 78, "pressure": 1012, "wind": 12, "cloud": 55},
    "GFS27": {"temp": 27.8, "humidity": 72, "pressure": 1005, "wind": 18, "cloud": 65}
}

# Pesos para predicción combinada
weights = {"HRRR": 0.5, "ECMWF": 0.3, "GFS27": 0.2}
```

### **Configuración de Darts (Opcional)**

```python
# Personalizar modelos de forecasting en model_validation.py
models = {
    'ARIMA': ARIMA(p=1, d=1, q=1),
    'ExponentialSmoothing': ExponentialSmoothing(),
    'LinearRegression': LinearRegressionModel(lags=24)
}
```

### **Umbrales de Alertas Inteligentes**

```python
# Personalizar umbrales en intelligent_alerts.py
alert_thresholds = {
    'temperature': {'min': -5, 'max': 45, 'critical': 50},
    'humidity': {'min': 0, 'max': 100, 'critical': 95},
    'pressure': {'min': 950, 'max': 1050, 'critical': 900},
    'wind_speed': {'min': 0, 'max': 50, 'critical': 80},
    'precipitation': {'min': 0, 'max': 100, 'critical': 150}
}
```

## 📊 **Métricas y Monitoreo Actualizado**

### **Métricas de Predicciones Avanzadas**
- **Accuracy**: Precisión del Random Forest Classifier
- **Precision**: Precisión del clasificador
- **Recall**: Sensibilidad del clasificador
- **F1-Score**: Media armónica de precisión y recall
- **R² Score**: Coeficiente de determinación del Gradient Boosting
- **MAE**: Error absoluto medio
- **MSE**: Error cuadrático medio
- **Feature Importance**: Importancia de variables meteorológicas

### **Métricas de Precisión de Modelos**
- **Precisión por Horizonte**: 24h, 48h, 72h
- **RMSE por Variable**: Temperatura, humedad, presión, viento
- **Skill de Precipitación**: POD, FAR, CSI
- **Estado de Actualización**: Timestamp de última actualización

### **Métricas de Alertas Inteligentes**
- **Tasa de Anomalías**: Porcentaje de anomalías detectadas
- **Distribución de Severidad**: CRITICAL, HIGH, MEDIUM, LOW
- **Puntuación de Anomalía**: Score de Isolation Forest
- **Recomendaciones**: Alertas contextuales generadas

### **Métricas de Validación de Modelos**
- **Cross-Validation**: 5 folds temporales
- **MAE por Modelo**: HRRR, ECMWF, GFS27
- **MSE por Modelo**: Error cuadrático medio
- **MAPE por Modelo**: Error porcentual absoluto medio
- **R² por Modelo**: Coeficiente de determinación
- **Ranking de Modelos**: Comparación objetiva

## 🚨 **Solución de Problemas Actualizado**

### **Error: "Darts no disponible"**
```python
# El sistema funciona sin Darts, pero con validación básica
# Para validación avanzada, instalar:
pip install darts>=0.24.0
```

### **Error: "Modelos no entrenados"**
```python
# Los modelos se entrenan automáticamente con datos sintéticos
# No requiere intervención manual
# Verificar en advanced_predictions.py que se ejecute el entrenamiento
```

### **Error: "Dependencias ML no encontradas"**
```bash
# Instalar dependencias básicas
pip install scikit-learn pandas numpy plotly streamlit joblib
```

### **Error: "Memoria insuficiente"**
```python
# Reducir tamaño de dataset sintético en model_validation.py
n_samples = 500  # En lugar de 1000
```

### **Error: "ImportError en módulos ML"**
```python
# Verificar que los módulos estén en pages_modules/ml_models/
# Verificar __init__.py incluye todos los módulos
from pages_modules.ml_models import show_advanced_predictions
```

## 🔄 **Mantenimiento y Actualización**

### **Limpieza Automática de Modelos**
```python
# Los modelos se guardan automáticamente en models/
# Limpieza manual si es necesario:
import os
import glob

# Eliminar modelos antiguos
old_models = glob.glob('models/*_v*.pkl')
for model in old_models:
    os.remove(model)
```

### **Backup de Modelos**
```python
# Crear backup de modelos importantes
import shutil
import datetime

backup_dir = f"backup_models_{datetime.datetime.now().strftime('%Y%m%d')}"
shutil.copytree('models', backup_dir)
```

### **Monitoreo de Rendimiento**
```python
# Verificar métricas en el dashboard Streamlit
# - Accuracy, Precision, Recall, F1-Score
# - MAE, MSE, R² Score
# - Feature Importance
# - Cross-validation scores
```

## 🎯 **Mejores Prácticas Actualizadas**

### **1. Entrenamiento Automático**
- Los modelos se entrenan automáticamente con datos sintéticos
- No requiere intervención manual
- Validación cruzada temporal incluida

### **2. Monitoreo Continuo**
- Verificar métricas en el dashboard Streamlit
- Comparar modelos de Windy (HRRR, ECMWF, GFS27)
- Ajustar pesos de predicción según rendimiento

### **3. Gestión de Modelos**
- Modelos persistidos automáticamente en `models/`
- Backup manual cuando sea necesario
- Limpieza de modelos antiguos

### **4. Optimización de Recursos**
- Darts opcional para validación avanzada
- Fallback a validación básica si Darts no está disponible
- Datos sintéticos optimizados para rendimiento

### **5. Stack Tecnológico Simplificado**
- **Scikit-learn**: ML clásico confiable
- **Darts**: Forecasting avanzado (opcional)
- **Plotly**: Visualizaciones interactivas
- **Streamlit**: Dashboard moderno
- **Sin Prophet**: Eliminado según preferencias

---

**Desarrollado para CorAlertMet Intelligence v2.5.0** 🚀

*"Machine Learning que salva vidas en la aviación"* ✈️🤖

### **📋 Resumen de Cambios v2.5.0**
- ✅ **Fase 5 Completada**: Validación de modelos con Darts + Scikit-learn
- ✅ **Stack Simplificado**: Solo 3 librerías principales
- ✅ **Interfaz Modular**: Componentes reutilizables
- ✅ **Predicción Automática**: Sin configuración manual
- ✅ **Validación Robusta**: Métricas profesionales
- ✅ **Documentación Actualizada**: Guía completa y actualizada
