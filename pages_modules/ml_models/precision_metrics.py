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

@st.cache_data(ttl=1800, show_spinner=False)  # Cache 30 minutos para métricas de precisión
def show_precision_metrics():
    """Mostrar métricas de precisión detalladas de modelos"""

    # Simular datos de precisión histórica
    models_data = {
        "ECMWF": {
            "name": "ECMWF",
            "accuracy_24h": 0.92,
            "accuracy_48h": 0.88,
            "accuracy_72h": 0.84,
            "temperature_rmse": 1.2,
            "pressure_rmse": 2.1,
            "wind_rmse": 3.4,
            "precipitation_skill": 0.78,
            "last_update": datetime.now() - timedelta(hours=6)
        },
        "GFS27": {
            "name": "GFS27",
            "accuracy_24h": 0.88,
            "accuracy_48h": 0.85,
            "accuracy_72h": 0.82,
            "temperature_rmse": 1.5,
            "pressure_rmse": 2.8,
            "wind_rmse": 4.2,
            "precipitation_skill": 0.72,
            "last_update": datetime.now() - timedelta(hours=3)
        },
        "ICON7": {
            "name": "ICON7",
            "accuracy_24h": 0.90,
            "accuracy_48h": 0.87,
            "accuracy_72h": 0.83,
            "temperature_rmse": 1.3,
            "pressure_rmse": 2.3,
            "wind_rmse": 3.8,
            "precipitation_skill": 0.75,
            "last_update": datetime.now() - timedelta(hours=4)
        },
        "HRRR": {
            "name": "HRRR",
            "accuracy_24h": 0.94,
            "accuracy_48h": 0.91,
            "accuracy_72h": 0.87,
            "temperature_rmse": 0.9,
            "pressure_rmse": 1.8,
            "wind_rmse": 2.9,
            "precipitation_skill": 0.82,
            "last_update": datetime.now() - timedelta(hours=1)
        }
    }

    # Métricas principales
    st.markdown("### 📊 Precisión por Horizonte Temporal")

    # Crear DataFrame para gráfico
    accuracy_data = []
    for model_id, model_info in models_data.items():
        accuracy_data.append({
            "Modelo": model_info["name"],
            "24h": model_info["accuracy_24h"] * 100,
            "48h": model_info["accuracy_48h"] * 100,
            "72h": model_info["accuracy_72h"] * 100
        })

    df_accuracy = pd.DataFrame(accuracy_data)

    # Gráfico de precisión temporal con mejoras visuales para pilotos
    fig = go.Figure()

    # Colores y estilos específicos para aviación
    model_styles = {
        "HRRR": {"color": "#FF4444", "symbol": "diamond", "line_style": "solid"},
        "ECMWF": {"color": "#00AA44", "symbol": "circle", "line_style": "solid"},
        "ICON7": {"color": "#0066CC", "symbol": "square", "line_style": "dash"},
        "GFS27": {"color": "#FF8800", "symbol": "triangle-up", "line_style": "dot"}
    }

    for model in df_accuracy["Modelo"]:
        model_data = df_accuracy[df_accuracy["Modelo"] == model]
        style = model_styles.get(
            model,
            {"color": "#666666",
            "symbol": "circle",
            "line_style": "solid"})

        fig.add_trace(go.Scatter(
            x=["24h", "48h", "72h"],
            y=[model_data["24h"].iloc[0], model_data["48h"].iloc[0], model_data["72h"].iloc[0]],
            mode='lines+markers+text',
            name=model,
            line=dict(width=4, color=style["color"], dash=style["line_style"]),
            marker=dict(
                size=12,
                color=style["color"],
                symbol=style["symbol"],
                line=dict(width=2, color="white")
            ),
text = (
                [f"{val:.0f}%" for val in [model_data["24h"].iloc[0], model_data["48h"].iloc[0], model_data["72h"].iloc[0]]],
            )
            textposition="top center",
            textfont=dict(size=10, color=style["color"], family="Arial Black")
        ))

    # Zonas de confianza para interpretación rápida
    fig.add_hrect(
        y0=90,
        y1=100,
        fillcolor="rgba(0,
        255,
        0,
        0.1)",
        layer="below",
        line_width=0,
        annotation_text="🟢 EXCELENTE (>90%)")
    fig.add_hrect(
        y0=80,
        y1=90,
        fillcolor="rgba(255,
        255,
        0,
        0.1)",
        layer="below",
        line_width=0,
        annotation_text="🟡 BUENO (80-90%)")
    fig.add_hrect(
        y0=70,
        y1=80,
        fillcolor="rgba(255,
        165,
        0,
        0.1)",
        layer="below",
        line_width=0,
        annotation_text="🟠 ACEPTABLE (70-80%)")
    fig.add_hrect(
        y0=0,
        y1=70,
        fillcolor="rgba(255,
        0,
        0,
        0.1)",
        layer="below",
        line_width=0,
        annotation_text="🔴 CRÍTICO (<70%)")

    fig.update_layout(
        title=dict(
            text="🎯 PRECISIÓN DE MODELOS METEOROLÓGICOS<br><sub>Para Planificación de Vuelo</sub>",
            font=dict(size=18, family="Arial Black"),
            x=0.5
        ),
        xaxis=dict(
            title=dict(text="HORIZONTE TEMPORAL", font=dict(size=14, family="Arial Black")),
            tickfont=dict(size=12, family="Arial"),
            gridcolor="rgba(128,128,128,0.3)",
            gridwidth=1
        ),
        yaxis=dict(
            title=dict(text="PRECISIÓN (%)", font=dict(size=14, family="Arial Black")),
            tickfont=dict(size=12, family="Arial"),
            range=[60, 100],
            gridcolor="rgba(128,128,128,0.3)",
            gridwidth=1,
            tickmode="linear",
            tick0=60,
            dtick=10
        ),
        height=500,
        hovermode='x unified',
        plot_bgcolor="rgba(248,249,250,0.8)",
        paper_bgcolor="white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=12, family="Arial Black")
        ),
        margin=dict(l=50, r=50, t=100, b=50)
    )

    st.plotly_chart(fig, use_container_width=True)

    # Indicadores visuales rápidos para pilotos
    st.markdown("### 🛩️ Indicadores Rápidos")

    # Crear métricas visuales en tiempo real
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        # Mejor modelo para 24h
        best_24h = df_accuracy.loc[df_accuracy['24h'].idxmax()]
        st.metric(
            label="🏆 MEJOR 24H",
            value=f"{best_24h['Modelo']}",
            delta=f"{best_24h['24h']:.0f}%",
            help="Modelo más preciso para pronósticos de 24 horas"
        )

    with col2:
        # Mejor modelo para 48h
        best_48h = df_accuracy.loc[df_accuracy['48h'].idxmax()]
        st.metric(
            label="🎯 MEJOR 48H",
            value=f"{best_48h['Modelo']}",
            delta=f"{best_48h['48h']:.0f}%",
            help="Modelo más preciso para pronósticos de 48 horas"
        )

    with col3:
        # Degradación promedio
        avg_degradation = df_accuracy.apply(
            lambda row: (row['24h'] - row['72h']) / row['24h'] * 100,
            axis=1).mean()
        st.metric(
            label="📉 DEGRADACIÓN",
            value=f"{avg_degradation:.1f}%",
            delta="por 48h",
            help="Degradación promedio de precisión de 24h a 72h"
        )

    with col4:
        # Confiabilidad general
        overall_confidence = df_accuracy[['24h', '48h', '72h']].mean().mean()
