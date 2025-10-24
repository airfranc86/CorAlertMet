"""
Mapa Interactivo - CorAlertMet Intelligence
Mapa con 4 ubicaciones estratégicas para análisis meteorológico
"""

import streamlit as st
import folium
import requests
from streamlit_folium import st_folium

# Agregar src al path (comentado - directorio src no existe)
# sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Importar componentes
# from components.footer import show_footer
from components.styles import apply_corporate_styles

# Configuración de la página
st.set_page_config(
    page_title="Mapa Interactivo - CorAlertMet Intelligence",
    page_icon="🗺️",
    layout="wide"
)

# Aplicar estilos corporativos
apply_corporate_styles()

def get_aeronautical_coordinates(location_name):
    """
    Obtiene coordenadas usando códigos aeronáuticos ICAO/IATA
    Basado en datos oficiales del SMN y OACI
    """
    # Base de datos de aeropuertos de Córdoba con códigos oficiales
    aeronautical_db = {
        "Córdoba Centro": {
            "icao": None,
            "iata": None,
            "lat": -31.4201,
            "lon": -64.1888,
            "name": "Plaza San Martín, Córdoba",
            "type": "ciudad"
        },
        "Aeropuerto SACO/COR": {
            "icao": "SACO",
            "iata": "COR",
            "lat": -31.3236,
            "lon": -64.2079,
            "name": "Aeropuerto Internacional Ingeniero Ambrosio L.V. Taravella",
            "type": "aeropuerto"
        },
        "Río Cuarto": {
            "icao": "SAOC",
            "iata": "RCU",
            "lat": -33.1303,
            "lon": -64.3499,
            "name": "Aeropuerto Río Cuarto",
            "type": "aeropuerto"
        },
        "Altagracia": {
            "icao": "SAGR",
            "iata": None,
            "lat": -31.6500,
            "lon": -64.3500,
            "name": "Altagracia",
            "type": "localidad"
        },
        "Villa María": {
            "icao": "SACV",
            "iata": "VME",
            "lat": -32.3206,
            "lon": -63.2264,
            "name": "Aeropuerto Villa María",
            "type": "aeropuerto"
        },
        "San Francisco": {
            "icao": "SANS",
            "iata": "SFN",
            "lat": -31.4278,
            "lon": -62.0831,
            "name": "Aeropuerto San Francisco",
            "type": "aeropuerto"
        }
    }

    if location_name in aeronautical_db:
        location_data = aeronautical_db[location_name]
        return {
            "lat": location_data["lat"],
            "lon": location_data["lon"],
            "source": "SMN/OACI",
            "icao": location_data.get("icao"),
            "iata": location_data.get("iata"),
            "name": location_data["name"],
            "type": location_data["type"]
        }

    return None

@st.cache_data(ttl=900, show_spinner=False)  # Cache 15 minutos para datos meteorológicos
def get_weather_data_windy(lat, lon):
    """
    Obtiene datos meteorológicos de Windy API
    """
    try:
        # Simular datos de Windy (en producción usar API real)
        import random

        # Simular datos meteorológicos realistas
        weather_data = {
            "temperature": round(random.uniform(15, 35), 1),  # 15-35°C
            "humidity": round(random.uniform(30, 90), 1),      # 30-90%
            "pressure": round(random.uniform(1000, 1020), 1), # 1000-1020 hPa
            "wind_speed": round(random.uniform(5, 25), 1),     # 5-25 km/h
            "wind_direction": random.randint(0, 360),         # 0-360°
            "visibility": round(random.uniform(5, 20), 1),    # 5-20 km
            "precipitation": round(random.uniform(0, 10), 1)   # 0-10 mm
        }

        return weather_data

    except Exception as e:
        st.error(f"Error obteniendo datos meteorológicos: {e}")
        return None

def get_temp_color(temp: float) -> str:
    """
    Obtiene color según temperatura
    """
    if temp < 10:
        return "blue"      # Muy frío
    elif temp < 20:
        return "lightblue" # Frío
    elif temp < 25:
        return "green"     # Templado
    elif temp < 30:
        return "orange"    # Caliente
    else:
        return "red"       # Muy caliente

