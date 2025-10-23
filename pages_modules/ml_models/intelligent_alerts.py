"""
Módulo de Alertas Inteligentes para CorAlertMet Intelligence
Sistema de notificaciones automáticas basadas en ML
"""

import json
import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

class IntelligentAlertSystem:
    """Sistema de alertas inteligentes basado en ML"""

    def __init__(self):
        self.alert_history = []
        self.anomaly_model = None
        self.scaler = StandardScaler()
        self.alert_thresholds = {
            'temperature': {'min': -5, 'max': 45, 'critical': 50},
            'humidity': {'min': 0, 'max': 100, 'critical': 95},
            'pressure': {'min': 950, 'max': 1050, 'critical': 900},
            'wind_speed': {'min': 0, 'max': 50, 'critical': 80},
            'precipitation': {'min': 0, 'max': 100, 'critical': 150}
        }

    def generate_synthetic_data(self, n_samples=500):
        """Generar datos sintéticos para entrenamiento"""
        np.random.seed(42)

        # Datos normales
        normal_data = {
            'temperature': np.random.normal(25, 8, n_samples),
            'humidity': np.random.normal(65, 15, n_samples),
            'pressure': np.random.normal(1013, 20, n_samples),
            'wind_speed': np.random.exponential(12, n_samples),
            'precipitation': np.random.exponential(5, n_samples),
            'timestamp': [datetime.now() - timedelta(hours=i) for i in range(n_samples, 0, -1)]
        }

        # Agregar anomalías (5% de los datos)
        n_anomalies = int(n_samples * 0.05)
        anomaly_indices = np.random.choice(n_samples, n_anomalies, replace=False)

        for idx in anomaly_indices:
            # Crear anomalías realistas
            if np.random.random() > 0.5:
                # Anomalía de temperatura extrema
                normal_data['temperature'][idx] = np.random.choice([-15, 55])
            else:
                # Anomalía de presión extrema
                normal_data['pressure'][idx] = np.random.choice([900, 1100])

        df = pd.DataFrame(normal_data)
        df['is_anomaly'] = df.index.isin(anomaly_indices)

        return df

    def train_anomaly_detection(self, df):
        """Entrenar modelo de detección de anomalías"""
        # Preparar datos
        features = ['temperature', 'humidity', 'pressure', 'wind_speed', 'precipitation']
        X = df[features]

        # Escalar datos
        X_scaled = self.scaler.fit_transform(X)

        # Entrenar Isolation Forest
        self.anomaly_model = IsolationForest(
            contamination=0.05,  # 5% de anomalías esperadas
            random_state=42
        )
        self.anomaly_model.fit(X_scaled)

        return features

    def detect_anomalies(self, df):
        """Detectar anomalías en nuevos datos"""
        if self.anomaly_model is None:
            return df

        features = ['temperature', 'humidity', 'pressure', 'wind_speed', 'precipitation']
        X = df[features]
        X_scaled = self.scaler.transform(X)

        # Predecir anomalías
        anomaly_scores = self.anomaly_model.decision_function(X_scaled)
        predictions = self.anomaly_model.predict(X_scaled)

        df['anomaly_score'] = anomaly_scores
        df['is_anomaly_predicted'] = predictions == -1

        return df

    def generate_alert(self, row, alert_type="ANOMALY"):
        """Generar alerta basada en anomalía detectada"""
        alert = {
            'timestamp': row['timestamp'],
            'type': alert_type,
            'severity': self._calculate_severity(row),
            'message': self._generate_message(row),
            'variables': self._get_anomalous_variables(row),
            'recommendations': self._get_recommendations(row)
        }

        self.alert_history.append(alert)
        return alert

    def _calculate_severity(self, row):
        """Calcular severidad de la alerta"""
        score = abs(row['anomaly_score'])

        if score > 0.8:
            return "CRITICAL"
        elif score > 0.5:
            return "HIGH"
        elif score > 0.3:
            return "MEDIUM"
        else:
            return "LOW"

    def _generate_message(self, row):
        """Generar mensaje de alerta personalizado"""
        variables = self._get_anomalous_variables(row)

        if len(variables) == 1:
            var = variables[0]
            return f"Anomalía detectada en {var}: {row[var]:.1f}"
        else:
            return f"Anomalías múltiples detectadas en: {', '.join(variables)}"

    def _get_anomalous_variables(self, row):
        """Identificar variables con valores anómalos"""
        anomalous = []

        for var, thresholds in self.alert_thresholds.items():
            if var in row:
                value = row[var]
                if (value < thresholds['min'] or
                    value > thresholds['max'] or
                    value > thresholds.get('critical', float('inf'))):
                    anomalous.append(var)

        return anomalous

    def _get_recommendations(self, row):
        """Generar recomendaciones basadas en anomalías detectadas"""
        recommendations = []

        if row['temperature'] > 40:
            recommendations.append("⚠️ Temperatura extrema - Evitar exposición prolongada")

        if row['wind_speed'] > 30:
            recommendations.append("🌪️ Viento fuerte - Evitar actividades al aire libre")

        if row['pressure'] < 1000:
            recommendations.append("🌧️ Baja presión - Posible cambio meteorológico")

        if row['humidity'] > 90:
            recommendations.append("💧 Humedad extrema - Condiciones de niebla")

        if not recommendations:
            recommendations.append("✅ Condiciones dentro de rangos normales")

        return recommendations

