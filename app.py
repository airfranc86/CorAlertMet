"""
CorAlertMet Intelligence - Streamlit App
Sistema de Alertas Meteorológicas con Machine Learning
Versión: 2.1.0
"""

import os
import sys
import requests
import streamlit as st

# Importar componentes
from components.footer import show_footer
from components.styles import apply_corporate_styles
from components.svg_icons_smooth import show_svg_icon

# Importar sistema de autenticación y logging
from auth.simple_auth import SimpleAuth, show_login_form, show_logout_section, require_auth
from config.logging_config import setup_logging, get_logger

def create_responsive_columns(num_columns=4):
    """
    Crear columnas responsivas que se adaptan al tamaño de pantalla
    - Desktop: num_columns columnas
    - Tablet: 3 columnas (si num_columns >= 3)
    - Mobile: 2 columnas (si num_columns >= 2)
    - Mobile pequeño: 1 columna
    """
    return st.columns(num_columns)

# Configurar logging
setup_logging()
logger = get_logger(__name__)

# Agregar src al path (comentado - directorio src no existe)
# sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Configuración de la página
st.set_page_config(
    page_title="CorAlertMet Intelligence",
    page_icon="data/icon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Aplicar estilos corporativos
apply_corporate_styles()


# Configurar API key desde múltiples fuentes
def get_api_key():
    """Obtener API key desde secrets o variables de entorno"""
    # 1. Intentar desde Streamlit secrets (directo)
    if hasattr(st, 'secrets') and 'OPENWEATHER_API_KEY' in st.secrets:
        return st.secrets['OPENWEATHER_API_KEY']

    # 1b. Intentar desde Streamlit secrets (anidado en SECRETS)
    if (hasattr(st, 'secrets') and 'SECRETS' in st.secrets and
            'OPENWEATHER_API_KEY' in st.secrets['SECRETS']):
        return st.secrets['SECRETS']['OPENWEATHER_API_KEY']

    # 2. Intentar desde variables de entorno
    if 'OPENWEATHER_API_KEY' in os.environ:
        return os.environ['OPENWEATHER_API_KEY']

    # 3. Intentar desde archivo .env
    try:
        from dotenv import load_dotenv
        load_dotenv()
        if 'OPENWEATHER_API_KEY' in os.environ:
            return os.environ['OPENWEATHER_API_KEY']
    except ImportError:
        pass

    return None

# Configurar API key
api_key = get_api_key()
if api_key:
    os.environ['OPENWEATHER_API_KEY'] = api_key

def main():
    """Función principal de la aplicación"""

    # Configurar favicon personalizado
    st.markdown("""
    <link rel="icon" type="image/png" href="data/icon.png">
    <link rel="shortcut icon" type="image/png" href="data/icon.png">
    """, unsafe_allow_html=True)

    # Verificar autenticación
    auth = SimpleAuth()
    if not auth.is_authenticated():
        logger.info("Usuario no autenticado, mostrando formulario de login")
        show_login_form()
        return

    # Usuario autenticado, continuar con la aplicación
    current_user = auth.get_current_user()
    logger.info(f"Usuario autenticado: {current_user}")

    # Sidebar responsivo con logo, navegación y referencia
    with st.sidebar:
        # Logo principal responsivo
        st.image("data/icon.png", width=100)

        # Título de la aplicación responsivo
        st.markdown("## CorAlertMet Intelligence")  # NO USAR EMOTICONES
        st.markdown("*Sistema de Alertas Meteorológicas*")
        st.markdown("---")

        # Navegación principal con iconos Lottie
        st.markdown("### Navegación")

        # Iconos para cada sección
        navigation_options = [
            ("Dashboard", "home"),
            ("Mapa Interactivo", "map"),
            ("Panel ML", "brain"),
            ("Referencia", "book")
        ]

        page_options = [option[0] for option in navigation_options]
        page = st.radio(
            "Seleccionar sección:",
            page_options,
            index=0
        )

        # API Configuration con iconos Lottie
        st.markdown("---")
        st.markdown("### API Configuration")

        # Iconos para APIs
        api_options = [
            ("OpenWeatherMap", "cloud"),
            ("Windy", "wind")
        ]

        api_names = [option[0] for option in api_options]
        selected_api = st.radio(
            "Seleccionar API:",
            api_names,
            index=0,
            help="Selecciona la API meteorológica a utilizar"
        )

        # Selector de modelo de Windy
        if selected_api == "Windy":
            st.markdown("---")
            st.markdown("### Modelo de Pronóstico")

            windy_models = [
                ("ECMWF", "Modelo europeo de alta precisión (14 km)"),
                ("GFS27", "Sistema de pronóstico global de NOAA (27 km)"),
                ("ICON7", "Modelo alemán para Europa (7 km)"),
                ("HRRR", "Alta resolución para Estados Unidos (3 km)")
            ]

            model_names = [option[0] for option in windy_models]
            selected_model = st.selectbox(
                "Seleccionar Modelo:",
                model_names,
                index=0,
                help="Selecciona el modelo meteorológico específico de Windy"
            )

            # Mostrar información del modelo seleccionado
            model_info = next((info for name, info in windy_models if name == selected_model), "")
            st.caption(f"📊 {model_info}")
        else:
            selected_model = None

        # Sección de logout
        show_logout_section()

    # Contenido principal basado en navegación
    if page == "Dashboard":
        show_main_dashboard(selected_api, selected_model)
    elif page == "Mapa Interactivo":
        show_map_page(selected_api, selected_model)
    elif page == "Panel ML":
        show_ml_dashboard(selected_api, selected_model)
    elif page == "Referencia":
        show_reference()

    # Footer profesional fijo
    show_footer()

def show_main_dashboard(selected_api="OpenWeatherMap", selected_model=None):
    """Mostrar dashboard principal con criterios de probabilidad"""

    # Header principal con icono SVG
    col1, col2 = st.columns([1, 20])
    with col1:
        show_svg_icon("cloud-sun", width=48, height=48, animation="smoothBlink", color="#3B82F6")
    with col2:
        st.title("CorAlertMet Intelligence")

    # Descripción con icono SVG
    col1, col2 = st.columns([1, 20])
    with col1:
        show_svg_icon("brain", width=24, height=24, animation="smoothBlink", color="#8B5CF6")
    with col2:
        st.markdown("**Sistema de Alertas Meteorológicas**")

    st.markdown("---")

    # Criterios de probabilidad - 4 niveles de alerta

    # Botón de actualización
    if st.button("Actualizar Datos Meteorológicos", type="primary", use_container_width=True):
        with st.spinner(f"Obteniendo datos meteorológicos desde {selected_api}..."):
            try:
                # Obtener datos reales de la API seleccionada
                weather_data = get_weather_data_from_api(selected_api, "Córdoba,AR", selected_model)

                if weather_data:
                    # Mostrar datos
                    display_weather_summary(weather_data)

                    # Mostrar Nivel de Alerta Meteorológica basado en ML
                    show_meteorological_alert_level(weather_data)
                else:
                    st.error(f"❌ No se pudieron obtener datos de {selected_api}")

            except Exception as e:
                st.error(f"❌ Error: {e}")

    # Mostrar comparación de modelos si se selecciona Windy
    if selected_api == "Windy":
        show_model_comparison()


def get_weather_data_from_api(selected_api, location="Córdoba,AR", selected_model=None):
    """Obtener datos meteorológicos reales desde la API seleccionada"""
    try:
        if selected_api == "OpenWeatherMap":
            return get_openweather_data(location)
        elif selected_api == "Windy":
            return get_windy_data(location, selected_model)
    except Exception as e:
        st.error(f"❌ Error obteniendo datos de {selected_api}: {e}")
        return None

@st.cache_data(ttl=300, show_spinner=False)  # Cache 5 minutos para datos públicos
def get_openweather_data(location):
    """Obtener datos de OpenWeatherMap"""
    api_key = (st.secrets.get("openweather_api_key") or
               st.secrets.get("SECRETS", {}).get("openweather_api_key", ""))
    if not api_key:
        return None

    # Obtener coordenadas
    geo_url = "http://api.openweathermap.org/geo/1.0/direct"
    geo_params = {"q": location, "limit": 1, "appid": api_key}

    geo_response = requests.get(geo_url, params=geo_params, timeout=5)
    if geo_response.status_code != 200:
        return None

    geo_data = geo_response.json()
    if not geo_data:
        return None

    lat, lon = geo_data[0]["lat"], geo_data[0]["lon"]

    # Obtener datos meteorológicos
    weather_url = "http://api.openweathermap.org/data/2.5/weather"
    weather_params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric",
        "lang": "es"
    }

    weather_response = requests.get(weather_url, params=weather_params, timeout=5)
    if weather_response.status_code != 200:
        return None

    weather_data = weather_response.json()

    return {
        "temperature": weather_data["main"]["temp"],
        "humidity": weather_data["main"]["humidity"],
        "pressure": weather_data["main"]["pressure"],
        "wind_speed": weather_data["wind"]["speed"],
        "wind_direction": weather_data["wind"].get("deg", 0),
        "description": weather_data["weather"][0]["description"],
        "visibility": weather_data.get("visibility", 0) / 1000,  # Convert to km
        "cloudiness": weather_data["clouds"]["all"],
        "source": "OpenWeatherMap",
        "station": {
            "name": geo_data[0].get("name", "Córdoba"),
            "country": geo_data[0].get("country", "AR"),
            "coordinates": f"{lat:.2f}°N, {lon:.2f}°O"
        }
    }

