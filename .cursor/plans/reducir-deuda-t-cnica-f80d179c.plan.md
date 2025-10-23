<!-- f80d179c-1283-40b9-958e-ada0ede17c17 c497f050-f9ef-469d-8cce-ba3c48ef2f29 -->
# Plan: Reducir Deuda Técnica y Análisis de Calidad

## Contexto del Proyecto

**CorAlertMet Intelligence** - Sistema de alertas meteorológicas con ML para Córdoba, Argentina.

**Módulos críticos identificados:**

- `auth/simple_auth.py` - Sistema de autenticación con HMAC
- `cache/cache_manager.py` - Gestor de cache para modelos ML
- `pages_modules/ml_models/` - Modelos de ML (4 módulos)

**Configuración existente:**

- Pylint configurado en `pyproject.toml`
- Estructura de seguridad en `security_analysis/`

## Fase 1: Tests Unitarios para Módulos Críticos

### 1.1 Configurar Infraestructura de Testing

- Crear estructura `tests/` con subdirectorios: `unit/`, `fixtures/`, `conftest.py`
- Instalar dependencias de testing: `pytest>=8.0.0`, `pytest-cov>=4.1.0`, `pytest-mock>=3.12.0`
- Configurar `pytest.ini` con cobertura mínima del 80%

### 1.2 Tests para `auth/simple_auth.py`

**Archivo:** `tests/unit/test_simple_auth.py`

**Casos de prueba críticos:**

- `test_check_password_valid()` - Verificar autenticación exitosa con HMAC
- `test_check_password_invalid()` - Verificar rechazo de credenciales incorrectas
- `test_login_success()` - Flujo completo de login exitoso
- `test_login_failed_attempts()` - Protección anti-fuerza bruta (5 intentos)
- `test_account_lockout()` - Bloqueo temporal de cuenta (5 minutos)
- `test_logout()` - Limpieza correcta de sesión
- `test_is_authenticated()` - Verificación de estado de autenticación
- `test_has_permission_admin()` - Permisos de administrador
- `test_has_permission_guest()` - Permisos de invitado

### 1.3 Tests para `cache/cache_manager.py`

**Archivo:** `tests/unit/test_cache_manager.py`

**Casos de prueba críticos:**

- `test_save_model()` - Guardar modelo con joblib
- `test_load_model()` - Cargar modelo existente
- `test_model_expiration()` - Verificar expiración de modelos (7 días)
- `test_save_data()` - Guardar datos con pickle
- `test_load_data()` - Cargar datos existentes
- `test_data_expiration()` - Verificar expiración de datos (1 hora)
- `test_cleanup_expired()` - Limpieza de cache expirado
- `test_get_cache_stats()` - Estadísticas de cache
- `test_generate_key_consistency()` - Generación consistente de claves MD5

### 1.4 Tests para Módulos ML

**Archivos:**

- `tests/unit/test_advanced_predictions.py`
- `tests/unit/test_intelligent_alerts.py`
- `tests/unit/test_model_validation.py`
- `tests/unit/test_precision_metrics.py`

**Casos de prueba por módulo (mínimo 5 tests cada uno):**

- Validación de entradas
- Manejo de errores
- Cálculos matemáticos correctos
- Integración con cache
- Formato de salida esperado

## Fase 2: Análisis con Pylint

### 2.1 Ejecutar Pylint con Configuración Existente

**Comando:** `pylint app.py auth/ cache/ pages_modules/ components/ config/ --rcfile=pyproject.toml`

**Configuración actual en `pyproject.toml`:**

```toml
[tool.pylint.master]
disable = "C0114,C0116,R0903,W0613"
max-line-length = 100
```

### 2.2 Corregir Errores Encontrados

**Prioridad de corrección:**

1. **Errores (E)** - Código que no funcionará
2. **Warnings (W)** - Problemas potenciales
3. **Refactor (R)** - Mejoras de diseño (solo si son críticas)
4. **Convention (C)** - Ya deshabilitados en config

**Archivos a analizar:**