def show_intelligent_alerts():
    """Mostrar sistema de alertas inteligentes"""


    # Inicializar sistema de alertas
    if 'alert_system' not in st.session_state:
        st.session_state.alert_system = IntelligentAlertSystem()

    alert_system = st.session_state.alert_system

    # Generar y mostrar datos
    st.markdown("### 📊 Datos Meteorológicos en Tiempo Real")

    # Generar datos sintéticos
    df = alert_system.generate_synthetic_data(100)

    # Entrenar modelo si no está entrenado
    if alert_system.anomaly_model is None:
        with st.spinner("Entrenando modelo de detección de anomalías..."):
            features = alert_system.train_anomaly_detection(df)
            st.success("✅ Modelo entrenado exitosamente")

    # Detectar anomalías
    df_with_anomalies = alert_system.detect_anomalies(df)

    # Mostrar estadísticas
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Muestras", len(df_with_anomalies))

    with col2:
        anomalies = df_with_anomalies['is_anomaly_predicted'].sum()
        st.metric("Anomalías Detectadas", anomalies)

    with col3:
        anomaly_rate = (anomalies / len(df_with_anomalies)) * 100
        st.metric("Tasa de Anomalías", f"{anomaly_rate:.1f}%")

    with col4:
        st.metric("Modelo Activo", "Isolation Forest")

    # Visualización de anomalías

    # Gráfico de dispersión con anomalías
    fig_scatter = px.scatter(
        df_with_anomalies,
        x='temperature',
        y='pressure',
        color='is_anomaly_predicted',
        size='wind_speed',
        hover_data=['humidity', 'precipitation', 'anomaly_score'],
        title="Detección de Anomalías: Temperatura vs Presión",
        color_discrete_map={True: 'red', False: 'blue'}
    )
    fig_scatter.update_layout(height=500)
    st.plotly_chart(fig_scatter, use_container_width=True)

    # Gráfico de series temporales
    st.markdown("### 📈 Series Temporales con Anomalías")

    # Seleccionar variable para visualizar
    variable = st.selectbox(
        "Seleccionar Variable:",
        ['temperature', 'humidity', 'pressure', 'wind_speed', 'precipitation']
    )

    fig_time = go.Figure()

    # Datos normales
    normal_data = df_with_anomalies[~df_with_anomalies['is_anomaly_predicted']]
    fig_time.add_trace(go.Scatter(
        x=normal_data['timestamp'],
        y=normal_data[variable],
        mode='markers',
        name='Normal',
        marker=dict(color='blue', size=6)
    ))

    # Datos anómalos
    anomaly_data = df_with_anomalies[df_with_anomalies['is_anomaly_predicted']]
    if not anomaly_data.empty:
        fig_time.add_trace(go.Scatter(
            x=anomaly_data['timestamp'],
            y=anomaly_data[variable],
            mode='markers',
            name='Anomalía',
            marker=dict(color='red', size=10, symbol='x')
        ))

    fig_time.update_layout(
        title=f"Serie Temporal: {variable.title()}",
        xaxis_title="Tiempo",
        yaxis_title=variable.title(),
        height=400
    )

    st.plotly_chart(fig_time, use_container_width=True)

