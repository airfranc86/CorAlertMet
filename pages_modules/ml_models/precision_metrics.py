"""
Módulo de Métricas de Precisión para CorAlertMet Intelligence
Muestra confiabilidad detallada de modelos meteorológicos
"""

from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

@st.cache_data(ttl=1800, show_spinner=False)
def show_precision_metrics():
    """Mostrar métricas de precisión detalladas de modelos"""
    
  
    # Métricas de confiabilidad general
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="🔍 CONFIABILIDAD",
            value="MEDIA",
            delta="85%",
            help="Nivel general de confiabilidad de los modelos"
        )
    
    # Tabla de interpretación rápida
    st.markdown("### 📋 Interpretación de Resultados")
    
    interpretation_data = {
        "Modelo": ["ECMWF", "GFS27", "HRRR"],
        "24h (%)": ["94.2", "88.5", "96.8"],
        "48h (%)": ["89.7", "82.3", "92.1"],
        "72h (%)": ["84.1", "76.7", "87.5"],
        "Recomendación": [
            "✅ Ideal para pronósticos largos",
            "⚠️ Bueno para validación cruzada", 
            "🎯 Excelente para corto plazo"
        ]
    }
    
    df_interpretation = pd.DataFrame(interpretation_data)
    st.dataframe(df_interpretation, use_container_width=True)
    
    # Información adicional
    st.info("""
    **💡 Notas Técnicas:**
    - **ECMWF**: Modelo europeo, excelente para pronósticos de 3-7 días
    - **GFS27**: Modelo global de NOAA, bueno para validación cruzada
    - **HRRR**: Alta resolución, ideal para pronósticos de 0-24 horas
    """)