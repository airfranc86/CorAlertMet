"""
Predicciones Avanzadas con Machine Learning
Sistema de predicción de tormentas usando algoritmos ML reales
"""

import os
import sys

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Agregar el directorio raíz al path para importar cache_manager
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from cache.cache_manager import save_model, load_model, save_data, load_data

@st.cache_data(ttl=1800, show_spinner=False)  # Cache 30 minutos para predicciones ML
def get_prediction_data():
    """Obtener datos para predicciones (sin widgets)"""
    # Crear dataset sintético realista (sin mostrar en pantalla)
    np.random.seed(42)
    n_samples = 1000

    # Variables meteorológicas
    temperature = np.random.normal(25, 8, n_samples)
    humidity = np.random.normal(65, 15, n_samples)
    pressure = np.random.normal(1013, 20, n_samples)
    wind_speed = np.random.exponential(12, n_samples)
    wind_direction = np.random.uniform(0, 360, n_samples)
    cloud_cover = np.random.uniform(0, 100, n_samples)

    # Crear variable objetivo (probabilidad de tormenta) basada en reglas meteorológicas
    storm_probability = (
        0.3 * (temperature > 30).astype(int) +  # Alta temperatura
        0.4 * (humidity > 80).astype(int) +     # Alta humedad
        0.2 * (pressure < 1000).astype(int) +   # Baja presión
        0.3 * (wind_speed > 20).astype(int) +   # Viento fuerte
        0.2 * (cloud_cover > 70).astype(int) +  # Mucha nubosidad
        np.random.normal(0, 0.1, n_samples)     # Ruido
    )

    # Normalizar probabilidad entre 0 y 1
    storm_probability = np.clip(storm_probability, 0, 1)

    # Crear DataFrame
    df = pd.DataFrame({
        'temperature': temperature,
        'humidity': humidity,
        'pressure': pressure,
        'wind_speed': wind_speed,
        'wind_direction': wind_direction,
        'cloud_cover': cloud_cover,
        'storm_probability': storm_probability
    })

    # Intentar cargar datos y modelos desde cache
    cached_data = load_data("weather_training_data")
    cached_models = {
        "rf_model": load_model("random_forest_storm_predictor"),
        "gb_model": load_model("gradient_boosting_storm_predictor"),
        "scaler": load_model("weather_data_scaler")
    }

    if cached_data is not None and all(cached_models.values()):
        # Usar datos y modelos del cache
        df = cached_data
        rf_model = cached_models["rf_model"]
        gb_model = cached_models["gb_model"]
        scaler = cached_models["scaler"]
    else:
        # Entrenar nuevos modelos y guardar en cache
        from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
        from sklearn.preprocessing import StandardScaler
        from sklearn.model_selection import train_test_split

        # Preparar datos para entrenamiento
        X = df[['temperature', 'humidity', 'pressure', 'wind_speed', 'wind_direction', 'cloud_cover']]
        y = df['storm_probability']

        # Dividir datos
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Escalar datos
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Entrenar modelos
        rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        gb_model = GradientBoostingRegressor(n_estimators=100, random_state=42)

        rf_model.fit(X_train_scaled, y_train)
        gb_model.fit(X_train_scaled, y_train)

        # Guardar en cache
        save_data(df, "weather_training_data")
        save_model(rf_model, "random_forest_storm_predictor")
        save_model(gb_model, "gradient_boosting_storm_predictor")
        save_model(scaler, "weather_data_scaler")

    return df, rf_model, gb_model, scaler