- `app.py` (1054 líneas)
- `auth/simple_auth.py` (343 líneas)
- `cache/cache_manager.py` (376 líneas)
- `pages_modules/ml_dashboard.py`
- `pages_modules/ml_models/*.py`

## Fase 3: Análisis SAST

### 3.1 Ejecutar Bandit (Análisis de Seguridad)

**Comando:** `bandit -r . -f json -o security_analysis/bandit_current.json --exclude venv,tests`

**Severidades a corregir:**

- **HIGH** - Vulnerabilidades críticas
- **MEDIUM** - Solo si son de seguridad real

**Problemas conocidos a verificar:**

- Uso de `pickle` en `cache_manager.py` (líneas 193, 238) - ALTO RIESGO
- Comparación con `hmac.compare_digest` en auth - CORRECTO
- Configuración de cookies seguras - VERIFICAR

### 3.2 Ejecutar pip-audit (Vulnerabilidades de Dependencias)

**Comando:** `pip-audit --format json --output security_analysis/pip_audit_current.json`

**Acción:** Actualizar dependencias con vulnerabilidades críticas en `requirements.txt`

### 3.3 Ejecutar Pylint como SAST Adicional

**Enfoque:** Detectar patrones inseguros (inyección SQL, eval, exec, etc.)

## Fase 4: Correcciones Críticas

### 4.1 Problema Crítico: Uso de Pickle

**Archivo:** `cache/cache_manager.py` líneas 193-194, 238

**Problema:** `pickle.load()` es inseguro - puede ejecutar código arbitrario

**Solución:**

```python
# ANTES (línea 193-194)
with open(data_file, 'wb') as f:
    pickle.dump(data, f)

# DESPUÉS - Usar joblib o JSON según tipo de dato
import joblib
with open(data_file, 'wb') as f:
    joblib.dump(data, f)
```

### 4.2 Otros Problemas de Severidad Alta

- Verificar uso de `eval()` o `exec()` - NO ENCONTRADO ✓
- Verificar hardcoded secrets - NO ENCONTRADO ✓
- Verificar SQL injection - NO APLICA (no usa SQL) ✓

## Fase 5: Reporte Final

### 5.1 Generar Reportes

**Archivos a crear:**

- `tests/coverage_report.txt` - Cobertura de tests
- `security_analysis/pylint_report.json` - Resultados de Pylint
- `security_analysis/FIXES_APPLIED.md` - Documentación de correcciones

### 5.2 Métricas de Calidad

**Objetivos:**

- Cobertura de tests: ≥80% en módulos críticos
- Pylint score: ≥9.0/10
- Vulnerabilidades críticas: 0
- Type hints: 100% en funciones públicas

## Entregables

1. **Tests Unitarios Completos**

   - 25+ tests para módulos críticos
   - Cobertura ≥80%
   - Fixtures reutilizables

2. **Código Limpio**

   - Sin errores de Pylint
   - Type hints completos
   - Documentación mejorada

3. **Seguridad Mejorada**

   - Reemplazo de pickle por joblib
   - Vulnerabilidades críticas corregidas
   - Reporte de seguridad actualizado

4. **Documentación**

   - README de tests
   - Guía de contribución
   - Reporte de cambios aplicados

### To-dos

- [x] Configurar infraestructura de testing (pytest, estructura de directorios, conftest.py)
- [x] Crear tests unitarios para auth/simple_auth.py (9+ casos de prueba)
- [x] Crear tests unitarios para cache/cache_manager.py (9+ casos de prueba)
- [x] Crear tests unitarios para módulos ML (4 archivos, 5+ tests cada uno)
- [x] Ejecutar Pylint con configuración existente y generar reporte
- [x] Corregir errores y warnings críticos encontrados por Pylint
- [x] Ejecutar Bandit para análisis de seguridad y generar reporte
- [x] Ejecutar pip-audit para detectar vulnerabilidades en dependencias
- [x] Reemplazar pickle por joblib en cache_manager.py (CRÍTICO)
- [x] Corregir problemas de severidad alta/crítica encontrados por SAST
- [x] Ejecutar suite completa de tests y generar reporte de cobertura
- [x] Generar reportes finales de calidad, seguridad y documentación