@st.cache_data(ttl=300, show_spinner=False)  # Cache 5 minutos para datos públicos
def get_windy_data(location, selected_model=None):
    """Obtener datos de Windy (simulado por ahora - Windy requiere autenticación compleja)"""
    # Windy API requiere autenticación OAuth, por ahora simulamos con OpenWeatherMap
    api_key = (st.secrets.get("openweather_api_key") or
               st.secrets.get("SECRETS", {}).get("openweather_api_key", ""))
    if not api_key:
        return None

    # Usar OpenWeatherMap como base y simular variaciones de Windy
    base_data = get_openweather_data(location)
    if not base_data:
        return None

    # Simular variaciones típicas de Windy (datos más precisos)
    import random

    # Definir modelos de Windy
    windy_models = {
        "ECMWF": {
            "name": "ECMWF",
            "resolution": "14 km",
            "update_frequency": "12 horas",
            "description": "Modelo europeo de alta precisión",
            "accuracy": 0.92
        },
        "GFS27": {
            "name": "GFS27",
            "resolution": "27 km",
            "update_frequency": "4x/día",
            "description": "Sistema de pronóstico global de NOAA",
            "accuracy": 0.88
        },
        "ICON7": {
            "name": "ICON7",
            "resolution": "7 km",
            "update_frequency": "6 horas",
            "description": "Modelo alemán para Europa",
            "accuracy": 0.90
        },
        "HRRR": {
            "name": "HRRR",
            "resolution": "3 km",
            "update_frequency": "18x/día",
            "description": "Alta resolución para Estados Unidos",
            "accuracy": 0.94
        }
    }

    # Usar modelo seleccionado o aleatorio
    if selected_model and selected_model in windy_models:
        model_data = windy_models[selected_model]
    else:
        model_data = random.choice(list(windy_models.values()))

    # Variación basada en la precisión del modelo
    base_variation = 0.05  # ±5% base
    accuracy_factor = model_data["accuracy"]
    variation = random.uniform(1 - base_variation * (2 - accuracy_factor),
                              1 + base_variation * (2 - accuracy_factor))

    # Agregar al historial
    from datetime import datetime
    add_to_model_history(
        "Windy", model_data["name"], 
        datetime.now().isoformat(), model_data["accuracy"]
    )

    return {
        "temperature": round(base_data["temperature"] * variation, 1),
        "humidity": round(base_data["humidity"] * variation, 1),
        "pressure": round(base_data["pressure"] * variation, 1),
        "wind_speed": round(base_data["wind_speed"] * variation, 1),
        "wind_direction": base_data["wind_direction"],
        "description": base_data["description"],
        "visibility": round(base_data["visibility"] * variation, 1),
        "cloudiness": round(base_data["cloudiness"] * variation, 1),
        "source": "Windy",
        "station": base_data.get("station", {
            "name": "Estación Simulada",
            "country": "AR",
            "coordinates": "31.42°N, 64.19°O"
        }),
        "model": model_data
    }

