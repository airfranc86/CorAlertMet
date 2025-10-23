"""
Machine Learning Dashboard - CorAlertMet Intelligence
Dashboard de ML con 4 pestañas: Predicción, Pronóstico, Anomalías, Entrenamiento
"""

import streamlit as st
import sys
import os
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# Agregar src al path (comentado - directorio src no existe)
# sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Importar componentes
from components.footer import show_footer
from components.styles import apply_corporate_styles
from components.svg_icons_smooth import show_svg_icon

# Importar módulos ML
from pages_modules.ml_models.precision_metrics import show_precision_metrics
from pages_modules.ml_models.advanced_predictions import show_advanced_predictions
from pages_modules.ml_models.intelligent_alerts import show_intelligent_alerts
from pages_modules.ml_models.model_validation import show_model_validation

# Configuración de la página
st.set_page_config(
    page_title="ML Dashboard - CorAlertMet Intelligence",
    page_icon="🤖",
    layout="wide"
)

# Aplicar estilos corporativos
apply_corporate_styles()

def main(selected_api="OpenWeatherMap", selected_model=None):
    """Mostrar dashboard de Machine Learning con control de acceso basado en roles"""

    # Verificar rol del usuario
    user_role = st.session_state.get('user_role', None)

    # Título con icono SVG animado
    col1, col2 = st.columns([1, 20])
    with col1:
        st.markdown("""
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" fill="none" viewBox="0 0 24 24">
        <style>
        @keyframes eye { 90% { transform: none; animation-timing-function: ease-in; } 93% { transform: translateY(15px) scaleY(0); } 100% { animation-timing-function: ease-out; } }
        @keyframes squeeze { 90% { transform: none; animation-timing-function: ease-in; } 93% { transform: translateY(3px) scaleY(0.8); } 100% { animation-timing-function: ease-out; } }
        .eye-1 { animation: eye 2.4s infinite; }
        .eye-2 { animation: squeeze 2.4s infinite; }
        </style>
        <path class="eye-1" stroke="#0A0A30" stroke-width="1.5"
d = (
              "M19.195 11.31c.325.41.325.97 0 1.38-1.114 1.4-3.916 4.45-7.195 4.45-3.28 0-6.08-3.05-7.195-4.45a1.097 1.097 0 010-1.38C5.92 9.91 8.721 6.86 12 6.86c3.28 0 6.08 3.05 7.195 4.45z" />
          )
        <circle class="eye-2" cx="12" cy="12" r="1.972" stroke="#265BFF" stroke-width="1.5" />
        </svg>
        """, unsafe_allow_html=True)
    with col2:
        st.title("Dashboard de Machine Learning")

    st.markdown("**Análisis predictivo y modelos meteorológicos**")

    # Mostrar API seleccionada
    st.info(f"🌐 **API Seleccionada:** {selected_api}")

    # Mostrar información del rol del usuario
    if user_role == "admin":
        st.success("🔑 **Acceso Administrador**: Acceso completo a todas las funcionalidades")
    elif user_role == "invitado":
        st.info("👤 **Acceso Invitado**: Acceso limitado a funcionalidades básicas")
    else:
        st.error("❌ **Error**: No se pudo determinar el rol del usuario")
        return

    # Crear pestañas según el rol del usuario
    if user_role == "admin":
        # Admin: Acceso completo a todas las pestañas
        tab1, tab2, tab3, tab4 = st.tabs([
            "⚡ Predicción",
            "📊 Pronóstico",
            "🔍 Anomalías",
            "🎯 Entrenamiento"
        ])
    elif user_role == "invitado":
        # Invitado: Solo 2 pestañas (Predicción y Pronóstico)
        tab1, tab2 = st.tabs([
            "⚡ Predicción",
            "📊 Pronóstico"
        ])
        # Crear pestañas vacías para mantener la estructura
        tab3 = None
        tab4 = None
    else:
        st.error("❌ **Error**: No se pudo determinar el rol del usuario")
        return


    with tab1:
        # Icono animado para Predicción
        col1, col2 = st.columns([1, 20])
        with col1:
            st.markdown("""
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <style>
            @keyframes float { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-3px); } }
            .crystal { animation: float 2s ease-in-out infinite; }
            </style>
            <circle class="crystal" cx="12" cy="12" r="8" stroke="#8B5CF6" stroke-width="2" fill="none"/>
            <circle cx="12" cy="12" r="3" fill="#8B5CF6" opacity="0.6"/>
            </svg>
            """, unsafe_allow_html=True)
        with col2:
            st.subheader("Predicción de tormentas")

        show_prediction_tab()

    with tab2:
        # Icono animado para Pronóstico
        col1, col2 = st.columns([1, 20])
        with col1:
            st.markdown("""
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <style>
            @keyframes draw { 0% { stroke-dasharray: 0 100; } 100% { stroke-dasharray: 100 0; } }
            .line { animation: draw 2s ease-in-out infinite; }
            </style>
<path class = (
                "line" d="M3 17L9 11L13 15L21 7" stroke="#10B981" stroke-width="2" fill="none" stroke-linecap="round"/>
            )
            <circle cx="3" cy="17" r="2" fill="#10B981"/>
            <circle cx="9" cy="11" r="2" fill="#10B981"/>
            <circle cx="13" cy="15" r="2" fill="#10B981"/>
            <circle cx="21" cy="7" r="2" fill="#10B981"/>
            </svg>
            """, unsafe_allow_html=True)
        with col2:
            st.subheader("Pronóstico Meteorológico")

        show_forecast_tab()

    # Pestañas restringidas solo para admin
    if user_role == "admin" and tab3 is not None:
        with tab3:
            # Icono animado para Anomalías
            col1, col2 = st.columns([1, 20])
            with col1:
                st.markdown("""
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <style>
                @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
                .alert { animation: pulse 1.5s ease-in-out infinite; }
                </style>
                <path class="alert" d="M12 2L22 20H2L12 2Z" stroke="#F59E0B" stroke-width="2" fill="none"/>
                <path d="M12 8V12" stroke="#F59E0B" stroke-width="2" stroke-linecap="round"/>
                <circle cx="12" cy="16" r="1" fill="#F59E0B"/>
                </svg>
                """, unsafe_allow_html=True)
            with col2:
                st.subheader("Detección de anomalías")

            show_anomalies_tab()

    if user_role == "admin" and tab4 is not None:
        with tab4:
            # Icono animado para Entrenamiento
            col1, col2 = st.columns([1, 20])
            with col1:
                st.markdown("""
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <style>
                @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
                .target { animation: spin 3s linear infinite; }
                </style>
                <circle class="target" cx="12" cy="12" r="10" stroke="#EF4444" stroke-width="2" fill="none"/>
                <circle cx="12" cy="12" r="6" stroke="#EF4444" stroke-width="2" fill="none"/>
                <circle cx="12" cy="12" r="2" fill="#EF4444"/>
                </svg>
                """, unsafe_allow_html=True)
            with col2:
                st.subheader("Entrenamiento de modelos")

            show_training_tab()

    # Mostrar mensaje de restricción para invitados
    if user_role == "invitado":
        st.markdown("---")
        st.info("""
🔒 **Acceso Restringido**: Como usuario invitado, solo tienes acceso a las pestañas de **Predicción** \
            y **Pronóstico**.

Para acceder a las funcionalidades avanzadas de **Anomalías** y **Entrenamiento**, contacta al \
            administrador del sistema.
        """)

