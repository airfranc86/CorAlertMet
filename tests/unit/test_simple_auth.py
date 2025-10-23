"""
Tests unitarios para auth/simple_auth.py
Sistema de autenticación con HMAC y protección anti-fuerza bruta
"""
import pytest
import os
import hmac
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Importar el módulo a testear
from auth.simple_auth import SimpleAuth, show_login_form, show_logout_section, require_auth


class TestSimpleAuth:
    """Tests para la clase SimpleAuth"""
    
    def test_init_default_values(self):
        """Test inicialización con valores por defecto"""
        auth = SimpleAuth()
        
        assert 'admin' in auth.users
        assert 'invitado' in auth.users
        assert auth.users['admin'] == os.getenv('ADMIN_PASSWORD', '')
        assert auth.users['invitado'] == os.getenv('GUEST_PASSWORD', '')
    
    def test_check_password_valid(self, mock_streamlit_session):
        """Test verificación de contraseña válida con HMAC"""
        auth = SimpleAuth()
        
        # Configurar contraseñas de test
        auth.users['admin'] = 'test_password'
        
        # Test con contraseña correcta
        result = auth.check_password('admin', 'test_password')
        assert result is True
    
    def test_check_password_invalid(self, mock_streamlit_session):
        """Test verificación de contraseña inválida"""
        auth = SimpleAuth()
        
        # Configurar contraseñas de test
        auth.users['admin'] = 'test_password'
        
        # Test con contraseña incorrecta
        result = auth.check_password('admin', 'wrong_password')
        assert result is False
    
    def test_check_password_nonexistent_user(self, mock_streamlit_session):
        """Test verificación con usuario inexistente"""
        auth = SimpleAuth()
        
        result = auth.check_password('nonexistent', 'any_password')
        assert result is False
    
    def test_check_password_empty_credentials(self, mock_streamlit_session):
        """Test verificación con credenciales vacías"""
        auth = SimpleAuth()
        
        result = auth.check_password('', '')
        assert result is False
        
        result = auth.check_password('admin', '')
        assert result is False
    
    @patch('auth.simple_auth.st.session_state')
    def test_login_success(self, mock_session_state):
        """Test login exitoso"""
        auth = SimpleAuth()
        auth.users['admin'] = 'test_password'
        
        result = auth.login('admin', 'test_password')
        
        assert result['success'] is True
        assert result['user'] == 'admin'
        assert 'Bienvenido' in result['message']
        assert mock_session_state.authenticated is True
        assert mock_session_state.user_role == 'admin'
        assert mock_session_state.login_attempts == 0
    
    @patch('auth.simple_auth.st.session_state')
    def test_login_failed_attempts(self, mock_session_state):
        """Test protección anti-fuerza bruta (5 intentos)"""
        auth = SimpleAuth()
        auth.users['admin'] = 'test_password'
        
        # Simular 5 intentos fallidos
        for i in range(5):
            result = auth.login('admin', 'wrong_password')
            assert result['success'] is False
            assert mock_session_state.login_attempts == i + 1
        
        # 6to intento debería estar bloqueado
        result = auth.login('admin', 'wrong_password')
        assert result['success'] is False
        assert 'Demasiados intentos' in result['error']
    
    @patch('auth.simple_auth.st.session_state')
    def test_account_lockout(self, mock_session_state):
        """Test bloqueo temporal de cuenta (5 minutos)"""
        auth = SimpleAuth()
        auth.users['admin'] = 'test_password'
        
        # Simular 5 intentos fallidos
        for i in range(5):
            auth.login('admin', 'wrong_password')
        
        # Verificar que la cuenta está bloqueada
        assert auth._is_account_locked() is True
        
        # Simular que han pasado 6 minutos
        mock_session_state.last_attempt = datetime.now() - timedelta(minutes=6)
        assert auth._is_account_locked() is False
    
    @patch('auth.simple_auth.st.session_state')
    def test_logout(self, mock_session_state):
        """Test logout correcto"""
        auth = SimpleAuth()
        
        # Simular usuario autenticado
        mock_session_state.authenticated = True
        mock_session_state.user_role = 'admin'
        mock_session_state.login_attempts = 3
        mock_session_state.last_attempt = datetime.now()
        mock_session_state.secure_session = {'user': 'admin'}
        
        auth.logout()
        
        assert mock_session_state.authenticated is False
        assert mock_session_state.user_role is None
        assert mock_session_state.login_attempts == 0
        assert mock_session_state.last_attempt is None
        assert 'secure_session' not in mock_session_state
    
    @patch('auth.simple_auth.st.session_state')
    def test_is_authenticated(self, mock_session_state):
        """Test verificación de estado de autenticación"""
        auth = SimpleAuth()
        
        # Usuario no autenticado
        mock_session_state.get.return_value = False
        assert auth.is_authenticated() is False
        
        # Usuario autenticado
        mock_session_state.get.return_value = True
        assert auth.is_authenticated() is True
    
    @patch('auth.simple_auth.st.session_state')
    def test_get_current_user(self, mock_session_state):
        """Test obtención de usuario actual"""
        auth = SimpleAuth()
        
        # Usuario no autenticado