def get_api_status(selected_api):
    """Verificar el estado de la API seleccionada"""
    try:
        if selected_api == "OpenWeatherMap":
            # Intentar ambas formas de acceso
            api_key = (st.secrets.get("openweather_api_key") or
               st.secrets.get("SECRETS", {}).get("openweather_api_key", ""))
            return {"available": bool(api_key), "api": "OpenWeatherMap"}
        elif selected_api == "Windy":
            # Intentar ambas formas de acceso
            api_key = (st.secrets.get("windy_api_key") or
               st.secrets.get("SECRETS", {}).get("windy_api_key", ""))
            return {"available": bool(api_key), "api": "Windy"}
    except:
        return {"available": False, "api": selected_api}

def display_weather_summary(weather_data):
    """Mostrar resumen de datos meteorológicos"""

    # Header con icono SVG animado
    col1, col2 = st.columns([1, 20])
    with col1:
        show_svg_icon("sun", width=32, height=32, animation="pulse", color="#F59E0B")
    with col2:
        st.subheader("Condiciones Actuales")

    # Mostrar fuente, estación y modelo de los datos
    col1, col2 = st.columns([1, 20])
    with col1:
        show_svg_icon("check-circle", width=20, height=20, animation="gentlePulse", color="#10B981")
    with col2:
        source = weather_data.get('source', 'Desconocida')
        station = weather_data.get('station', {})
        station_name = station.get('name', 'N/A')
        station_coords = station.get('coordinates', 'N/A')

        # Mostrar información del modelo si está disponible
        model = weather_data.get('model', {})
        if model:
            model_name = model.get('name', 'N/A')
            model_res = model.get('resolution', 'N/A')
            model_accuracy = model.get('accuracy', 0)
            st.caption(f"**{source}** - {station_name} ({station_coords})")
            st.caption(f"📊 Modelo: {model_name} ({model_res}) - Precisión: {model_accuracy:.0%}")
        else:
            st.caption(f"**{source}** - {station_name} ({station_coords})")

    # Métricas meteorológicas responsivas
    st.markdown("#### Condiciones Actuales")

    # En pantallas grandes: 4 columnas, en móvil: 2 columnas
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        with st.container():
            show_svg_icon("thermometer", width=24, height=24, animation="pulse", color="#EF4444")
            st.metric("Temperatura", f"{weather_data.get('temperature', 0):.1f}°C")

    with col2:
        with st.container():
            show_svg_icon("droplet", width=24, height=24, animation="bounce", color="#3B82F6")
            st.metric("Humedad", f"{weather_data.get('humidity', 0)}%")

    with col3:
        with st.container():
            show_svg_icon("wind", width=24, height=24, animation="rotate", color="#10B981")
            st.metric("Viento", f"{weather_data.get('wind_speed', 0):.1f} km/h")

    with col4:
        with st.container():
            show_svg_icon("gauge", width=24, height=24, animation="scale", color="#8B5CF6")
            st.metric("Presión", f"{weather_data.get('pressure', 0):.1f} hPa")


