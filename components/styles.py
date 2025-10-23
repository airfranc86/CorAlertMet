"""
Componente de estilos CSS centralizado para CorAlertMet Intelligence
"""
import streamlit as st

def apply_corporate_styles():
    """
    Aplicar estilos corporativos responsivos para CorAlertIntel
    Siguiendo las mejores prácticas de Streamlit CSS
    """
    st.markdown("""
    <style>
    /* ===== OCULTAR ELEMENTOS NATIVOS DE STREAMLIT ===== */
    /* Ocultar menú hamburguesa */
    #MainMenu {visibility: hidden;}

    /* Ocultar footer nativo */
    footer {visibility: hidden;}

    /* Ocultar botón de deploy */
    .stDeployButton {display: none;}

    /* Ocultar toolbar de Streamlit */
    div[data-testid="stToolbar"] {
        visibility: hidden;
        height: 0;
        position: absolute;
    }

    /* Ocultar decoración de Streamlit */
    div[data-testid="stDecoration"] {display: none;}

    /* ===== RESPONSIVIDAD MÓVIL (≤ 768px) ===== */
    @media (max-width: 768px) {
        /* Sidebar responsivo - usar clases estándar de Streamlit */
        .css-1d391kg {
            width: 100% !important;
            min-width: 100% !important;
        }

        /* Columnas responsivas - 4 columnas → 2 columnas */
        .element-container .stColumn {
            flex: 0 0 50% !important;
            max-width: 50% !important;
        }

        /* Iconos SVG responsivos */
        .smooth-icon {
            width: 20px !important;
            height: 20px !important;
        }

        /* Botones responsivos */
        .stButton > button {
            width: 100% !important;
            font-size: 14px !important;
        }

        /* Métricas responsivas */
        .metric-container {
            padding: 8px !important;
        }

        /* Texto responsivo - usar selectores específicos de Streamlit */
        .stMarkdown h1 {
            font-size: 1.5rem !important;
        }
        .stMarkdown h2 {
            font-size: 1.3rem !important;
        }
        .stMarkdown h3 {
            font-size: 1.1rem !important;
        }

        /* Gráficos Plotly responsivos */
        .js-plotly-plot {
            width: 100% !important;
            height: auto !important;
        }

        /* Mapa Folium responsivo */
        .folium-container {
            width: 100% !important;
            height: 300px !important;
        }
    }

    /* ===== MÓVIL PEQUEÑO (≤ 480px) ===== */
    @media (max-width: 480px) {
        /* Una columna en pantallas muy pequeñas */
        .element-container .stColumn {
            flex: 0 0 100% !important;
            max-width: 100% !important;
        }

        /* Sidebar colapsado en móvil */
        .css-1d391kg {
            transform: translateX(-100%);
            transition: transform 0.3s ease;
        }

        /* Iconos más pequeños */
        .smooth-icon {
            width: 16px !important;
            height: 16px !important;
        }

        /* Padding reducido en móvil */
        .main .block-container {
            padding: 1rem !important;
        }
    }

    /* ===== TABLET (769px - 1024px) ===== */
    @media (min-width: 769px) and (max-width: 1024px) {
        .element-container .stColumn {
            flex: 0 0 33.333% !important;
            max-width: 33.333% !important;
        }
    }

    /* ===== MEJORAS GENERALES DE RESPONSIVIDAD ===== */
    /* Selectbox responsivo */
    .stSelectbox > div > div {
        min-width: 0 !important;
    }

    /* Radio buttons responsivos */
    .stRadio > div {
        flex-wrap: wrap !important;
    }

    .stRadio > div > label {
        flex: 1 1 auto !important;
        min-width: 0 !important;
    }

    /* Tablas responsivas con scroll horizontal */
    .stDataFrame {
        overflow-x: auto !important;
    }

    /* Footer responsivo */
    .footer-container {
        flex-direction: column !important;
        text-align: center !important;
    }

    .footer-container > div {
        margin-bottom: 10px !important;
    }

    /* ===== MEJORAS ESPECÍFICAS DE STREAMLIT ===== */
    /* Mejorar contenedores de métricas */
    .metric-container {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: rgba(255, 255, 255, 0.05);
    }

    /* Mejorar botones */
    .stButton > button {
        border-radius: 0.5rem;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    /* Mejorar sidebar */
    .css-1d391kg {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    }

    /* Mejorar contenedores principales */
    .main .block-container {
        padding: 2rem 1rem 60px 1rem; /* Espacio extra para footer fijo */
        max-width: 1200px;
    }

    /* Footer fijo - asegurar que esté siempre visible */
    .footer-fixed {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        z-index: 1000 !important;
    }

    /* ===== ANIMACIONES SUAVES ===== */
    /* Transiciones suaves para elementos interactivos */
    .stButton > button,
    .stSelectbox > div,
    .stRadio > div > label {
        transition: all 0.3s ease;
    }

    /* Animación de carga suave */
    .stSpinner {
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
    """, unsafe_allow_html=True)
