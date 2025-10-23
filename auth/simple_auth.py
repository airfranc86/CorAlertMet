"""
Sistema de Autenticación Simple para CorAlertIntel
Solo admin e invitado con contraseñas desde .env
Basado en mejores prácticas de Streamlit
"""
import streamlit as st
import hmac
import os
import logging
from datetime import datetime
from typing import Optional, Dict, Any
from config.logging_config import get_auth_logger

# Configurar logger de autenticación
auth_logger = get_auth_logger()

class SimpleAuth:
    """Sistema de autenticación simple con admin e invitado"""

    def __init__(self):
        # Debug completo de Streamlit Secrets
        st.write("🔍 **DEBUG COMPLETO DE STREAMLIT SECRETS:**")
        
        # Mostrar todas las claves disponibles
        try:
            st.write("📋 **Claves disponibles en st.secrets:**")
            for key in st.secrets.keys():
                st.write(f"- {key}")
        except Exception as e:
            st.write(f"❌ Error al leer claves: {e}")
        
        # Verificar si existe la sección secrets
        try:
            if hasattr(st.secrets, 'secrets'):
                st.write("✅ Sección 'secrets' encontrada")
            else:
                st.write("❌ Sección 'secrets' NO encontrada")
        except Exception as e:
            st.write(f"❌ Error al verificar sección secrets: {e}")
        
        # Intentar leer las contraseñas con diferentes métodos
        try:
            # Método 1: Acceso directo
            admin_pass = st.secrets["ADMIN_PASSWORD"]
            guest_pass = st.secrets["GUEST_PASSWORD"]
            st.write("✅ Contraseñas leídas con método directo")
        except KeyError:
            try:
                # Método 2: Acceso a través de la sección secrets
                admin_pass = st.secrets.secrets["ADMIN_PASSWORD"]
                guest_pass = st.secrets.secrets["GUEST_PASSWORD"]
                st.write("✅ Contraseñas leídas con método secrets.secrets")
            except KeyError as e:
                st.error(f"⚠️ **Error de configuración**: No se encontró la variable {e} en Streamlit Secrets.")
                st.info("Por favor, configura estas variables en Streamlit Cloud Secrets.")
                st.stop()
            except Exception as e:
                st.error(f"❌ **Error inesperado**: {e}")
                st.stop()
        except Exception as e:
            st.error(f"❌ **Error inesperado**: {e}")
            st.stop()
            
        self.users = {
            'admin': admin_pass,
            'invitado': guest_pass
        }

        # Inicializar estado de sesión
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'user_role' not in st.session_state:
            st.session_state.user_role = None
        if 'login_attempts' not in st.session_state:
            st.session_state.login_attempts = 0
        if 'last_attempt' not in st.session_state:
            st.session_state.last_attempt = None

    def check_password(self, username: str, password: str) -> bool:
        """
        Verifica credenciales usando comparación segura con HMAC

        Args:
            username: Nombre de usuario (admin o invitado)
            password: Contraseña ingresada

        Returns:
            bool: True si las credenciales son correctas
        """
        try:
            if username not in self.users:
                auth_logger.warning(f"Intento de login con usuario inexistente: {username}")
                return False

            stored_password = self.users[username]
            if not stored_password:
                auth_logger.error(f"Contraseña no configurada para usuario: {username}")
                return False

            # Comparación segura con HMAC
            is_valid = hmac.compare_digest(password, stored_password)

            if is_valid:
                auth_logger.info(f"Login exitoso para usuario: {username}")
            else:
                auth_logger.warning(f"Login fallido para usuario: {username}")

            return is_valid

        except Exception as e:
            auth_logger.error(f"Error verificando credenciales: {str(e)}")
            return False

    def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        Procesa el login del usuario

        Args:
            username: Nombre de usuario
            password: Contraseña

        Returns:
            Dict con resultado del login
        """
        try:
            # Verificar intentos de login
            if self._is_account_locked():
                return {
                    "success": False,
                    "error": "Demasiados intentos fallidos (máximo 10). Intenta más tarde."
                }

            # Validar entrada
            if not username or not password:
                return {
                    "success": False,
                    "error": "Usuario y contraseña son requeridos"
                }

            # Verificar credenciales
            if self.check_password(username, password):
                # Login exitoso
                st.session_state.authenticated = True
                st.session_state.user_role = username
                st.session_state.login_attempts = 0
                st.session_state.last_attempt = None

                # Configurar cookie segura
                self._set_secure_cookie(username)

                auth_logger.info(f"Usuario {username} autenticado exitosamente")

                return {
                    "success": True,
                    "user": username,
                    "message": f"¡Bienvenido {username}!"
                }
            else:
                # Login fallido
                self._record_failed_attempt()

                return {
                    "success": False,
                    "error": "Error en la contraseña o el usuario"
                }

        except Exception as e:
            auth_logger.error(f"Error en login: {str(e)}")
            return {
                "success": False,
                "error": "Error interno del servidor"
            }

    def logout(self) -> None:
        """Cierra la sesión del usuario"""
        try:
            if st.session_state.authenticated:
                user = st.session_state.user_role
                auth_logger.info(f"Usuario {user} cerró sesión")

            # Limpiar estado de sesión
            st.session_state.authenticated = False
            st.session_state.user_role = None
            st.session_state.login_attempts = 0
            st.session_state.last_attempt = None

            # Limpiar cookie
            self._clear_cookie()

        except Exception as e:
            auth_logger.error(f"Error en logout: {str(e)}")

    def is_authenticated(self) -> bool:
        """Verifica si el usuario está autenticado"""
        return st.session_state.get('authenticated', False)

    def get_current_user(self) -> Optional[str]:
        """Obtiene el usuario actual"""
        if self.is_authenticated():
            return st.session_state.get('user_role')
        return None

    def _is_account_locked(self) -> bool:
        """Verifica si la cuenta está bloqueada por intentos fallidos"""
        max_attempts = 10
        lockout_duration = 180  # 3 minutos

        if st.session_state.login_attempts >= max_attempts:
            if st.session_state.last_attempt:
                time_since_attempt = (
                    datetime.now() - st.session_state.last_attempt
                ).total_seconds()
                if time_since_attempt < lockout_duration:
                    return True
                else:
                    # Desbloquear cuenta
                    st.session_state.login_attempts = 0
                    st.session_state.last_attempt = None

        return False

    def _record_failed_attempt(self) -> None:
        """Registra un intento fallido de login"""
        st.session_state.login_attempts += 1
        st.session_state.last_attempt = datetime.now()

        auth_logger.warning(f"Intento fallido #{st.session_state.login_attempts}")

    def _set_secure_cookie(self, username: str) -> None:
        """Configura cookie segura para la sesión"""
        try:
            # Crear cookie con información básica
            cookie_data = {
                'user': username,
                'timestamp': datetime.now().isoformat(),
                'authenticated': True
            }

            # En Streamlit, usamos session_state para simular cookies seguras
            st.session_state['secure_session'] = cookie_data

        except Exception as e:
            auth_logger.error(f"Error configurando cookie: {str(e)}")

    def _clear_cookie(self) -> None:
        """Limpia la cookie de sesión"""
        if 'secure_session' in st.session_state:
            del st.session_state['secure_session']

    def has_permission(self, permission: str) -> bool:
        """
        Verifica si el usuario actual tiene un permiso específico

        Args:
            permission: Permiso a verificar ('admin', 'invitado', 'ml_advanced')

        Returns:
            bool: True si tiene el permiso
        """
        if not st.session_state.get('authenticated', False):
            return False

        user_role = st.session_state.get('user_role', None)

        if permission == 'admin':
            return user_role == 'admin'
        elif permission == 'invitado':
            return user_role == 'invitado'
        elif permission == 'ml_advanced':
            # Solo admin puede acceder a funcionalidades avanzadas de ML
            return user_role == 'admin'
        else:
            return False

    def get_user_permissions(self) -> list:
        """
        Obtiene la lista de permisos del usuario actual

        Returns:
            list: Lista de permisos disponibles
        """
        if not st.session_state.get('authenticated', False):
            return []

        user_role = st.session_state.get('user_role', None)

        if user_role == 'admin':
            return ['admin', 'ml_advanced', 'ml_basic']
        elif user_role == 'invitado':
            return ['invitado', 'ml_basic']
        else:
            return []

def show_login_form() -> None:
    """Muestra el formulario de login"""
    # Header con icono SVG profesional
    col1, col2 = st.columns([1, 20])
    with col1:
        from components.svg_icons_simple import show_svg_icon
        show_svg_icon("user", width=48, height=48, animation="gentlePulse", color="#3B82F6")
    with col2:
        st.markdown("## Acceso al Sistema")

    st.markdown("**CorAlertMet Intelligence - Sistema de Alertas Meteorológicas**")

    with st.form("login_form"):
        st.markdown("### Iniciar Sesión")

        # Selector de usuario
        username = st.selectbox(
            "Usuario:",
            ["", "admin", "invitado"],
            help="Selecciona tu tipo de usuario"
        )

        # Campo de contraseña
        password = st.text_input(
            "Contraseña:",
            type="password",
            help="Ingresa tu contraseña"
        )

        # Botón de login
        submitted = st.form_submit_button(
            "Iniciar Sesión",
            type="primary",
            use_container_width=True
        )

        if submitted:
            if username and password and username != "":
                auth = SimpleAuth()
                result = auth.login(username, password)

                if result["success"]:
                    # Éxito con icono
                    col1, col2 = st.columns([1, 20])
                    with col1:
                        show_svg_icon(
                            "check-circle", width=24, height=24, 
                            animation="softBounce", color="#10B981"
                        )
                    with col2:
                        st.success(result["message"])
                    st.rerun()
                else:
                    # Error con icono
                    col1, col2 = st.columns([1, 20])
                    with col1:
                        show_svg_icon(
                            "alert-circle", width=24, height=24, 
                            animation="smoothBlink", color="#EF4444"
                        )
                    with col2:
                        st.error(result["error"])
            else:
                # Warning con icono
                col1, col2 = st.columns([1, 20])
                with col1:
                    show_svg_icon(
                        "info", width=24, height=24, 
                        animation="gentlePulse", color="#F59E0B"
                    )
                with col2:
                    st.warning("Por favor selecciona un usuario e ingresa la contraseña")

def show_logout_section() -> None:
    """Muestra la sección de logout en el sidebar"""
    with st.sidebar:
        st.markdown("---")
        # Mostrar usuario actual
        auth = SimpleAuth()
        current_user = auth.get_current_user()
        if current_user:
            st.success(f"Conectado como: **{current_user}**")

            # Botón de logout
            if st.button("Cerrar Sesión", type="secondary", use_container_width=True):
                auth.logout()
                st.success("Sesión cerrada")
                st.rerun()
        else:
            st.warning("No autenticado")

def require_auth(func):
    """Decorator para requerir autenticación en funciones"""
    def wrapper(*args, **kwargs):
        auth = SimpleAuth()
        if not auth.is_authenticated():
            show_login_form()
            st.stop()
        return func(*args, **kwargs)
    return wrapper

# Instancia global del sistema de autenticación
auth_system = SimpleAuth()