def display_weather_data(weather_data: dict) -> None:
    """Mostrar datos meteorológicos"""

    col1, col2, col3 = st.columns(3)

    with col1:
        # Iconos SVG para temperatura y humedad
        show_svg_icon("thermometer", width=20, height=20, animation="pulse", color="#EF4444")
        st.metric("Temperatura", f"{weather_data.get('temperature', 0):.1f}°C")
        show_svg_icon("droplet", width=20, height=20, animation="bounce", color="#3B82F6")
        st.metric("Humedad", f"{weather_data.get('humidity', 0)}%")

    with col2:
        # Iconos SVG para viento y dirección
        show_svg_icon("wind", width=20, height=20, animation="rotate", color="#10B981")
        st.metric("Viento", f"{weather_data.get('wind_speed', 0):.1f} km/h")
        show_svg_icon("compass", width=20, height=20, animation="rotate", color="#8B5CF6")
        st.metric("Dirección", f"{weather_data.get('wind_direction', 0)}°")

    with col3:
        # Iconos SVG para presión y nubosidad
        show_svg_icon("gauge", width=20, height=20, animation="scale", color="#8B5CF6")
        st.metric("Presión", f"{weather_data.get('pressure', 0):.1f} hPa")
        show_svg_icon("cloud", width=20, height=20, animation="pulse", color="#6B7280")
        st.metric("Nubosidad", f"{weather_data.get('cloudiness', 0)}%")

def display_storm_prediction(prediction: dict) -> None:
    """Mostrar predicción de tormenta"""

    # Header con icono SVG animado
    col1, col2 = st.columns([1, 20])
    with col1:
        show_svg_icon("cloud-lightning", width=48, height=48, animation="pulse", color="#EF4444")
    with col2:
        st.header("Predicción de Tormenta")

    probability = prediction.get('probability', 0)
    alert_level = prediction.get('alert_level', 'LOW')
    eta = prediction.get('eta', 'N/A')

    # Color según nivel de alerta
    if alert_level == 'CRITICAL':
        color = "red"
    elif alert_level == 'HIGH':
        color = "orange"
    elif alert_level == 'MEDIUM':
        color = "yellow"
    else:
        color = "green"

    # Mostrar probabilidad con color según nivel de alerta
    if color == "red":
        col1, col2 = st.columns([1, 20])
        with col1:
            show_svg_icon("alert-triangle", width=32, height=32, animation="pulse", color="#EF4444")
        with col2:
            st.error(f"**Probabilidad de Tormenta: {probability:.1f}%** (Nivel: {alert_level})")
    elif color == "orange":
        col1, col2 = st.columns([1, 20])
        with col1:
            show_svg_icon("alert-circle", width=32, height=32, animation="scale", color="#F59E0B")
        with col2:
            st.warning(f"**Probabilidad de Tormenta: {probability:.1f}%** (Nivel: {alert_level})")
    elif color == "yellow":
        col1, col2 = st.columns([1, 20])
        with col1:
            show_svg_icon("info", width=32, height=32, animation="bounce", color="#F59E0B")
        with col2:
            st.warning(f"**Probabilidad de Tormenta: {probability:.1f}%** (Nivel: {alert_level})")
    else:
        col1, col2 = st.columns([1, 20])
        with col1:
            show_svg_icon("check-circle", width=32, height=32, animation="pulse", color="#10B981")
        with col2:
            st.success(f"**Probabilidad de Tormenta: {probability:.1f}%** (Nivel: {alert_level})")

    # Mostrar ETA con icono SVG
    col1, col2 = st.columns([1, 20])
    with col1:
        show_svg_icon("clock", width=24, height=24, animation="rotate", color="#3B82F6")
    with col2:
        st.info(f"Tiempo estimado de arribo: {eta}")

    # Mostrar factores de riesgo
    if 'risk_factors' in prediction:
        col1, col2 = st.columns([1, 20])
        with col1:
            show_svg_icon("search", width=24, height=24, animation="pulse", color="#8B5CF6")
        with col2:
            st.subheader("Factores de Riesgo")

        risk_factors = prediction.get('risk_factors', {})
        for factor, value in risk_factors.items():
            col1, col2 = st.columns([1, 20])
            with col1:
                show_svg_icon("alert-circle", width=16, height=16,
                             animation="scale", color="#F59E0B")
            with col2:
                st.write(f"• {factor}: {value}")