def get_combined_temp_wind_color(temp: float, wind_speed: float) -> str:
    """
    Obtiene color combinado basado en temperatura y viento
    Rojo = Alta temperatura + Viento intenso
    Verde = Temperatura normal + Viento suave
    Azul = Baja temperatura + Viento suave
    Amarillo = Temperatura alta + Viento suave
    Naranja = Temperatura normal + Viento intenso
    """
    # Clasificar temperatura
    if temp < 10:
        temp_level = "cold"  # Frío
    elif temp < 20:
        temp_level = "cool"  # Fresco
    elif temp < 25:
        temp_level = "normal"  # Normal
    elif temp < 30:
        temp_level = "warm"  # Cálido
    else:
        temp_level = "hot"  # Caliente

    # Clasificar viento
    if wind_speed < 10:
        wind_level = "calm"  # Calmado
    elif wind_speed < 20:
        wind_level = "moderate"  # Moderado
    else:
        wind_level = "strong"  # Fuerte

    # Combinar colores según temperatura y viento
    if temp_level == "hot" and wind_level == "strong":
        return "#DC2626"  # Rojo intenso - Alta temp + Viento fuerte
    elif temp_level == "hot" and wind_level == "moderate":
        return "#EF4444"  # Rojo - Alta temp + Viento moderado
    elif temp_level == "hot" and wind_level == "calm":
        return "#F59E0B"  # Amarillo - Alta temp + Viento calmado
    elif temp_level == "warm" and wind_level == "strong":
        return "#EA580C"  # Naranja - Temp cálida + Viento fuerte
    elif temp_level == "warm" and wind_level == "moderate":
        return "#F97316"  # Naranja claro - Temp cálida + Viento moderado
    elif temp_level == "warm" and wind_level == "calm":
        return "#F59E0B"  # Amarillo - Temp cálida + Viento calmado
    elif temp_level == "normal" and wind_level == "strong":
        return "#059669"  # Verde oscuro - Temp normal + Viento fuerte
    elif temp_level == "normal" and wind_level == "moderate":
        return "#10B981"  # Verde - Temp normal + Viento moderado
    elif temp_level == "normal" and wind_level == "calm":
        return "#22C55E"  # Verde claro - Temp normal + Viento calmado
    elif temp_level == "cool" and wind_level == "strong":
        return "#0891B2"  # Cian - Temp fresca + Viento fuerte
    elif temp_level == "cool" and wind_level == "moderate":
        return "#06B6D4"  # Cian claro - Temp fresca + Viento moderado
    elif temp_level == "cool" and wind_level == "calm":
        return "#67E8F9"  # Cian muy claro - Temp fresca + Viento calmado
    elif temp_level == "cold" and wind_level == "strong":
        return "#1E40AF"  # Azul oscuro - Temp fría + Viento fuerte
    elif temp_level == "cold" and wind_level == "moderate":
        return "#3B82F6"  # Azul - Temp fría + Viento moderado
    else:  # cold + calm
        return "#60A5FA"  # Azul claro - Temp fría + Viento calmado

def get_wind_color(speed: float) -> str:
    """
    Obtiene color según velocidad del viento
    """
    if speed < 10:
        return "green"     # Viento suave
    elif speed < 20:
        return "yellow"    # Viento moderado
    elif speed < 30:
        return "orange"    # Viento fuerte
    else:
        return "red"       # Viento muy fuerte

def get_wind_direction_arrow(direction: int) -> str:
    """
    Convierte dirección en grados a flecha Unicode
    """
    if direction < 22.5 or direction >= 337.5:
        return "↑"  # Norte
    elif direction < 67.5:
        return "↗"  # Noreste
    elif direction < 112.5:
        return "→"  # Este
    elif direction < 157.5:
        return "↘"  # Sureste
    elif direction < 202.5:
        return "↓"  # Sur
    elif direction < 247.5:
        return "↙"  # Suroeste
    elif direction < 292.5:
        return "←"  # Oeste
    else:
        return "↖"  # Noroeste

