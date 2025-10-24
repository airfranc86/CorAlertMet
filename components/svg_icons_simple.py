"""
Componente simplificado para iconos SVG
Versión compatible con Streamlit Cloud
"""
import streamlit as st

def show_svg_icon(icon_name, width=24, height=24, animation="none", color="#3B82F6"):
    """
    Mostrar icono SVG simplificado
    
    Args:
        icon_name: Nombre del icono
        width: Ancho en píxeles
        height: Alto en píxeles
        animation: Tipo de animación CSS (ignorado por compatibilidad)
        color: Color del icono
    """
    
    # Iconos SVG básicos y funcionales
    svg_icons = {
        "user": f'<svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" stroke="{color}" stroke-width="2" fill="none"/><circle cx="12" cy="7" r="4" stroke="{color}" stroke-width="2" fill="none"/></svg>',
        
        "check-circle": f'<svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" stroke="{color}" stroke-width="2" stroke-linecap="round"/><path d="M22 4 12 14.01l-3-3" stroke="{color}" stroke-width="2" stroke-linecap="round"/></svg>',
        
        "alert-circle": f'<svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="10" stroke="{color}" stroke-width="2" fill="none"/><path d="M12 8v4" stroke="{color}" stroke-width="2" stroke-linecap="round"/><circle cx="12" cy="16" r="1" fill="{color}"/></svg>',
        
        "info": f'<svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="10" stroke="{color}" stroke-width="2" fill="none"/><path d="M12 16v-4" stroke="{color}" stroke-width="2" stroke-linecap="round"/><path d="M12 8h.01" stroke="{color}" stroke-width="2" stroke-linecap="round"/></svg>',
        
        "home": f'<svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" stroke="{color}" stroke-width="2" fill="none"/><path d="M9 22V12h6v10" stroke="{color}" stroke-width="2" fill="none"/></svg>',
        
        "map": f'<svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M1 6v16l7-4 8 4 7-4V2l-7 4-8-4-7 4z" stroke="{color}" stroke-width="2" fill="none"/><path d="M8 2v16" stroke="{color}" stroke-width="2" stroke-linecap="round"/><path d="M16 6v16" stroke="{color}" stroke-width="2" stroke-linecap="round"/></svg>',
        
        "cloud": f'<svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z" stroke="{color}" stroke-width="2" fill="none"/></svg>',
        
        "sun": f'<svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="5" stroke="{color}" stroke-width="2" fill="none"/><path d="M12 1v2" stroke="{color}" stroke-width="2" stroke-linecap="round"/><path d="M12 21v2" stroke="{color}" stroke-width="2" stroke-linecap="round"/><path d="M4.22 4.22l1.42 1.42" stroke="{color}" stroke-width="2" stroke-linecap="round"/><path d="M18.36 18.36l1.42 1.42" stroke="{color}" stroke-width="2" stroke-linecap="round"/><path d="M1 12h2" stroke="{color}" stroke-width="2" stroke-linecap="round"/><path d="M21 12h2" stroke="{color}" stroke-width="2" stroke-linecap="round"/><path d="M4.22 19.78l1.42-1.42" stroke="{color}" stroke-width="2" stroke-linecap="round"/><path d="M18.36 5.64l1.42-1.42" stroke="{color}" stroke-width="2" stroke-linecap="round"/></svg>',
        
        "book": f'<svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" stroke="{color}" stroke-width="2" fill="none"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" stroke="{color}" stroke-width="2" fill="none"/></svg>',
        
        "thermometer": f'<svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0Z" stroke="{color}" stroke-width="2" fill="none"/></svg>',
        
        "wind": f'<svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M17.7 7.7a2.5 2.5 0 1 1 1.8 4.3H2" stroke="{color}" stroke-width="2" fill="none"/><path d="M9.6 4.6A2 2 0 1 1 11 8H2" stroke="{color}" stroke-width="2" fill="none"/><path d="M12.6 19.4A2 2 0 1 0 14 16H2" stroke="{color}" stroke-width="2" fill="none"/></svg>',
        
        "droplet": f'<svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z" stroke="{color}" stroke-width="2" fill="none"/></svg>',
        
        "gauge": f'<svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 14l3-3" stroke="{color}" stroke-width="2" stroke-linecap="round"/><path d="M12 2a10 10 0 1 0 10 10" stroke="{color}" stroke-width="2" fill="none"/></svg>',
        
        "refresh": f'<svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8" stroke="{color}" stroke-width="2" fill="none"/><path d="M21 3v5h-5" stroke="{color}" stroke-width="2" fill="none"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16" stroke="{color}" stroke-width="2" fill="none"/><path d="M3 21v-5h5" stroke="{color}" stroke-width="2" fill="none"/></svg>',
        
        "brain": f'<svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1 .34-4.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 1.98-3A2.5 2.5 0 0 1 9.5 2Z" stroke="{color}" stroke-width="2" fill="none"/><path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0-.34-4.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-1.98-3A2.5 2.5 0 0 0 14.5 2Z" stroke="{color}" stroke-width="2" fill="none"/></svg>',
        
        "compass": f'<svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="10" stroke="{color}" stroke-width="2" fill="none"/><path d="M16.24 7.76l-2.12 6.36-6.36 2.12 2.12-6.36 6.36-2.12z" stroke="{color}" stroke-width="2" fill="none"/></svg>',
        
        "search": f'<svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="11" cy="11" r="8" stroke="{color}" stroke-width="2" fill="none"/><path d="M21 21l-4.35-4.35" stroke="{color}" stroke-width="2" stroke-linecap="round"/></svg>',
        
        "mail": f'<svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" stroke="{color}" stroke-width="2" fill="none"/><path d="M22 6l-10 7L2 6" stroke="{color}" stroke-width="2" stroke-linecap="round"/></svg>',
        
        "cloud-sun": f'<svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z" stroke="{color}" stroke-width="2" fill="none"/><circle cx="12" cy="12" r="4" stroke="{color}" stroke-width="2" fill="none"/></svg>',
        
        "bar-chart-3": f'<svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 3v18h18" stroke="{color}" stroke-width="2" stroke-linecap="round"/><path d="M18 17V9" stroke="{color}" stroke-width="2" stroke-linecap="round"/><path d="M13 17V5" stroke="{color}" stroke-width="2" stroke-linecap="round"/><path d="M8 17v-3" stroke="{color}" stroke-width="2" stroke-linecap="round"/></svg>',
        
        "alert-triangle": f'<svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" stroke="{color}" stroke-width="2" fill="none"/><path d="M12 9v4" stroke="{color}" stroke-width="2" stroke-linecap="round"/><path d="M12 17h.01" stroke="{color}" stroke-width="2" stroke-linecap="round"/></svg>',
        
        "clock": f'<svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="10" stroke="{color}" stroke-width="2" fill="none"/><path d="M12 6v6l4 2" stroke="{color}" stroke-width="2" stroke-linecap="round"/></svg>',
        
        "cloud-lightning": f'<svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z" stroke="{color}" stroke-width="2" fill="none"/><path d="M13 10l-4 6h6l-4 6" stroke="{color}" stroke-width="2" stroke-linecap="round"/></svg>'
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
    return ["none", "pulse", "rotate", "bounce"]

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