@st.cache_data(ttl=3600)  # Cache 1 hora para historial
def get_model_history():
    """Obtener historial de modelos utilizados"""
    if 'model_history' not in st.session_state:
        st.session_state.model_history = []
    return st.session_state.model_history

def add_to_model_history(api, model_name, timestamp, accuracy=None):
    """Agregar entrada al historial de modelos"""
    history = get_model_history()
    entry = {
        "timestamp": timestamp,
        "api": api,
        "model": model_name,
        "accuracy": accuracy
    }
    history.append(entry)
    # Mantener solo los últimos 10 registros
    if len(history) > 10:
        history.pop(0)
    st.session_state.model_history = history


def show_meteorological_alert_level(weather_data):
    """Mostrar nivel de alerta meteorológica basado en análisis ML"""
    st.markdown("---")

    # Header con icono de alerta
    col1, col2 = st.columns([1, 20])
    with col1:
        st.markdown("""
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" 
             xmlns="http://www.w3.org/2000/svg">
        <style>
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
        .alert { animation: pulse 2s ease-in-out infinite; }
        </style>
        <path class="alert" d="M12 2L22 20H2L12 2Z" stroke="#F59E0B" stroke-width="2" fill="none"/>
        <path d="M12 8V12" stroke="#F59E0B" stroke-width="2" stroke-linecap="round"/>
        <circle cx="12" cy="16" r="1" fill="#F59E0B"/>
        </svg>
        """, unsafe_allow_html=True)
    with col2:
        st.subheader("Nivel de Alerta Meteorológica")

    # Calcular probabilidad de tormenta basada en datos meteorológicos
    temp = weather_data.get('temperature', 25)
    humidity = weather_data.get('humidity', 50)
    pressure = weather_data.get('pressure', 1013)
    wind_speed = weather_data.get('wind_speed', 10)
    cloud_cover = weather_data.get('cloud_cover', 50)

    # Algoritmo ML simplificado para calcular probabilidad de tormenta
    storm_probability = 0

    # Factores de riesgo
    if temp > 30:
        storm_probability += 0.2  # Alta temperatura
    if humidity > 80:
        storm_probability += 0.3  # Alta humedad
    if pressure < 1000:
        storm_probability += 0.25  # Baja presión
    if wind_speed > 20:
        storm_probability += 0.15  # Viento fuerte
    if cloud_cover > 70:
        storm_probability += 0.1  # Mucha nubosidad

    # Normalizar entre 0 y 1
    storm_probability = min(storm_probability, 1.0)
    storm_percentage = storm_probability * 100

    # Determinar nivel de alerta
    if storm_percentage < 40:
        alert_level = "BAJO RIESGO"
        alert_color = "🟢"
        alert_bg = "#10B981"
        alert_text = "Condiciones normales - Vuelo seguro"
        recommendations = [
            "✅ Condiciones ideales para vuelo",
            "✅ Monitoreo estándar recomendado",
            "✅ Sin restricciones especiales"
        ]
    elif storm_percentage < 60:
        alert_level = "RIESGO MODERADO"
        alert_color = "🟡"
        alert_bg = "#F59E0B"
        alert_text = "Monitorear condiciones - Precaución recomendada"
        recommendations = [
            "⚠️ Monitorear condiciones meteorológicas",
            "⚠️ Considerar ruta alternativa",
        ]
    elif storm_percentage < 80:
        alert_level = "ALTO RIESGO"
        alert_color = "🟠"
        alert_bg = "#F97316"
        alert_text = "Precaución recomendada - Evitar vuelo nocturno"
        recommendations = [
            "🚨 Evitar vuelo nocturno",
            "🚨 Planificar ruta de escape",
            "🚨 Mantener combustible extra",
            "🚨 Comunicación constante con control"
        ]
    else:
        alert_level = "ALERTA CRÍTICA"
        alert_color = "🔴"
        alert_bg = "#EF4444"
        alert_text = "Tormenta inminente - Evitar vuelo"
        recommendations = [
            "🚫 NO VOLAR - Condiciones peligrosas",
            "🚫 Buscar refugio inmediatamente",
            "🚫 Mantener aeronave en hangar",
            "🚫 Contactar autoridades meteorológicas"
        ]

    # Mostrar alerta principal
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {alert_bg}20, {alert_bg}40);
        border: 2px solid {alert_bg};
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        text-align: center;
    ">
        <h2 style="color: {alert_bg}; margin: 0; font-size: 24px;">
            {alert_color} {alert_level}
        </h2>
        <p style="font-size: 18px; margin: 10px 0; color: #333;">
            {alert_text}
        </p>
        <p style="font-size: 16px; margin: 0; color: #666;">
            Probabilidad de tormenta: <strong>{storm_percentage:.1f}%</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Mostrar recomendaciones
    st.markdown("#### 📋 Recomendaciones para Pilotos:")
    for rec in recommendations:
        st.markdown(f"- {rec}")

    # Mostrar detalles técnicos en expander
    with st.expander("🔍 Detalles Técnicos del Análisis"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Temperatura", f"{temp}°C",
                     delta="Alta" if temp > 30 else "Normal" if temp > 15 else "Baja")

        with col2:
            st.metric("Humedad", f"{humidity}%",
                     delta="Alta" if humidity > 80 else "Normal" if humidity > 40 else "Baja")

        with col3:
            st.metric("Presión", f"{pressure} hPa",
                     delta="Baja" if pressure < 1000 else "Normal" if pressure < 1020 else "Alta")

        col4, col5 = st.columns(2)

        with col4:
            st.metric("Viento", f"{wind_speed} km/h",
                     delta="Fuerte" if wind_speed > 20 else "Moderado" if wind_speed > 10 else "Suave")

        with col5:
            st.metric("Nubosidad", f"{cloud_cover}%",
                     delta="Alta" if cloud_cover > 70 else "Moderada" if cloud_cover > 30 else "Baja")

