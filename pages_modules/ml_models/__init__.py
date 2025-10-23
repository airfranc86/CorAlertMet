"""
Módulos de Machine Learning para CorAlertMet Intelligence
Sistema de Alertas Meteorológicas con ML Avanzado
"""

__version__ = "1.0.0"
__author__ = "Francisco Aucar"

# Importar módulos principales (solo los que existen)
from .precision_metrics import show_precision_metrics
from .advanced_predictions import show_advanced_predictions
from .intelligent_alerts import show_intelligent_alerts
from .model_validation import show_model_validation

__all__ = [
    "show_precision_metrics",
    "show_advanced_predictions",
    "show_intelligent_alerts",
    "show_model_validation"
]