def get_pressure_color(pressure: float) -> str:
    """
    Obtiene color según presión atmosférica
    """
    if pressure < 1000:
        return "red"       # Baja presión (tormenta)
    elif pressure < 1010:
        return "orange"    # Presión moderadamente baja
    elif pressure < 1020:
        return "yellow"    # Presión normal
    elif pressure < 1030:
        return "lightgreen" # Presión moderadamente alta
    else:
        return "blue"      # Alta presión (anticiclón)

def get_humidity_color(humidity: float) -> str:
    """
    Obtiene color según humedad relativa
    """
    if humidity < 30:
        return "blue"      # Muy seco (azul)
    elif humidity < 50:
        return "lightblue" # Seco (azul claro)
    elif humidity < 70:
        return "green"     # Normal (verde)
    elif humidity < 85:
        return "orange"    # Húmedo (naranja)
    else:
        return "red"       # Muy húmedo (rojo - niebla)

def get_visibility_color(visibility: float) -> str:
    """
    Obtiene color según visibilidad
    """
    if visibility < 1:
        return "red"       # Niebla densa
    elif visibility < 3:
        return "orange"    # Niebla moderada
    elif visibility < 5:
        return "yellow"    # Niebla ligera
    elif visibility < 10:
        return "lightgreen" # Visibilidad reducida
    else:
        return "green"     # Visibilidad excelente

def get_location_icon_svg(
    icon_type: str = "location",
    size: int = 16,
    color: str = "#3B82F6") -> str:
    """
    Obtiene icono SVG de Heroicons según el tipo
    """
    icons = {
        "location": f"""
<svg width = (
            "{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        )
<path d = (
                "M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z" fill="{color}"/>
            )
        </svg>
        """,
        "airport": f"""
<svg width = (
            "{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        )
<path d = (
                "M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z" fill="{color}"/>
            )
        </svg>
        """,
        "factory": f"""
<svg width = (
            "{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        )
<path d = (
                "M12 2L2 7v10c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V7l-10-5zM6 15h12v2H6v-2zm0-4h12v2H6v-2zm0-4h12v2H6V7z" fill="{color}"/>
            )
        </svg>
        """,
        "wheat": f"""
<svg width = (
            "{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        )
<path d = (
                "M12 2L2 7v10c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V7l-10-5zM6 15h12v2H6v-2zm0-4h12v2H6v-2zm0-4h12v2H6V7z" fill="{color}"/>
            )
        </svg>
        """
    }
    return icons.get(icon_type, icons["location"])

def create_wind_arrow_svg(wind_direction: int, wind_speed: float, size: int = 24) -> str:
    """
    Crea una flecha SVG que indica la dirección del viento
    """
    # Calcular el ángulo de rotación (wind_direction ya viene en grados)
    # El viento sopla HACIA la dirección indicada
    rotation_angle = wind_direction

    # Determinar color según intensidad del viento
    if wind_speed < 10:
        arrow_color = "#10B981"  # Verde - viento suave
    elif wind_speed < 20:
        arrow_color = "#F59E0B"  # Amarillo - viento moderado
    elif wind_speed < 30:
        arrow_color = "#EF4444"  # Rojo - viento fuerte
    else:
        arrow_color = "#7C2D12"  # Marrón - viento muy fuerte

    # Crear SVG de flecha
    arrow_svg = f"""
<svg width = (
        "{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"
    )
         style="transform: rotate({rotation_angle}deg); transform-origin: center;">
        <path d="M12 2L22 12L12 22L12 16L2 16L2 8L12 8L12 2Z"
              fill="{arrow_color}"
              stroke="white"
              stroke-width="1.5"
              stroke-linecap="round"
              stroke-linejoin="round"/>
    </svg>
    """
    return arrow_svg