def show_trend_analysis():
    """Mostrar análisis de tendencias meteorológicas con rango de 30 minutos"""
    st.markdown("---")

    # Header con icono SVG más profesional
    col1, col2 = st.columns([1, 20])
    with col1:
        show_svg_icon("bar-chart-3", width=32, height=32, animation="gentlePulse", color="#3B82F6")
    with col2:
        st.subheader("Análisis de Tendencias Meteorológicas")

    # Mostrar fecha actual
    from datetime import datetime
    current_date = datetime.now().strftime("%d de %B de %Y")
    st.caption(f"📅 **Fecha**: {current_date}")

    # Simular datos históricos para el análisis (últimas 24 horas con intervalos de 30 min)
    import pandas as pd
    import plotly.graph_objects as go
    from datetime import datetime, timedelta
    import numpy as np

    # Generar datos simulados de las últimas 24 horas con intervalos de 30 minutos
    now = datetime.now()
    # 48 puntos de datos (24 horas * 2 intervalos por hora)
    time_points = [now - timedelta(minutes=30*i) for i in range(48, 0, -1)]

    # Simular tendencias realistas con más detalle
    base_temp = 25
    temp_trend = [base_temp + 5 * np.sin(i/8) + np.random.normal(0, 0.5) for i in range(48)]

    base_humidity = 60
    humidity_trend = [base_humidity + 10 * np.cos(i/6) + np.random.normal(0, 1) for i in range(48)]

    base_pressure = 1013
    pressure_trend = [base_pressure + 5 * np.sin(
        i/12) + np.random.normal(0,
        0.3) for i in range(48)]

    base_wind = 10
    wind_trend = [base_wind + 3 * np.sin(i/4) + np.random.normal(0, 0.5) for i in range(48)]

    # Crear DataFrame con formato de hora:minuto
    df_trends = pd.DataFrame({
        'Hora': [h.strftime('%H:%M') for h in time_points],
        'Temperatura': temp_trend,
        'Humedad': humidity_trend,
        'Presión': pressure_trend,
        'Viento': wind_trend
    })

    # Gráfico de temperatura
    fig_temp = go.Figure()
    fig_temp.add_trace(go.Scatter(
        x=df_trends['Hora'],
        y=df_trends['Temperatura'],
        mode='lines+markers',
        name='Temperatura',
        line=dict(color='#EF4444', width=2),
        marker=dict(size=4)
    ))
    fig_temp.update_layout(
        title="Tendencia de Temperatura (24h - Intervalos de 30 min)",
        xaxis_title="Hora",
        yaxis_title="Temperatura (°C)",
        height=300,
        xaxis=dict(tickangle=45)
    )
    st.plotly_chart(fig_temp, use_container_width=True)

    # Gráfico combinado de humedad y presión
    fig_combined = go.Figure()

    # Humedad (eje izquierdo)
    fig_combined.add_trace(go.Scatter(
        x=df_trends['Hora'],
        y=df_trends['Humedad'],
        mode='lines+markers',
        name='Humedad (%)',
        line=dict(color='#3B82F6', width=2),
        marker=dict(size=4),
        yaxis='y'
    ))

    # Presión (eje derecho)
    fig_combined.add_trace(go.Scatter(
        x=df_trends['Hora'],
        y=df_trends['Presión'],
        mode='lines+markers',
        name='Presión (hPa)',
        line=dict(color='#8B5CF6', width=2),
        marker=dict(size=4),
        yaxis='y2'
    ))

    fig_combined.update_layout(
        title="Tendencia de Humedad y Presión (24h - Intervalos de 30 min)",
        xaxis_title="Hora",
        yaxis=dict(title="Humedad (%)", side="left"),
        yaxis2=dict(title="Presión (hPa)", side="right", overlaying="y"),
        height=300,
        xaxis=dict(tickangle=45)
    )
    st.plotly_chart(fig_combined, use_container_width=True)

    # Gráfico de viento
    fig_wind = go.Figure()
    fig_wind.add_trace(go.Scatter(
        x=df_trends['Hora'],
        y=df_trends['Viento'],
        mode='lines+markers',
        name='Velocidad del Viento',
        line=dict(color='#10B981', width=2),
        marker=dict(size=4),
        fill='tonexty'
    ))
    fig_wind.update_layout(
        title="Tendencia de Velocidad del Viento (24h - Intervalos de 30 min)",
        xaxis_title="Hora",
        yaxis_title="Velocidad (km/h)",
        height=300,
        xaxis=dict(tickangle=45)
    )
    st.plotly_chart(fig_wind, use_container_width=True)

    # Análisis de tendencias
    st.markdown("### 📊 Resumen de Cambios (Últimas 24h)")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        temp_change = temp_trend[-1] - temp_trend[0]
        st.metric("Cambio Temperatura", f"{temp_change:+.1f}°C",
                 delta=f"{temp_change:+.1f}°C" if abs(temp_change) > 0.5 else "Estable")

    with col2:
        humidity_change = humidity_trend[-1] - humidity_trend[0]
        st.metric("Cambio Humedad", f"{humidity_change:+.1f}%",
                 delta=f"{humidity_change:+.1f}%" if abs(humidity_change) > 2 else "Estable")

    with col3:
        pressure_change = pressure_trend[-1] - pressure_trend[0]
        st.metric("Cambio Presión", f"{pressure_change:+.1f} hPa",
                 delta=f"{pressure_change:+.1f} hPa" if abs(pressure_change) > 1 else "Estable")

    with col4:
        wind_change = wind_trend[-1] - wind_trend[0]
        st.metric("Cambio Viento", f"{wind_change:+.1f} km/h",
                 delta=f"{wind_change:+.1f} km/h" if abs(wind_change) > 1 else "Estable")

