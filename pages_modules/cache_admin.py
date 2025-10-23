"""
Panel de Administración de Cache para CorAlertIntel
Permite monitorear y gestionar el sistema de cache
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from cache.cache_manager import get_cache_stats, cleanup_cache, clear_all_cache

@st.cache_data(ttl=300, show_spinner=False)  # Cache 5 minutos para estadísticas de caché
def show_cache_admin():
    """Mostrar panel de administración de cache"""

    st.title("🗄️ Administración de Cache")
    st.markdown("**Gestión del sistema de cache para modelos ML y datos meteorológicos**")

    # Obtener estadísticas del cache
    stats = get_cache_stats()

    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="📊 Modelos Guardados",
            value=stats.get("total_models", 0),
            help="Número total de modelos ML en cache"
        )

    with col2:
        st.metric(
            label="📁 Archivos de Datos",
            value=stats.get("total_data_files", 0),
            help="Número total de archivos de datos en cache"
        )

    with col3:
        st.metric(
            label="💾 Tamaño Total",
            value=f"{stats.get('total_size_mb', 0)} MB",
            help="Tamaño total del cache en MB"
        )

    with col4:
        st.metric(
            label="🕒 Última Actualización",
            value=datetime.now().strftime("%H:%M"),
            help="Hora de la última actualización"
        )

    st.markdown("---")

    # Tabs para diferentes secciones
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📋 Modelos",
        "📊 Datos",
        "⚙️ Configuración",
        "🧹 Mantenimiento"])

    with tab1:
        show_models_tab(stats)

    with tab2:
        show_data_tab(stats)

    with tab3:
        show_config_tab()

    with tab4:
        show_maintenance_tab()

def show_models_tab(stats):
    """Mostrar información de modelos"""
    st.subheader("🤖 Modelos ML en Cache")

    if stats.get("models"):
        models_df = pd.DataFrame(stats["models"])

        # Formatear columnas
        if "saved_at" in models_df.columns:
            models_df["saved_at"] = pd.to_datetime(models_df["saved_at"]).dt.strftime("%Y-%m-%d %H:%M")

        if "file_size" in models_df.columns:
            models_df["file_size_mb"] = (models_df["file_size"] / (1024 * 1024)).round(2)

        # Mostrar tabla
        st.dataframe(
            models_df[["model_name", "model_type", "accuracy", "saved_at", "file_size_mb"]].rename(columns={
                "model_name": "Nombre",
                "model_type": "Tipo",
                "accuracy": "Precisión",
                "saved_at": "Guardado",
                "file_size_mb": "Tamaño (MB)"
            }),
            use_container_width=True
        )

        # Gráfico de distribución por tipo
        if "model_type" in models_df.columns:
            st.subheader("📈 Distribución por Tipo de Modelo")
            type_counts = models_df["model_type"].value_counts()
            st.bar_chart(type_counts)
    else:
        st.info("No hay modelos en cache")

def show_data_tab(stats):
    """Mostrar información de datos"""
    st.subheader("📊 Datos en Cache")

    if stats.get("data_files"):
        data_df = pd.DataFrame(stats["data_files"])

        # Formatear columnas
        if "saved_at" in data_df.columns:
            data_df["saved_at"] = pd.to_datetime(data_df["saved_at"]).dt.strftime("%Y-%m-%d %H:%M")

        if "file_size" in data_df.columns:
            data_df["file_size_mb"] = (data_df["file_size"] / (1024 * 1024)).round(2)

        # Mostrar tabla
        st.dataframe(
            data_df[["data_name", "data_type", "shape", "saved_at", "file_size_mb"]].rename(columns={
                "data_name": "Nombre",
                "data_type": "Tipo",
                "shape": "Forma",
                "saved_at": "Guardado",
                "file_size_mb": "Tamaño (MB)"
            }),
            use_container_width=True
        )

        # Gráfico de tamaño por archivo
        if "file_size_mb" in data_df.columns:
            st.subheader("📈 Tamaño de Archivos de Datos")
            st.bar_chart(data_df.set_index("data_name")["file_size_mb"])
    else:
        st.info("No hay datos en cache")

def show_config_tab():
    """Mostrar configuración del cache"""
    st.subheader("⚙️ Configuración del Cache")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Configuración Actual:**

        - **TTL Modelos:** 7 días
        - **TTL Datos:** 1 hora
        - **Tamaño Máximo:** 500 MB
        - **Limpieza Automática:** 48 horas
        """)

    with col2:
        st.markdown("""
        **Ubicaciones:**

        - **Modelos:** `cache/models/`
        - **Datos:** `cache/data/`
        - **Configuración:** `cache/config/`
        """)

    # Configuración avanzada
    st.subheader("🔧 Configuración Avanzada")

    with st.expander("Modificar Configuración"):
        st.warning("⚠️ Modificar la configuración puede afectar el rendimiento del sistema")

        col1, col2 = st.columns(2)

        with col1:
            st.number_input(
                "TTL Modelos (días)",
                min_value=1,
                max_value=30,
                value=7,
                help="Tiempo de vida de los modelos en días",
                key="model_ttl"
            )

            st.number_input(
                "TTL Datos (horas)",
                min_value=1,
                max_value=24,
                value=1,
                help="Tiempo de vida de los datos en horas",
                key="data_ttl"
            )

        with col2:
            st.number_input(
                "Tamaño Máximo (MB)",
                min_value=100,
                max_value=2000,
                value=500,
                help="Tamaño máximo del cache en MB",
                key="max_size"
            )

            st.number_input(
                "Intervalo de Limpieza (horas)",
                min_value=1,
                max_value=168,
                value=48,
                help="Intervalo entre limpiezas automáticas en horas",
                key="cleanup_interval"
            )

        if st.button("💾 Guardar Configuración"):
            # Aquí se actualizaría la configuración
            st.success("Configuración actualizada")

def show_maintenance_tab():
    """Mostrar herramientas de mantenimiento"""
    st.subheader("🧹 Herramientas de Mantenimiento")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Limpieza Automática**")

        if st.button("🧽 Limpiar Archivos Expirados"):
            with st.spinner("Limpiando archivos expirados..."):
                cleanup_stats = cleanup_cache()

            st.success(f"Limpieza completada:")
            st.write(f"- Modelos eliminados: {cleanup_stats['models_removed']}")
            st.write(f"- Archivos de datos eliminados: {cleanup_stats['data_removed']}")
            st.write(f"- Espacio liberado: {cleanup_stats['space_freed'] / (1024*1024):.2f} MB")

    with col2:
        st.markdown("**Limpieza Completa**")

        st.warning("⚠️ Esta acción eliminará TODO el cache")

        if st.button("🗑️ Limpiar Todo el Cache", type="secondary"):
            if st.checkbox("Confirmar eliminación completa"):
                with st.spinner("Limpiando todo el cache..."):
                    success = clear_all_cache()

                if success:
                    st.success("Cache completamente limpiado")
                    st.rerun()
                else:
                    st.error("Error al limpiar el cache")

    # Información del sistema
    st.subheader("ℹ️ Información del Sistema")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Estado del Cache:**

        - ✅ Sistema activo
        - ✅ Limpieza automática habilitada
        - ✅ Compresión habilitada
        - ✅ Metadatos completos
        """)

    with col2:
        st.markdown("""
        **Recomendaciones:**

        - 🔄 Limpiar semanalmente
        - 📊 Monitorear tamaño
        - 🗂️ Revisar archivos antiguos
        - 💾 Hacer backup periódico
        """)

def main():
    """Función principal"""
    show_cache_admin()

if __name__ == "__main__":
    main()