def create_wind_barb_enhanced(wind_speed: float, wind_direction: int) -> str:
    """
    Crea wind barb mejorado con dirección e intensidad
    """
    # Convertir km/h a nudos
    wind_knots = wind_speed / 1.852

    # Determinar color según intensidad
    if wind_knots < 10:
        color = "#10B981"  # Verde
    elif wind_knots < 20:
        color = "#F59E0B"  # Amarillo
    elif wind_knots < 30:
        color = "#EF4444"  # Rojo
    else:
        color = "#7C2D12"  # Marrón

    # Calcular número de plumas (cada pluma = 10 nudos)
    full_plumes = int(wind_knots // 10)
    half_plume = int((wind_knots % 10) >= 5)

    # Crear wind barb SVG
    barb_svg = f"""
    <svg width="40" height="20" viewBox="0 0 40 20" fill="none" xmlns="http://www.w3.org/2000/svg">
        <!-- Línea principal -->
        <line x1="5" y1="10" x2="35" y2="10" stroke="{color}" stroke-width="2" stroke-linecap="round"/>

        <!-- Plumas completas -->
        {''.join([f'<line x1="{15 + i*3}" y1="10" x2="{15 + i*3}" y2="5" stroke="{color}" stroke-width="2" stroke-linecap="round"/>' for i in range(full_plumes)])}

        <!-- Media pluma -->
        {f'<line x1="{15 + full_plumes*3}" y1="10" x2="{15 + full_plumes*3}" y2="7.5" stroke="{color}" stroke-width="2" stroke-linecap="round"/>' if half_plume else ''}

        <!-- Flecha de dirección -->
        <path d="M35 10L30 7L30 13L35 10Z" fill="{color}"/>
    </svg>
    """
    return barb_svg

def create_enhanced_wind_marker(
    lat: float,
    lon: float,
    combined_color: str,
    wind_direction: int,
    wind_speed: float,
    name: str,
    popup_content: str) -> tuple:
    """
    Crea un marcador con color combinado (temperatura + viento) y flecha de viento
    """
    import math

    # Crear marcador base con color combinado
    marker = folium.CircleMarker(
        [lat, lon],
        radius=25,
        popup=folium.Popup(popup_content, max_width=300),
        tooltip=f"{name} | {wind_speed} km/h | {wind_direction}°",
        color="black",
        weight=3,
        fillColor=combined_color,
        fillOpacity=0.8
    )

    # Crear flecha de viento
    wind_arrow_svg = create_wind_arrow_svg(wind_direction, wind_speed, 20)

    # Calcular posición de la flecha (fuera del marcador)
    angle_rad = math.radians(wind_direction)
    offset_distance = 0.0003  # Aproximadamente 30 metros
    arrow_lat = lat + offset_distance * math.cos(angle_rad)
    arrow_lon = lon + offset_distance * math.sin(angle_rad)

    # Crear marcador de flecha
    wind_arrow_marker = folium.Marker(
        [arrow_lat, arrow_lon],
        icon=folium.DivIcon(
            html=wind_arrow_svg,
            icon_size=(20, 20),
            icon_anchor=(10, 10)
        )
    )

    return marker, wind_arrow_marker

def create_simple_wind_barb(wind_speed: float, wind_direction: int) -> str:
    """
    Crea wind barb simple con dirección e intensidad
    """
    # Convertir km/h a nudos
    wind_knots = wind_speed / 1.852

    # Determinar color según intensidad
    if wind_knots < 10:
        color = "#00AA00"  # Verde
    elif wind_knots < 20:
        color = "#FFAA00"  # Amarillo
    elif wind_knots < 30:
        color = "#FF6600"  # Naranja
    else:
        color = "#FF0000"  # Rojo

    # Calcular número de plumas
    full_barbs = int(wind_knots // 10)
    half_barb = int((wind_knots % 10) // 5)

    # Crear SVG simple
    barb_svg = f"""
    <svg width="40" height="40" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
        <!-- Línea principal -->
        <line x1="20" y1="20" x2="20" y2="20"
              stroke="{color}" stroke-width="4"
              transform="rotate({wind_direction} 20 20)" />

        <!-- Plumas completas -->
        {create_barb_lines(full_barbs, half_barb, wind_direction, color)}

        <!-- Círculo central -->
        <circle cx="20" cy="20" r="4" fill="{color}" />
    </svg>
    """

    return barb_svg

def create_barb_lines(full_barbs: int, half_barb: int, direction: int, color: str) -> str:
    """
    Crea las líneas de las plumas del wind barb
    """
    lines = ""

    # Plumas completas (10 nudos cada una)
    for i in range(full_barbs):
        y_pos = 20 - (i + 1) * 4
        lines += f'<line x1="20" y1="{y_pos}" x2="28" y2="{y_pos}" stroke="{color}" stroke-width="3" transform="rotate({direction} 20 20)" />'

    # Media pluma (5 nudos)
    if half_barb:
        y_pos = 20 - (full_barbs + 1) * 4
        lines += f'<line x1="20" y1="{y_pos}" x2="24" y2="{y_pos}" stroke="{color}" stroke-width="3" transform="rotate({direction} 20 20)" />'

    return lines

@st.cache_data(ttl=1800, show_spinner=False)  # Cache 30 minutos para coordenadas
def get_coordinates_from_api(
    location_name: str,
    selected_api: str = "OpenWeatherMap",
    cache_version: str = "v2.0") -> dict:
    """
    Obtiene coordenadas usando códigos aeronáuticos (preferido) o APIs de geocoding
    """
    # Usar códigos aeronáuticos (más preciso y confiable)
    aeronautical_coords = get_aeronautical_coordinates(location_name)
    if aeronautical_coords:
        return aeronautical_coords

    # Fallback a API de geocoding si no hay datos aeronáuticos
    try:
        api_key = st.secrets.get(
            "openweather_api_key") or st.secrets.get("SECRETS",
            {}).get("openweather_api_key",
            "")
        if not api_key:
            st.error("❌ OpenWeatherMap API Key no configurada")
            return None

        # Mapeo de nombres para geocoding
        location_mapping = {
            "Córdoba Centro": "Córdoba, Argentina",
            "Aeropuerto SACO/COR": "Ingeniero Ambrosio Taravella International Airport, Argentina",
            "Río Cuarto": "Río Cuarto, Argentina",
            "Altagracia": "Altagracia, Córdoba, Argentina",
            "Villa María": "Villa María, Córdoba, Argentina",
            "San Francisco": "San Francisco, Córdoba, Argentina"
        }

        search_query = location_mapping.get(location_name, f"{location_name}, Córdoba, Argentina")

        url = f"http://api.openweathermap.org/geo/1.0/direct"
        params = {
            "q": search_query,
            "limit": 1,
            "appid": api_key
        }

        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data:
                return {
                    "lat": data[0]["lat"],
                    "lon": data[0]["lon"],
                    "source": selected_api
                }
            else:
                st.error(f"❌ No se encontraron coordenadas para {location_name}")
                return None
        else:
            st.error(f"❌ Error de API: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"❌ Error obteniendo coordenadas para {location_name}: {e}")
        return None

def main(selected_api: str = "OpenWeatherMap", selected_model: str = None) -> None:
    """Mostrar mapa interactivo con 4 ubicaciones estratégicas"""

    # Título con icono SVG animado
    col1, col2 = st.columns([1, 20])
    with col1:
        st.markdown("""
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" width="48" height="48" fill="none">
            <style>@keyframes slide{0%{transform:translateX(0)}to{transform:translateX(5.5px) translateY(-1px)}}</style>
<path stroke = (
                "#0A0A30" stroke-width="1.5" d="M4 8a4 4 0 014-4h8a4 4 0 014 4v8a4 4 0 01-4 4H8a4 4 0 01-4-4V8z"/>
            )
<path stroke = (
                "#0A0A30" stroke-width="1.5" d="M4.221 17.607c.498-.603.767-.816 1.263-1.426.944-1.169 1.58-1.507 2.287-1.21.287.123.575.308.87.503.79.523 1.888 1.24 3.334.461.994-.544 1.57-1.477 2.07-2.286.206-.329.4-.657.627-.954.235-.308 1.107-1.271 2.234-.586.719.432 1.314.915 1.96 1.54.247.24.433.614.55.905.352.88.457 1.372.457 2.488"/>
            )
            <path stroke="#265BFF" stroke-width="1.33" d="M8.647 11.032c.977 0 1.773-.796 1.773-1.773 0-.977-.796-1.773-1.773-1.773-.978 0-1.773.796-1.773 1.773 0 .977.795 1.773 1.773 1.773" style="transform-origin:center;animation:slide 1.5s cubic-bezier(
                .86,
                0,
                .07,
                1) infinite alternate-reverse both"/>
        </svg>
        """, unsafe_allow_html=True)
    with col2:
        st.title("Mapa Interactivo Meteorológico")

    st.markdown("**5 ubicaciones estratégicas para análisis regional**")

    # Configuración de ubicaciones (5 ubicaciones estratégicas)
    locations_config = {
        "Aeropuerto SACO/COR": {"color": "blue", "icon": "airport", "icon_type": "airport"},
        "Río Cuarto": {"color": "green", "icon": "location", "icon_type": "location"},
        "Altagracia": {"color": "orange", "icon": "location", "icon_type": "location"},
        "Villa María": {"color": "purple", "icon": "factory", "icon_type": "factory"},
        "San Francisco": {"color": "darkred", "icon": "wheat", "icon_type": "wheat"}
    }


    # Vista integrada con todos los datos meteorológicos
    st.info("**Vista Integrada**: Todos los datos meteorológicos en un solo marcador")

    # Obtener coordenadas y preparar datos
    locations = {}
    coord_data = []

    for name, config in locations_config.items():
        api_coords = get_coordinates_from_api(name, selected_api, "v2.0")

        if not api_coords:
            st.error(f"❌ No se pudieron obtener coordenadas para {name}")
            st.stop()

        # Obtener datos meteorológicos para todas las ubicaciones
        weather_data = get_weather_data_windy(api_coords["lat"], api_coords["lon"])

        # Usar coordenadas obtenidas
        locations[name] = {
            "lat": api_coords["lat"],
            "lon": api_coords["lon"],
            "color": config["color"],
            "icon": config["icon"],
            "icon_type": config["icon_type"],
            "weather": weather_data
        }

        # Preparar datos para tabla
        source = "SMN/OACI" if api_coords.get("source") == "SMN/OACI" else selected_api
        icao = api_coords.get("icao", "N/A") if api_coords.get("source") == "SMN/OACI" else "N/A"
        iata = api_coords.get("iata", "N/A") if api_coords.get("source") == "SMN/OACI" else "N/A"

        coord_data.append({
            "Ubicación": name,
            "Latitud": f"{api_coords['lat']:.2f}°",
            "Longitud": f"{api_coords['lon']:.2f}°",
            "ICAO": icao,
            "IATA": iata,
            "Fuente": source
        })

    # Crear mapa centrado dinámicamente
    center_lat = sum(data["lat"] for data in locations.values()) / len(locations)
    center_lon = sum(data["lon"] for data in locations.values()) / len(locations)

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=8,
        tiles='OpenStreetMap'
    )

    # Agregar marcadores con datos meteorológicos integrados
    for name, data in locations.items():
        if data["weather"]:
            # Marcador con todas las capas meteorológicas integradas
            temp = data["weather"]["temperature"]
            wind_speed = data["weather"]["wind_speed"]
            wind_direction = data["weather"]["wind_direction"]
            pressure = data["weather"]["pressure"]
            humidity = data["weather"]["humidity"]
            visibility = data["weather"]["visibility"]

            # Crear popup con todos los datos
            wind_arrow = get_wind_direction_arrow(wind_direction)
            icon_svg = get_location_icon_svg(data["icon_type"], 16, "#3B82F6")

            # Popup completo con todos los datos meteorológicos
            popup_content = f"""
            <div style="font-family: Arial, sans-serif; min-width: 200px;">
                <h3 style="margin: 0 0 10px 0; color: #2E86AB;">{icon_svg} {name}</h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 12px;">
                    <div style="background: #E3F2FD; padding: 5px; border-radius: 3px;">
<strong><svg width = (
                            '14' height='14' viewBox='0 0 24 24' fill='none' xmlns='http://www.w3.org/2000/svg' style='display: inline; vertical-align: middle; margin-right: 4px;'><path d='M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0z' stroke='#EF4444' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/></svg>Temp:</strong><br>{temp}°C
                        )
                    </div>
                    <div style="background: #E8F5E8; padding: 5px; border-radius: 3px;">
<strong><svg width = (
                            '14' height='14' viewBox='0 0 24 24' fill='none' xmlns='http://www.w3.org/2000/svg' style='display: inline; vertical-align: middle; margin-right: 4px;'><path d='M3 12h18m-9-9l9 9-9 9' stroke='#10B981' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/></svg>Viento:</strong><br>{wind_speed} km/h {wind_arrow}
                        )
                    </div>
                    <div style="background: #FFF3E0; padding: 5px; border-radius: 3px;">
<strong><svg width = (
                            '14' height='14' viewBox='0 0 24 24' fill='none' xmlns='http://www.w3.org/2000/svg' style='display: inline; vertical-align: middle; margin-right: 4px;'><path d='M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z' stroke='#F59E0B' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/></svg>Presión:</strong><br>{pressure} hPa
                        )
                    </div>
                    <div style="background: #F3E5F5; padding: 5px; border-radius: 3px;">
<strong><svg width = (
                            '14' height='14' viewBox='0 0 24 24' fill='none' xmlns='http://www.w3.org/2000/svg' style='display: inline; vertical-align: middle; margin-right: 4px;'><path d='M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z' stroke='#8B5CF6' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/></svg>Humedad:</strong><br>{humidity}%
                        )
                    </div>
                    <div style="background: #E0F2F1; padding: 5px; border-radius: 3px; grid-column: 1 / -1;">
<strong><svg width = (
                            '14' height='14' viewBox='0 0 24 24' fill='none' xmlns='http://www.w3.org/2000/svg' style='display: inline; vertical-align: middle; margin-right: 4px;'><path d='M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z' stroke='#06B6D4' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/><circle cx='12' cy='12' r='3' stroke='#06B6D4' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/></svg>Visibilidad:</strong><br>{visibility} km
                        )
                    </div>
                </div>
            </div>
            """

            # Usar color combinado (temperatura + viento) para el marcador principal
            combined_color = get_combined_temp_wind_color(temp, wind_speed)

            # Crear marcador con flecha de viento
            marker, wind_arrow = create_enhanced_wind_marker(
                data["lat"],
                data["lon"],
                combined_color,
                wind_direction,
                wind_speed,
                name,
                popup_content
            )

            # Agregar elementos al mapa
            marker.add_to(m)
            wind_arrow.add_to(m)

        else:
            # Marcador normal
            icon_svg = get_location_icon_svg(data["icon_type"], 16, "#3B82F6")
            folium.Marker(
                [data["lat"], data["lon"]],
                popup=f"<b>{icon_svg} {name}</b>",
                tooltip=f"{name}",
                icon=folium.Icon(color=data["color"], icon="info-sign")
            ).add_to(m)

    # Mostrar mapa responsivo
    st_folium(m, width=1200, height=600, returned_objects=[])

    # Selector de capas
    st.markdown("---")
    st.markdown(
        "### <svg width='20' height='20' viewBox='0 0 24 24' fill='none' xmlns='http://www.w3.org/2000/svg' style='display: inline; vertical-align: middle; margin-right: 8px;'><path d='M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z' stroke='#3B82F6' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/></svg> Seleccionar Capa de Visualización",
        unsafe_allow_html=True)
    selected_layer = st.selectbox(
        "Elige qué datos meteorológicos mostrar en la leyenda:",
        ["Temperatura", "Viento", "Todas las Capas"],
        index=0,
        help="Selecciona el tipo de datos meteorológicos para ver la leyenda correspondiente"
    )

    # Mostrar leyenda según la capa seleccionada
    if selected_layer == "Temperatura":
        st.markdown(
            "#### <svg width='20' height='20' viewBox='0 0 24 24' fill='none' xmlns='http://www.w3.org/2000/svg' style='display: inline; vertical-align: middle; margin-right: 8px;'><path d='M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0z' stroke='#EF4444' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/></svg> Leyenda de Temperatura",
            unsafe_allow_html=True)
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.markdown("**< 10°C**<br>Muy frío", unsafe_allow_html=True)
        with col2:
            st.markdown("**10-20°C**<br>Frío", unsafe_allow_html=True)
        with col3:
            st.markdown("**20-25°C**<br>Templado", unsafe_allow_html=True)
        with col4:
            st.markdown("**25-30°C**<br>Caliente", unsafe_allow_html=True)
        with col5:
            st.markdown("**> 30°C**<br>Muy caliente", unsafe_allow_html=True)

    elif selected_layer == "Viento":
        st.markdown(
            "#### <svg width='20' height='20' viewBox='0 0 24 24' fill='none' xmlns='http://www.w3.org/2000/svg' style='display: inline; vertical-align: middle; margin-right: 8px;'><path d='M3 12h18m-9-9l9 9-9 9' stroke='#10B981' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/></svg> Leyenda de Viento",
            unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown("**< 10 km/h**<br>Viento suave", unsafe_allow_html=True)
        with col2:
            st.markdown("**10-20 km/h**<br>Viento moderado", unsafe_allow_html=True)
        with col3:
            st.markdown("**20-30 km/h**<br>Viento fuerte", unsafe_allow_html=True)
        with col4:
            st.markdown("**> 30 km/h**<br>Viento muy fuerte", unsafe_allow_html=True)


    elif selected_layer == "Todas las Capas":
        st.markdown(
            "#### <svg width='20' height='20' viewBox='0 0 24 24' fill='none' xmlns='http://www.w3.org/2000/svg' style='display: inline; vertical-align: middle; margin-right: 8px;'><path d='M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z' stroke='#8B5CF6' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/><path d='M8 21v-4a2 2 0 012-2h4a2 2 0 012 2v4' stroke='#8B5CF6' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/></svg> Vista Integrada - Todas las Capas Meteorológicas",
            unsafe_allow_html=True)

        st.markdown("""
        <div style="background: linear-gradient(
            135deg,
            #E3F2FD,
            #E8F5E8,
            #FFF3E0,
            #F3E5F5,
            #E0F2F1);
                    padding: 20px; border-radius: 10px; margin: 10px 0;">
            <h4 style="margin: 0 0 15px 0; color: #2E86AB;">Interpretación de la Vista Integrada</h4>
            <div style="display: grid; grid-template-columns: repeat(
                auto-fit,
                minmax(200px,
                1fr)); gap: 15px;">
                <div style="background: #E3F2FD; padding: 10px; border-radius: 5px;">
                    <strong>Color del Marcador:</strong><br>
                    Combinación de temperatura + viento
                </div>
                <div style="background: #E8F5E8; padding: 10px; border-radius: 5px;">
                    <strong>Flecha de Viento:</strong><br>
                    Dirección del viento
                </div>
                <div style="background: #F3E5F5; padding: 10px; border-radius: 5px;">
                    <strong>Colores Combinados:</strong><br>
                    🔴 Rojo = Alta temp + Viento fuerte<br>
                    🟢 Verde = Temp normal + Viento suave<br>
                    🔵 Azul = Baja temp + Viento suave
                </div>
                <div style="background: #FFF3E0; padding: 10px; border-radius: 5px;">
                    <strong>Popup Completo:</strong><br>
                    Todos los datos meteorológicos
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Mostrar tabla de coordenadas (debajo del mapa)
    st.markdown("### 📍 Coordenadas de Ubicaciones")
    st.dataframe(coord_data, use_container_width=True)

# Ejecutar la página
if __name__ == "__main__":
    main()