mock_session_state.get.side_effect = (
            lambda key, default=None: False if key == 'authenticated' else default
        )
        assert auth.get_current_user() is None
        
        # Usuario autenticado
        mock_session_state.get.side_effect = lambda key, default=None: True if key == 'authenticated' else ('admin' if key == 'user_role' else default)
        assert auth.get_current_user() == 'admin'
    
    @patch('auth.simple_auth.st.session_state')
    def test_has_permission_admin(self, mock_session_state):
        """Test permisos de administrador"""
        auth = SimpleAuth()
        
        # Usuario no autenticado
        mock_session_state.authenticated = False
        assert auth.has_permission('admin') is False
        
        # Usuario invitado
        mock_session_state.authenticated = True
        mock_session_state.user_role = 'invitado'
        assert auth.has_permission('admin') is False
        
        # Usuario admin
        mock_session_state.user_role = 'admin'
        assert auth.has_permission('admin') is True
        assert auth.has_permission('ml_advanced') is True
    
    @patch('auth.simple_auth.st.session_state')
    def test_has_permission_guest(self, mock_session_state):
        """Test permisos de invitado"""
        auth = SimpleAuth()
        
        # Usuario invitado
        mock_session_state.authenticated = True
        mock_session_state.user_role = 'invitado'
        assert auth.has_permission('invitado') is True
        assert auth.has_permission('ml_basic') is True
        assert auth.has_permission('admin') is False
        assert auth.has_permission('ml_advanced') is False
    
    def test_get_user_permissions(self, mock_streamlit_session):
        """Test obtención de permisos del usuario"""
        auth = SimpleAuth()
        
        # Usuario no autenticado
        mock_streamlit_session.authenticated = False
        assert auth.get_user_permissions() == []
        
        # Usuario admin
        mock_streamlit_session.authenticated = True
        mock_streamlit_session.user_role = 'admin'
        permissions = auth.get_user_permissions()
        assert 'admin' in permissions
        assert 'ml_advanced' in permissions
        assert 'ml_basic' in permissions
        
        # Usuario invitado
        mock_streamlit_session.user_role = 'invitado'
        permissions = auth.get_user_permissions()
        assert 'invitado' in permissions
        assert 'ml_basic' in permissions
        assert 'admin' not in permissions
        assert 'ml_advanced' not in permissions
    
    def test_hmac_security(self):
        """Test que se usa HMAC para comparación segura"""
        auth = SimpleAuth()
        auth.users['admin'] = 'test_password'
        
        # Verificar que se usa hmac.compare_digest
        with patch('hmac.compare_digest') as mock_compare:
            mock_compare.return_value = True
            auth.check_password('admin', 'test_password')
            mock_compare.assert_called_once_with('test_password', 'test_password')
    
    def test_record_failed_attempt(self, mock_streamlit_session):
        """Test registro de intento fallido"""
        auth = SimpleAuth()
        
        # Simular estado inicial
        mock_streamlit_session.login_attempts = 0
        mock_streamlit_session.last_attempt = None
        
        auth._record_failed_attempt()
        
        assert mock_streamlit_session.login_attempts == 1
        assert mock_streamlit_session.last_attempt is not None
    
    def test_set_secure_cookie(self, mock_streamlit_session):
        """Test configuración de cookie segura"""
        auth = SimpleAuth()
        
        auth._set_secure_cookie('admin')
        
        assert 'secure_session' in mock_streamlit_session
        assert mock_streamlit_session['secure_session']['user'] == 'admin'
        assert mock_streamlit_session['secure_session']['authenticated'] is True
    
    def test_clear_cookie(self, mock_streamlit_session):
        """Test limpieza de cookie"""
        auth = SimpleAuth()
        
        # Simular cookie existente
        mock_streamlit_session['secure_session'] = {'user': 'admin'}
        
        auth._clear_cookie()
        
        assert 'secure_session' not in mock_streamlit_session