confidence_level = (
            "ALTA" if overall_confidence > 85 else "MEDIA" if overall_confidence > 75 else "BAJA"
        )
        st.metric(
            label="🔍 CONFIABILIDAD",
            value=confidence_level,
            delta=f"{overall_confidence:.0f}%",
            help="Nivel general de confiabilidad de los modelos"
        )

    # Tabla de interpretación rápida
    st.markdown("#### 📋 Guía de Interpretación Rápida")

    interpretation_data = []
    for _, row in df_accuracy.iterrows():
        # Determinar nivel de confianza
        avg_precision = (row['24h'] + row['48h'] + row['72h']) / 3
        if avg_precision >= 90:
            confidence = "🟢 ALTA"
            recommendation = "IDEAL para vuelos críticos"
        elif avg_precision >= 80:
            confidence = "🟡 MEDIA"
            recommendation = "BUENA para planificación general"
        elif avg_precision >= 70:
            confidence = "🟠 BAJA"
            recommendation = "USAR con precaución"
        else:
            confidence = "🔴 CRÍTICA"
            recommendation = "NO RECOMENDADO"

        interpretation_data.append({
            "Modelo": row['Modelo'],
            "24h": f"{row['24h']:.0f}%",
            "48h": f"{row['48h']:.0f}%",
            "72h": f"{row['72h']:.0f}%",
            "Promedio": f"{avg_precision:.0f}%",
            "Confianza": confidence,
            "Recomendación": recommendation
        })

    interpretation_df = pd.DataFrame(interpretation_data)
    st.dataframe(
        interpretation_df,
        use_container_width=True,
        column_config={
            "Modelo": st.column_config.TextColumn("Modelo", width="small"),
            "24h": st.column_config.TextColumn("24h", width="small"),
            "48h": st.column_config.TextColumn("48h", width="small"),
            "72h": st.column_config.TextColumn("72h", width="small"),
            "Promedio": st.column_config.TextColumn("Promedio", width="small"),
            "Confianza": st.column_config.TextColumn("Confianza", width="medium"),
            "Recomendación": st.column_config.TextColumn("Recomendación", width="large")
        }
    )

    # Estado de actualización integrado
    st.markdown("#### 🔄 Estado de Actualización de Modelos")

    # Crear columnas para mostrar estado de actualización
    update_cols = st.columns(4)

    for i, (model_id, model_info) in enumerate(models_data.items()):
        with update_cols[i]:
            last_update = model_info['last_update']
            hours_ago = (datetime.now() - last_update).total_seconds() / 3600

            if hours_ago < 6:
                status = "🟢 Actualizado"
                status_color = "success"
            elif hours_ago < 12:
                status = "🟡 Moderado"
                status_color = "warning"
            else:
                status = "🔴 Desactualizado"
                status_color = "error"

            # Mostrar métrica de estado
            st.metric(
                label=f"🔄 {model_info['name']}",
                value=status,
                delta=f"{hours_ago:.1f}h",
                help=f"Última actualización: {last_update.strftime('%H:%M')}"
            )

    # Resumen de estado general
    st.markdown("##### 📊 Resumen de Estado General")

    # Calcular estadísticas de actualización
    total_models = len(models_data)
    updated_models = sum(1 for model_info in models_data.values()
                        if (datetime.now() - model_info['last_update']).total_seconds() / 3600 < 6)
    moderate_models = sum(1 for model_info in models_data.values()
                         if 6 <= (datetime.now() - model_info['last_update']).total_seconds() / 3600 < 12)
    outdated_models = total_models - updated_models - moderate_models

    # Mostrar estadísticas en columnas
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

    with stat_col1:
        st.metric("🟢 Actualizados", updated_models, f"{updated_models/total_models*100:.0f}%")

    with stat_col2:
        st.metric("🟡 Moderados", moderate_models, f"{moderate_models/total_models*100:.0f}%")

    with stat_col3:
        st.metric("🔴 Desactualizados", outdated_models, f"{outdated_models/total_models*100:.0f}%")

    with stat_col4:
        avg_age = sum((datetime.now() - model_info['last_update']).total_seconds() / 3600
                     for model_info in models_data.values()) / total_models
        st.metric("⏱️ Edad Promedio", f"{avg_age:.1f}h", "de los datos")

    # Alertas para pilotos
    if outdated_models > 0:
        st.warning(f"⚠️ **ALERTA**: {outdated_models} modelo(s) desactualizado(s). Considera usar datos más frescos.")

    if updated_models == total_models:
        st.success("✅ **EXCELENTE**: Todos los modelos están actualizados. Datos óptimos para planificación de vuelo.")
    elif updated_models >= total_models * 0.75:
        st.info("ℹ️ **BUENO**: La mayoría de modelos están actualizados. Datos confiables para planificación.")

    # Recomendaciones basadas en precisión
    st.markdown("### 💡 Recomendaciones de Uso por Precisión")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.info("""
        **🌍 ECMWF**
        - Mejor para: Precipitaciones
        - Precisión: 92% (24h)
        - Ideal: Pronósticos globales
        """)

    with col2:
        st.success("""
        **🇺🇸 HRRR**
        - Mejor para: Alta resolución
        - Precisión: 94% (24h)
        - Ideal: Estados Unidos
        """)

    with col3:
        st.warning("""
        **🇪🇺 ICON7**
        - Mejor para: Europa
        - Precisión: 90% (24h)
        - Ideal: Regiones específicas
        """)

    with col4:
        st.info("""
        **🌐 GFS27**
        - Mejor para: Largo plazo
        - Precisión: 88% (24h)
        - Ideal: Análisis global
        """)