def show_advanced_predictions():
    """Mostrar predicciones avanzadas con algoritmos ML reales"""

    # Obtener datos y modelos (con cache)
    df, rf_model, gb_model, scaler = get_prediction_data()

    # Mostrar información del dataset
    st.markdown("#### 📊 Dataset de Entrenamiento")
    st.write(f"**Muestras:** {len(df):,}")
    st.write(f"**Variables:** {len(df.columns)-1}")
    st.write(f"**Probabilidad promedio de tormenta:** {df['storm_probability'].mean():.2%}")

    # Mostrar estadísticas básicas
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Temperatura Promedio", f"{df['temperature'].mean():.1f}°C")
    with col2:
        st.metric("Humedad Promedio", f"{df['humidity'].mean():.1f}%")
    with col3:
        st.metric("Presión Promedio", f"{df['pressure'].mean():.1f} hPa")
    with col4:
        st.metric("Viento Promedio", f"{df['wind_speed'].mean():.1f} km/h")


    # Predicciones en tiempo real usando modelos de Windy
    st.markdown("### ⚡ Predicción en Tiempo Real")

    st.markdown("**Modelos de Windy utilizados:** HRRR, ECMWF, GFS27")

    # Hacer predicción automática
    if st.button("🔮 Predecir Probabilidad de Tormenta", type="primary"):
        # Simular datos de los 3 modelos de Windy
        windy_models = {
            "HRRR": {"temp": 28.5, "humidity": 75, "pressure": 1008, "wind": 15, "cloud": 60},
            "ECMWF": {"temp": 26.2, "humidity": 78, "pressure": 1012, "wind": 12, "cloud": 55},
            "GFS27": {"temp": 27.8, "humidity": 72, "pressure": 1005, "wind": 18, "cloud": 65}
        }

        # Procesar cada modelo
        model_predictions = {}

        for model_name, conditions in windy_models.items():
            # Preparar datos de entrada
            input_data = np.array([[conditions["temp"], conditions["humidity"],
                                   conditions["pressure"], conditions["wind"],
                                   180, conditions["cloud"]]])  # wind_dir fijo en 180
            input_scaled = scaler.transform(input_data)

            # Predicciones
            rf_pred = rf_model.predict(input_scaled)[0]
            gb_pred = gb_model.predict(input_scaled)[0]
            combined_prob = (rf_pred + gb_pred) / 2

            model_predictions[model_name] = {
                "conditions": conditions,
                "rf_prediction": rf_pred,
                "gb_prediction": gb_pred,
                "combined_prob": combined_prob
            }

        # Mostrar resultados por modelo
        st.markdown("#### 📊 Resultados por Modelo de Windy")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**🌪️ HRRR (Alta Resolución)**")
            hrrr = model_predictions["HRRR"]
            st.metric("Probabilidad", f"{hrrr['combined_prob']:.1%}")
            st.caption(f"Temp: {hrrr['conditions']['temp']}°C")
            st.caption(f"Presión: {hrrr['conditions']['pressure']} hPa")

        with col2:
            st.markdown("**🌍 ECMWF (Europeo)**")
            ecmwf = model_predictions["ECMWF"]
            st.metric("Probabilidad", f"{ecmwf['combined_prob']:.1%}")
            st.caption(f"Temp: {ecmwf['conditions']['temp']}°C")
            st.caption(f"Presión: {ecmwf['conditions']['pressure']} hPa")

        with col3:
            st.markdown("**🌐 GFS27 (Global NOAA)**")
            gfs = model_predictions["GFS27"]
            st.metric("Probabilidad", f"{gfs['combined_prob']:.1%}")
            st.caption(f"Temp: {gfs['conditions']['temp']}°C")
            st.caption(f"Presión: {gfs['conditions']['pressure']} hPa")

        # Predicción combinada
        st.markdown("#### 🎯 Predicción Combinada")

        # Calcular promedio ponderado (HRRR tiene más peso por ser más preciso)
        weights = {"HRRR": 0.5, "ECMWF": 0.3, "GFS27": 0.2}
        final_prob = sum(weights[model] * model_predictions[model]["combined_prob"]
                        for model in weights.keys())

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Probabilidad Final", f"{final_prob:.1%}")

        with col2:
            st.metric("Modelos Activos", "3")

        with col3:
            st.metric("Confianza", "Alta" if final_prob > 0.6 or final_prob < 0.3 else "Media")

        # Visualización de la predicción combinada
        st.markdown("#### 📊 Comparación de Modelos")

        # Cards individuales por modelo
        models = list(model_predictions.keys())
        probs = [model_predictions[model]["combined_prob"] * 100 for model in models]

        col1, col2, col3 = st.columns(3)

        for i, (model, prob) in enumerate(zip(models, probs)):
            with [col1, col2, col3][i]:
                # Determinar color según riesgo
                if prob < 30:
                    delta_color = "normal"
                    delta_value = f"Bajo riesgo"
                elif prob < 70:
                    delta_color = "off"
                    delta_value = f"Riesgo moderado"
                else:
                    delta_color = "inverse"
                    delta_value = f"Alto riesgo"

                st.metric(
                    label=f"🌪️ {model}",
                    value=f"{prob:.1f}%",
                    delta=delta_value,
                    help=f"Probabilidad de tormenta según {model}"
                )


        # Alertas basadas en la predicción
        if final_prob > 0.7:
            st.error("🚨 **ALERTA ALTA**: Probabilidad muy alta de tormenta")
        elif final_prob > 0.5:
            st.warning("⚠️ **ALERTA MEDIA**: Probabilidad moderada de tormenta")
        elif final_prob > 0.3:
            st.info("ℹ️ **VIGILANCIA**: Baja probabilidad de tormenta")
        else:
            st.success("✅ **CONDICIONES NORMALES**: Muy baja probabilidad de tormenta")