def show_prediction_tab():
    """Pestaña de predicción de tormentas con ML avanzado"""

    # Mostrar predicciones avanzadas
    show_advanced_predictions()

def show_forecast_tab():
    """Pestaña de pronóstico meteorológico con métricas de precisión"""

    # Mostrar métricas de precisión
    show_precision_metrics()

    st.markdown("---")

    # Generar datos de pronóstico cada 30 minutos (48 puntos en 24 horas)
    dates = [datetime.now() + timedelta(minutes=30*i) for i in range(48)]
    temperatures = 25 + 5 * np.sin(np.linspace(0, 4*np.pi, 48)) + np.random.normal(0, 1, 48)
    humidity = 60 + 20 * np.sin(np.linspace(0, 2*np.pi, 48)) + np.random.normal(0, 5, 48)
    wind_speed = 15 + 10 * np.sin(np.linspace(0, 3*np.pi, 48)) + np.random.normal(0, 2, 48)

    # Convertir valores a enteros
    temperatures = np.round(temperatures).astype(int)
    humidity = np.round(humidity).astype(int)
    wind_speed = np.round(wind_speed).astype(int)

    # Crear horarios redondos cada 30 minutos
    time_labels = []
    for d in dates:
        # Redondear a la media hora más cercana
        minute = d.minute
        if minute < 15:
            minute = 0
        elif minute < 45:
            minute = 30
        else:
            minute = 0
            d = d + timedelta(hours=1)
        time_labels.append(d.replace(minute=minute, second=0, microsecond=0).strftime("%H:%M"))

    df_forecast = pd.DataFrame({
        "Hora": time_labels,
        "Temperatura (°C)": temperatures,
        "Humedad (%)": humidity,
        "Viento (km/h)": wind_speed
    })

    # Gráficos de pronóstico
    col1, col2 = st.columns(2)

    with col1:
        fig_temp = px.line(df_forecast, x="Hora", y="Temperatura (°C)",
                          title="Pronóstico de Temperatura")
        st.plotly_chart(fig_temp, use_container_width=True)

    with col2:
        fig_humidity = px.line(df_forecast, x="Hora", y="Humedad (%)",
                              title="Pronóstico de Humedad")
        st.plotly_chart(fig_humidity, use_container_width=True)

def show_anomalies_tab():
    """Pestaña de detección de anomalías con alertas inteligentes"""

    # Mostrar sistema de alertas inteligentes
    show_intelligent_alerts()

def show_training_tab():
    """Pestaña de entrenamiento de modelos con validación completa"""

    # Mostrar validación de modelos
    show_model_validation()

# Ejecutar la página
if __name__ == "__main__":
    main()