class TestAuthFunctions:
    """Tests para funciones auxiliares de autenticación"""
    
    @patch('auth.simple_auth.st')
    def test_show_login_form(self, mock_st):
        """Test función show_login_form"""
        # Mock de st.columns y st.form
        mock_st.columns.return_value = [MagicMock(), MagicMock()]
        mock_st.form.return_value.__enter__.return_value = MagicMock()
        mock_st.selectbox.return_value = "admin"
        mock_st.text_input.return_value = "password"
        mock_st.form_submit_button.return_value = True
        
        # Mock de show_svg_icon
        with patch('auth.simple_auth.show_svg_icon'):
            show_login_form()
        
        # Verificar que se llamaron las funciones de Streamlit
        mock_st.markdown.assert_called()
        mock_st.form.assert_called()
    
    @patch('auth.simple_auth.st')
    def test_show_logout_section(self, mock_st):
        """Test función show_logout_section"""
        # Mock de auth.get_current_user
        with patch('auth.simple_auth.SimpleAuth') as mock_auth_class:
            mock_auth = MagicMock()
            mock_auth.get_current_user.return_value = 'admin'
            mock_auth_class.return_value = mock_auth
            
            show_logout_section()
            
            # Verificar que se llamó get_current_user
            mock_auth.get_current_user.assert_called()
    
    def test_require_auth_decorator(self, mock_streamlit_session):
        """Test decorator require_auth"""
        # Función de prueba
        @require_auth
        def test_function():
            return "success"
        
        # Mock de auth.is_authenticated
        with patch('auth.simple_auth.SimpleAuth') as mock_auth_class:
            mock_auth = MagicMock()
            mock_auth.is_authenticated.return_value = False
            mock_auth_class.return_value = mock_auth
            
            # Mock de show_login_form y st.stop
            with patch('auth.simple_auth.show_login_form') as mock_show_form, \
                 patch('auth.simple_auth.st.stop') as mock_stop:
                
                result = test_function()
                
                # Verificar que se llamó show_login_form y st.stop
                mock_show_form.assert_called_once()
                mock_stop.assert_called_once()


@pytest.mark.auth
class TestAuthIntegration:
    """Tests de integración para el sistema de autenticación"""
    
    @patch('auth.simple_auth.st.session_state')
    def test_full_auth_flow(self, mock_session_state):
        """Test flujo completo de autenticación"""
        auth = SimpleAuth()
        auth.users['admin'] = 'test_password'
        
        # 1. Login exitoso
        result = auth.login('admin', 'test_password')
        assert result['success'] is True
        
        # 2. Verificar autenticación
        assert auth.is_authenticated() is True
        assert auth.get_current_user() == 'admin'
        
        # 3. Verificar permisos
        assert auth.has_permission('admin') is True
        assert auth.has_permission('ml_advanced') is True
        
        # 4. Logout
        auth.logout()
        assert auth.is_authenticated() is False
        assert auth.get_current_user() is None
    
    @patch('auth.simple_auth.st.session_state')
    def test_security_measures(self, mock_session_state):
        """Test medidas de seguridad implementadas"""
        auth = SimpleAuth()
        auth.users['admin'] = 'test_password'
        
        # Test timing attack protection con HMAC
        import time
        
        # Medir tiempo de respuesta para contraseñas válidas e inválidas
        start_time = time.time()
        auth.check_password('admin', 'test_password')
        valid_time = time.time() - start_time
        
        start_time = time.time()
        auth.check_password('admin', 'wrong_password')
        invalid_time = time.time() - start_time
        
        # Los tiempos deberían ser similares (protección contra timing attacks)
        time_diff = abs(valid_time - invalid_time)
        assert time_diff < 0.1  # Diferencia máxima de 100ms
