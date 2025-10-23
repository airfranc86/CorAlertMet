"""
Componente simplificado para iconos SVG
Versión compatible con Streamlit Cloud
"""
import streamlit as st

def show_svg_icon(icon_name, width=24, height=24, animation="smoothBlink", color="#3B82F6"):
    """
    Mostrar icono SVG simplificado
    
    Args:
        icon_name: Nombre del icono
        width: Ancho en píxeles
        height: Alto en píxeles
        animation: Tipo de animación CSS
        color: Color del icono
    """
    
    # Iconos SVG básicos
    svg_icons = {
        "user": f"""
        <svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" stroke="{color}" stroke-width="2" fill="none"/>
            <circle cx="12" cy="7" r="4" stroke="{color}" stroke-width="2" fill="none"/>
        </svg>
        """,
        
        "check-circle": f"""
        <svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
            <path d="M22 4 12 14.01l-3-3" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
        </svg>
        """,
        
        "alert-circle": f"""
        <svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="10" stroke="{color}" stroke-width="2" fill="none"/>
            <path d="M12 8v4" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
            <circle cx="12" cy="16" r="1" fill="{color}"/>
        </svg>
        """,
        
        "info": f"""
        <svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="10" stroke="{color}" stroke-width="2" fill="none"/>
            <path d="M12 16v-4" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
            <path d="M12 8h.01" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
        </svg>
        """,
        
        "home": f"""
        <svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" stroke="{color}" stroke-width="2" fill="none"/>
            <path d="M9 22V12h6v10" stroke="{color}" stroke-width="2" fill="none"/>
        </svg>
        """,
        
        "map": f"""
        <svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M1 6v16l7-4 8 4 7-4V2l-7 4-8-4-7 4z" stroke="{color}" stroke-width="2" fill="none"/>
            <path d="M8 2v16" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
            <path d="M16 6v16" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
        </svg>
        """,
        
        "cloud": f"""
        <svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z" stroke="{color}" stroke-width="2" fill="none"/>
        </svg>
        """,
        
        "sun": f"""
        <svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="5" stroke="{color}" stroke-width="2" fill="none"/>
            <path d="M12 1v2" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
            <path d="M12 21v2" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
            <path d="M4.22 4.22l1.42 1.42" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
            <path d="M18.36 18.36l1.42 1.42" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
            <path d="M1 12h2" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
            <path d="M21 12h2" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
            <path d="M4.22 19.78l1.42-1.42" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
            <path d="M18.36 5.64l1.42-1.42" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
        </svg>
        """
    }
    
    # Mostrar el icono
    if icon_name in svg_icons:
        svg_content = svg_icons[icon_name]
        st.markdown(svg_content, unsafe_allow_html=True)
    else:
        # Fallback para iconos no encontrados
        st.markdown(
            f'<div style="font-size: {width}px; text-align: center;">❓</div>',
            unsafe_allow_html=True
        )

def get_animation_types():
    """Obtener tipos de animación disponibles"""
    return ["smoothBlink", "gentlePulse", "softBounce", "smoothRotate"]

def get_icon_colors():
    """Obtener colores disponibles"""
    return {
        "blue": "#3B82F6",
        "green": "#10B981", 
        "red": "#EF4444",
        "yellow": "#F59E0B",
        "purple": "#8B5CF6",
        "gray": "#6B7280"
    }
