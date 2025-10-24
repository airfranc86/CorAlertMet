"""
Footer component for CorAlertMet Intelligence
"""
import streamlit as st
import base64
from pathlib import Path
try:
    from config.version import get_version
except ImportError:
    def get_version():
        return "2.3.0"

def show_footer():
    """Mostrar footer profesional con logo integrado"""
    st.markdown("---")

    # Obtener versión centralizada
    version = get_version()

    logo_path = Path("data/icon.png")
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            logo_data = f.read()
            logo_base64 = base64.b64encode(logo_data).decode("utf-8")
            logo_url = f"data:image/png;base64,{logo_base64}"
    else:
        logo_url = "https://static.streamlit.io/examples/logo.png"  # fallback

    footer_html = f"""
    <div class="footer-fixed" style="
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 6px 15px;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.2);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        z-index: 1000;
        border-top: 1px solid rgba(255,255,255,0.1);
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; 
                    flex-wrap: wrap; gap: 15px; max-width: 1200px; margin: 0 auto;">
            <div style="display: flex; align-items: center; gap: 8px; flex: 1; min-width: 150px;">
                <img src="{logo_url}" alt="CorAlertMet Intelligence" style="width: 24px; height: 24px; border-radius: 4px; box-shadow: 0 1px 3px rgba(
                    0,
                    0,
                    0,
                    0.2); object-fit: cover;">
                <div>
                    <span style="color: white; font-size: 0.9em; font-weight: 600;">CorAlertMet Intelligence</span>
                    <span style="color: #e0e0e0; font-size: 0.7em; margin-left: 8px;">v{version}</span>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
                <div style="display: flex; gap: 6px; align-items: center;">
                    <span style="background: rgba(
                        255,
                        255,
                        255,
                        0.2); padding: 2px 8px; border-radius: 10px; font-size: 0.7em; font-weight: 500;">ML</span>
                    <span style="background: rgba(
                        0,
                        255,
                        0,
                        0.2); padding: 2px 8px; border-radius: 10px; font-size: 0.7em; font-weight: 500;">Activo</span>
                </div>
                <span style="color: #b0b0b0; font-size: 0.7em;">© 2025 F. Aucar</span>
            </div>
        </div>
    </div>

    <!-- Espaciado para evitar que el contenido se oculte detrás del footer fijo -->
    <div style="height: 50px; margin-top: 20px;"></div>

    <style>
    /* Footer fijo responsivo */
    .footer-fixed {{
        transition: all 0.3s ease;
    }}

    @media (max-width: 768px) {{
        .footer-fixed {{
            padding: 4px 10px;
        }}
        .footer-fixed > div {{
            flex-direction: column !important;
            gap: 8px !important;
            text-align: center !important;
        }}
        .footer-fixed > div > div {{
            justify-content: center !important;
        }}
        .footer-fixed img {{
            width: 20px !important;
            height: 20px !important;
        }}
        .footer-fixed span {{
            font-size: 0.65em !important;
        }}
    }}

    @media (max-width: 480px) {{
        .footer-fixed {{
            padding: 3px 8px;
        }}
        .footer-fixed > div {{
            gap: 5px !important;
        }}
        .footer-fixed img {{
            width: 18px !important;
            height: 18px !important;
        }}
    }}

    /* Ajustar contenido principal para el footer fijo */
    .main .block-container {{
        padding-bottom: 60px !important;
    }}
    </style>
    """
    st.markdown(footer_html, unsafe_allow_html=True)
