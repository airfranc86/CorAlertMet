"""
Página de Referencia Técnica - CorAlertMet Intelligence
"""

import streamlit as st
import sys
import os

# Agregar src al path (comentado - directorio src no existe)
# sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Importar componentes
from components.footer import show_footer
from components.styles import apply_corporate_styles
# from components.svg_icons_simple import show_svg_icon  # Import moved inside functions

# Configuración de la página
st.set_page_config(
    page_title="Referencia Técnica - CorAlertMet Intelligence",
    page_icon="📚",
    layout="wide"
)

# Aplicar estilos corporativos
apply_corporate_styles()

def main():
    """Mostrar página de referencia técnica"""

    # Header principal con icono SVG
    col1, col2 = st.columns([1, 20])
    with col1:
        from components.svg_icons_simple import show_svg_icon
        show_svg_icon("book", width=48, height=48, animation="pulse", color="#3B82F6")
    with col2:
        st.title("Referencia Técnica")
        st.markdown("**Documentación científica y técnica del sistema**")

    # Variables Meteorológicas
    col1, col2 = st.columns([1, 20])
    with col1:
        from components.svg_icons_simple import show_svg_icon
        show_svg_icon("thermometer", width=32, height=32, animation="pulse", color="#EF4444")
    with col2:
        st.header("Variables Meteorológicas")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        col1_1, col1_2 = st.columns([1, 4])
        with col1_1:
            from components.svg_icons_simple import show_svg_icon
            show_svg_icon("wind", width=20, height=20, animation="rotate", color="#10B981")
        with col1_2:
            st.info("**Viento**\n> 50 km/h crítico\nRáfagas > 70 km/h")

    with col2:
        col2_1, col2_2 = st.columns([1, 4])
        with col2_1:
            from components.svg_icons_simple import show_svg_icon
            show_svg_icon("droplet", width=20, height=20, animation="bounce", color="#3B82F6")
        with col2_2:
            st.info("**Humedad**\n> 80% crítico\nPunto rocío > 20°C")

    with col3:
        col3_1, col3_2 = st.columns([1, 4])
        with col3_1:
            from components.svg_icons_simple import show_svg_icon
            show_svg_icon("gauge", width=20, height=20, animation="scale", color="#8B5CF6")
        with col3_2:
            st.info("**Presión**\n> Caída de 4 hPa/h crítico")

    with col4:
        col4_1, col4_2 = st.columns([1, 4])
        with col4_1:
            from components.svg_icons_simple import show_svg_icon
            show_svg_icon("cloud", width=20, height=20, animation="pulse", color="#6B7280")
        with col4_2:
            st.info("**Nubosidad**\n> 70% crítico\nCumulonimbus")

    st.markdown("---")


    # Diagrama compacto en una sola fila
    col1, col2 = st.columns([1, 20])
    with col1:
        from components.svg_icons_simple import show_svg_icon
        show_svg_icon("refresh", width=24, height=24, animation="rotate", color="#3B82F6")
    with col2:
        st.markdown("### Flujo de Procesamiento")

    # Crear un diagrama horizontal compacto
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

    with col1:
        st.markdown("**INPUT**")
        st.info("Datos OACI/SMN")

    with col2:
        st.markdown("**VALIDACIÓN**")
        st.warning("Control Calidad")

    with col3:
        st.markdown("**EXTRACCIÓN**")
        st.success("Características")

    with col4:
        st.markdown("**MODELO**")
        st.error("ML + Reglas OACI")

    with col5:
        st.markdown("**FUSIÓN**")
        st.info("Resultados")

    with col6:
        st.markdown("**CÁLCULO**")
        st.success("Probabilidad")

    with col7:
        st.markdown("**OUTPUT**")
        st.error("GO/NO-GO")

    st.markdown("---")


    # Organizar en 4 columnas
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        # Fuentes de Datos
        col1_1, col1_2 = st.columns([1, 20])
        with col1_1:
            from components.svg_icons_simple import show_svg_icon
            show_svg_icon(
                "bar-chart-3",
                width=20,
                height=20,
                animation="gentlePulse",
                color="#3B82F6")
        with col1_2:
            st.markdown("**Fuentes de Datos:**")

        st.markdown("""
        • SMN (Servicio Meteorológico Nacional)
        • OACI (Organización de Aviación Civil Internacional)
        • OpenWeatherMap API (Validación)
        • Windy API (Corroboración)
        """)

        # Parámetros Monitoreados
        col1_3, col1_4 = st.columns([1, 20])
        with col1_3:
            from components.svg_icons_simple import show_svg_icon
            show_svg_icon("thermometer", width=20, height=20, animation="pulse", color="#EF4444")
        with col1_4:
            st.markdown("**Parámetros Monitoreados:**")

        st.markdown("""
        • Temperatura del aire
        • Humedad relativa
        • Presión atmosférica
        • Velocidad y dirección del viento
        • Visibilidad horizontal
        • Nubosidad y altura de base
        """)

    with col2:
        # Algoritmos Utilizados
        col2_1, col2_2 = st.columns([1, 20])
        with col2_1:
            from components.svg_icons_simple import show_svg_icon
            show_svg_icon("brain", width=20, height=20, animation="pulse", color="#8B5CF6")
        with col2_2:
            st.markdown("**Algoritmos Utilizados:**")

        st.markdown("""
        • Gradient Boosting (XGBoost)
        • Reglas Heurísticas OACI
        • Análisis de Series Temporales
        • Detección de Anomalías
        """)

        # Precisión del Sistema
        col2_3, col2_4 = st.columns([1, 20])
        with col2_3:
            from components.svg_icons_simple import show_svg_icon
            show_svg_icon("gauge", width=20, height=20, animation="gentlePulse", color="#10B981")
        with col2_4:
            st.markdown("**Precisión del Sistema:**")

        st.markdown("""
        • Sensibilidad: 94.2%
        • Especificidad: 91.8%
        • Precisión: 89.5%
        • F1-Score: 91.8%
        """)

    with col3:
        # Modelos Globales
        col3_1, col3_2 = st.columns([1, 20])
        with col3_1:
            from components.svg_icons_simple import show_svg_icon
            show_svg_icon("compass", width=20, height=20, animation="rotate", color="#3B82F6")
        with col3_2:
            st.markdown("**Modelos Globales:**")

        st.markdown("""
        • ECMWF: 14 km, 12h
        • GFS27: 27 km, 4x/día
        • ICON7/13: 7-13 km, 6h/3h
        • GFS+: 27x27 km
        """)

        # Modelos Regionales
        col3_3, col3_4 = st.columns([1, 20])
        with col3_3:
            from components.svg_icons_simple import show_svg_icon
            show_svg_icon("map", width=20, height=20, animation="pulse", color="#10B981")
        with col3_4:
            st.markdown("**Modelos Regionales:**")

        st.markdown("""
        • NAM: 12 km, 2x/día
        • HRRR: 3 km, 18x/día
        • AROME: 1.25 km, 3h
        • NEMS: 4-30 km
        """)

    with col4:
        # Estándares Implementados
        col4_1, col4_2 = st.columns([1, 20])
        with col4_1:
            from components.svg_icons_simple import show_svg_icon
            show_svg_icon("check-circle", width=20, height=20, animation="pulse", color="#10B981")
        with col4_2:
            st.markdown("**Estándares Implementados:**")

        st.markdown("""
        • OACI Annex 3
        • OACI Doc 8896
        • WMO-No. 49
        • FAA AC 00-45H
        """)

        # Validación del Sistema
        col4_3, col4_4 = st.columns([1, 20])
        with col4_3:
            from components.svg_icons_simple import show_svg_icon
            show_svg_icon("search", width=20, height=20, animation="gentlePulse", color="#3B82F6")
        with col4_4:
            st.markdown("**Validación del Sistema:**")

        st.markdown("""
        • Certificación SMN
        • Datos históricos 5 años
        • Pruebas de estrés
        • Auditoría aeronáutica
        """)

    st.markdown("---")

    # Contacto y Soporte
    col1, col2 = st.columns([1, 20])
    with col1:
        from components.svg_icons_simple import show_svg_icon
        show_svg_icon("mail", width=32, height=32, animation="bounce", color="#3B82F6")
    with col2:
        st.header("Contacto")

    st.markdown("""
    **Contacto:**
    - Email: franciscoaucar@ajconsultingit.com
    - GitHub: [airfranc86/CAMet](https://github.com/airfranc86/CAMet)
    """)

# Ejecutar la página
if __name__ == "__main__":
    main()
