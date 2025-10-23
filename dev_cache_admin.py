"""
Script de Desarrollo - Panel de Administración de Cache
Solo para uso local durante el desarrollo
NO incluir en deploy de producción
"""

import streamlit as st
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(__file__))

# Importar el panel de administración de cache
from pages_modules.cache_admin import show_cache_admin

# Configuración de la página
st.set_page_config(
    page_title="Cache Admin - CorAlertIntel Dev",
    page_icon="data/icon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Función principal del panel de administración de cache"""

    # Header de desarrollo
    st.markdown("""
<div style = (
        "background-color: #f0f9ff; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;">
    )
        <h3 style="color: #1e40af; margin: 0;">🔧 Panel de Administración de Cache - DESARROLLO LOCAL</h3>
<p style = (
            "color: #1e40af; margin: 0.5rem 0 0 0;">Solo disponible para desarrollo. NO incluir en deploy de producción.</p>
        )
    </div>
    """, unsafe_allow_html=True)

    # Mostrar el panel de administración
    show_cache_admin()

    # Footer de desarrollo
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6b7280; font-size: 0.9rem;">
        <p><strong>⚠️ ADVERTENCIA:</strong> Este panel es solo para desarrollo local.</p>
        <p>Los archivos de cache NO se incluyen en el repositorio GitHub.</p>
        <p>En producción, los modelos se entrenan desde cero en cada deploy.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