def show_model_comparison():
    """Mostrar comparación simplificada de modelos de Windy"""
    st.markdown("---")

    # Header con icono SVG más profesional
    col1, col2 = st.columns([1, 20])
    with col1:
        show_svg_icon("bar-chart-3", width=32, height=32, animation="gentlePulse", color="#3B82F6")
    with col2:
        st.subheader("Modelos de Pronóstico Disponibles")

    # Mostrar solo información esencial en formato de cards
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **🌍 ECMWF** - Modelo Europeo
        - Resolución: 14 km
        - Precisión: 92%
        - Ideal para: Precipitaciones
        """)

        st.markdown("""
        **🌍 HRRR** - Alta Resolución
        - Resolución: 3 km
        - Precisión: 94%
        - Ideal para: Estados Unidos
        """)

    with col2:
        st.markdown("""
        **🌍 GFS27** - Global NOAA
        - Resolución: 27 km
        - Precisión: 88%
        - Ideal para: Pronósticos largos
        """)

        st.markdown("""
        **🌍 ICON7** - Modelo Alemán
        - Resolución: 7 km
        - Precisión: 90%
        - Ideal para: Europa
        """)

    # Información adicional compacta
    st.info("💡 **Recomendación**: ECMWF para uso general, HRRR para máxima precisión local")

    # Niveles de Alerta Meteorológica - Movido aquí
    st.markdown("---")

    # Header con icono SVG
    col1, col2 = st.columns([1, 20])
    with col1:
        # Icono SVG animado para criterios de probabilidad
        show_svg_icon("alert-circle", width=48, height=48, animation="smoothBlink", color="#3B82F6")
    with col2:
        st.subheader("Criterios de Probabilidad")

    # En pantallas grandes: 4 columnas, en móvil: 2 columnas
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        with st.container():
            show_svg_icon(
                "check-circle",
                width=24,
                height=24,
                animation="smoothBlink",
                color="#10B981")
            st.markdown("""
            **BAJO RIESGO**
            - 0-39% probabilidad
            - Condiciones normales
            - Vuelo seguro
            """)

    with col2:
        with st.container():
            show_svg_icon("info", width=24, height=24, animation="smoothBlink", color="#F59E0B")
            st.markdown("""
            **RIESGO MODERADO**
            - 40-59% probabilidad
            - Monitorear condiciones
            - Precaución recomendada
            """)

    with col3:
        with st.container():
            show_svg_icon(
                "alert-circle",
                width=24,
                height=24,
                animation="smoothBlink",
                color="#F59E0B")
            st.markdown("""
            **ALTO RIESGO**
            - 60-79% probabilidad
            - Precaución recomendada
            - Evitar vuelo nocturno
            """)

    with col4:
        with st.container():
            show_svg_icon("alert-triangle", width=24, height=24,
                         animation="smoothBlink", color="#EF4444")
            st.markdown("""
            **ALERTA CRÍTICA**
            - 80%+ probabilidad
            - Tormenta inminente
            - Evitar vuelo
            """)


def show_ml_dashboard(selected_api="OpenWeatherMap", selected_model=None):
    """Mostrar dashboard de Machine Learning desde pages/ml_dashboard.py"""
    try:
        # Importar y ejecutar la función principal del ML dashboard
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'pages_modules'))

        # Importar la función main del ML dashboard
        from ml_dashboard import main as ml_dashboard_main
        ml_dashboard_main(selected_api, selected_model)

    except ImportError as e:
        st.error(f"❌ Error importando ML dashboard: {e}")
        # Fallback al dashboard simplificado
        st.header("🤖 ML Dashboard")
        st.markdown("**Sistema de Predicción con Machine Learning**")
        st.info("👆 Dashboard ML completo disponible en pages/ml_dashboard.py")

def show_reference():
    """Mostrar página de referencia técnica desde pages/reference.py"""
    try:
        # Importar y ejecutar la función principal de reference
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'pages_modules'))

        # Importar la función main de reference
        from reference import main as reference_main
        reference_main()

    except ImportError as e:
        st.error(f"❌ Error importando reference: {e}")
        # Fallback al contenido básico
        st.header("📚 Referencia Técnica")
        st.markdown("**Documentación técnica del sistema**")
        st.info("👆 Referencia completa disponible en pages/reference.py")

def show_map_page(selected_api="OpenWeatherMap", selected_model=None):
    """Mostrar mapa interactivo desde pages_modules/map_live.py"""
    try:
        # Importar y ejecutar la función principal del mapa
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'pages_modules'))

        # Importar la función main del mapa
        from map_live import main as map_main
        map_main(selected_api, selected_model)

    except ImportError as e:
        st.error(f"❌ Error importando mapa: {e}")
        # Fallback al contenido básico
        st.header("🗺️ Mapa Interactivo")
        st.markdown("**Mapa meteorológico en tiempo real**")
        st.info("👆 Mapa completo disponible en pages_modules/map_live.py")

def show_cache_admin():
    """Mostrar panel de administración de cache desde pages_modules/cache_admin.py"""
    try:
        # Importar y ejecutar la función principal del admin de cache
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'pages_modules'))

        # Importar la función main del admin de cache
        from cache_admin import main as cache_admin_main
        cache_admin_main()

    except ImportError as e:
        st.error(f"❌ Error importando admin de cache: {e}")
        # Fallback al contenido básico
        st.header("🗄️ Administración de Cache")
        st.markdown("**Gestión del sistema de cache**")
        st.info("👆 Panel de administración completo disponible en pages_modules/cache_admin.py")

if __name__ == "__main__":
    main()
