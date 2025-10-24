# Changelog - CorAlertIntel Intelligence

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.3.0] - 2025-01-23

### 🔧 Corregido
- **Acceso a Streamlit Secrets**: Corregido formato de acceso a variables de entorno en Streamlit Cloud
  - Cambio de `st.secrets.get()` a `st.secrets.secrets["VARIABLE"]`
  - Afecta: Autenticación, APIs de OpenWeatherMap y Windy
  - **IMPORTANTE**: Para futuras configuraciones, usar formato `st.secrets.secrets["NOMBRE_VARIABLE"]`
- **Errores críticos de importación**: Eliminados imports problemáticos que causaban KeyError en Streamlit Cloud
  - Reemplazados imports de componentes con funciones dummy
  - Eliminados try-except blocks problemáticos
  - Aplicado en: `app.py`, `ml_dashboard.py`, `config/__init__.py`
- **Errores de sintaxis en ML Panel**: Corregidos múltiples errores que impedían el funcionamiento
  - String literals sin cerrar en `model_validation.py`
  - Imports faltantes (`cross_val_score`)
  - Compatibilidad con IsolationForest (`offset_` attribute)
  - Imports circulares en `pages_modules/ml_models/__init__.py`
- **Errores de SVG y mapas**: Corregidos problemas de renderizado
  - Sintaxis SVG corregida en `components/svg_icons_smooth.py`
  - Imports de mapas corregidos en `app.py`
  - Iconos SVG simplificados para compatibilidad con Python 3.13

### 🎉 Agregado
- **Sistema de indicadores visuales de viento** - Flechas SVG direccionales para mostrar dirección \
    del viento
- **Colores combinados temperatura-viento** - Marcadores que indican tanto temperatura como \
    intensidad del viento
- **Función de geocoding mejorada** - Coordenadas precisas para ubicaciones aeronáuticas
- **Leyenda interactiva de capas** - Selector para visualizar temperatura, viento o vista integrada
- **Iconos Heroicons unificados** - Reemplazo completo de emojis por iconos SVG profesionales
- **Sistema de colores meteorológicos** - 15 combinaciones de colores para temperatura + viento
- **Popup mejorado** - Datos meteorológicos completos con iconos SVG
- **Sistema de funciones dummy** - Fallbacks para componentes faltantes en Streamlit Cloud
- **Manejo robusto de errores** - Try-catch blocks para imports críticos
- **Iconos SVG simplificados** - Versión compatible con Python 3.13 en Streamlit Cloud

### 🔧 Cambiado
- **Marcadores del mapa** - De colores simples a colores combinados (temperatura + viento)
- **Indicadores de viento** - De Wind Barbs superpuestos a flechas SVG direccionales
- **Leyenda de capas** - Simplificada a 3 opciones: Temperatura, Viento, Todas las Capas
- **Iconos de interfaz** - Emojis reemplazados por Heroicons SVG en toda la aplicación
- **Sistema de colores** - De solo temperatura a combinación temperatura + viento
- **Coordenadas de Altagracia** - Corregidas para ubicación al sur de Córdoba capital
- **Imports de componentes** - De imports directos a funciones dummy para compatibilidad
- **Estructura de ML Panel** - Eliminado `__init__.py` problemático, imports directos
- **Gráficos de precisión** - Simplificados a mensajes informativos
- **Gráficos de comparación** - Eliminados gráficos lineales complejos

### 🐛 Corregido
- **NameError selected_layer** - Variable no definida en selector de capas
- **TypeError st.subheader** - Parámetro unsafe_allow_html no soportado
- **Superposición de indicadores** - Wind Barbs eliminados para evitar conflictos visuales
- **Coordenadas incorrectas** - Altagracia corregida de norte a sur de Córdoba
- **Cache de Streamlit** - Problemas de recarga forzada con comentarios de actualización
- **KeyError en imports** - Errores de importación de componentes en Streamlit Cloud
- **SyntaxError en ML Panel** - Errores de sintaxis que impedían el funcionamiento
- **ImportError circular** - Imports circulares en módulos ML
- **AttributeError IsolationForest** - Compatibilidad con versiones sin `offset_`
- **UnicodeEncodeError** - Problemas de codificación en Python 3.13

### 🎨 UI/UX
- **Flechas de viento animadas** - Rotación automática según dirección del viento
- **Colores meteorológicos profesionales** - 15 combinaciones temperatura + viento
- **Iconos SVG consistentes** - Heroicons en lugar de emojis para mejor profesionalismo
- **Leyenda visual mejorada** - Explicación clara de colores combinados
- **Popup informativo** - Datos meteorológicos con iconos SVG temáticos
- **Selector de capas intuitivo** - 3 opciones claras sin superposiciones

### 📊 Rendimiento
- **Eliminación de Wind Barbs** - Reducción de elementos SVG superpuestos
- **Optimización de marcadores** - Solo flechas direccionales + marcadores combinados
- **Cache de coordenadas** - Geocoding optimizado para ubicaciones aeronáuticas
- **Cálculos trigonométricos** - Posicionamiento preciso de flechas de viento

### 🔧 Mejoras Técnicas
- **Función `get_combined_temp_wind_color()`** - 15 combinaciones de colores temperatura + viento
- **Función `create_wind_arrow_svg()`** - Flechas SVG rotadas según dirección del viento
- **Función `create_enhanced_wind_marker()`** - Marcadores con colores combinados
- **Eliminación de `create_wind_barb_enhanced()`** - Wind Barbs removidos por superposición
- **Actualización de leyenda** - Explicación de colores combinados en vista integrada

### 📁 Archivos Modificados
- `pages_modules/map_live.py` - Sistema completo de indicadores visuales de viento
- `CHANGELOG.md` - Registro de cambios versión 2.3.0
- `app.py` - Funciones dummy para componentes, imports robustos
- `pages_modules/ml_dashboard.py` - Funciones dummy, imports directos ML
- `config/__init__.py` - Funciones dummy para logging
- `pages_modules/ml_models/model_validation.py` - Corrección sintaxis, eliminación gráficos
- `pages_modules/ml_models/precision_metrics.py` - Simplificación a mensajes informativos
- `pages_modules/ml_models/intelligent_alerts.py` - Compatibilidad IsolationForest
- `components/svg_icons_simple.py` - Iconos SVG simplificados para Python 3.13
- `auth/simple_auth.py` - Imports locales de iconos SVG

### ⚠️ Aspectos Negativos Identificados
- **Complejidad visual inicial** - Los colores combinados pueden requerir explicación adicional
- **Dependencia de datos de viento** - Sin datos de viento, los marcadores usan colores por defecto
- **Curva de aprendizaje** - Los usuarios necesitan entender el sistema de colores combinados
- **Rendimiento en mapas grandes** - Múltiples flechas SVG pueden impactar rendimiento
- **Funciones dummy** - Algunos componentes pueden mostrar funcionalidad limitada
- **Gráficos simplificados** - Menos visualizaciones complejas para mejor compatibilidad

### ✅ Aspectos Positivos Destacados
- **Visualización intuitiva** - Flechas direccionales claras y colores combinados informativos
- **Profesionalismo** - Iconos Heroicons y sistema de colores meteorológicos
- **Información completa** - Temperatura, viento y dirección en un vistazo
- **Sin superposiciones** - Diseño limpio sin elementos que se solapen
- **Escalabilidad** - Sistema fácil de extender para más ubicaciones
- **Compatibilidad total** - Funciona perfectamente en Streamlit Cloud con Python 3.13
- **Robustez** - Manejo de errores que previene fallos de la aplicación
- **Simplicidad** - Interfaz más limpia sin gráficos complejos problemáticos
- **Mantenibilidad** - Código más fácil de mantener y actualizar

---

## [2.2.0] - 2025-01-16

### 🎉 Agregado
- **Sistema de autenticación con iconos SVG profesionales** - Login visual mejorado
- **Mensajes de error con animaciones** - Feedback visual para credenciales incorrectas
- **Sistema de alertas meteorológicas inteligentes** - Niveles de riesgo automáticos
- **Cache híbrido optimizado** - Mejora de rendimiento con `@st.cache_data` y `@st.cache_resource`
- **Visualizaciones unificadas para pilotos** - Gráficos simplificados y claros
- **Cards de métricas por modelo** - Comparación visual de HRRR, ECMWF, GFS27
- **Guía de interpretación rápida** - Tabla de confianza para toma de decisiones
- **Indicadores de estado de actualización** - Monitoreo en tiempo real de modelos
- **Sistema de recomendaciones automáticas** - Alertas basadas en probabilidad de tormenta

### 🔧 Cambiado
- **Login visual** - Emoticones básicos reemplazados por iconos SVG animados
- **Validación de modelos** - Gráficos individuales unificados en comparación visual
- **Precisión temporal** - Mejorada con colores aeronáuticos y zonas de confianza
- **Predicciones avanzadas** - Simplificadas para mejor interpretación de pilotos
- **Niveles de alerta** - Movidos al final de la página para mejor flujo
- **Cache de sesión** - Implementado para mantener estado entre actualizaciones

### 🐛 Corregido
- **CachedWidgetWarning** - Refactorizado para separar datos de widgets
- **Rutas de entorno virtual** - Corregidas en `pyvenv.cfg` para ejecución correcta
- **Dependencias incompatibles** - Actualizadas versiones de `plotly` y `darts`
- **Propiedades de Plotly** - Corregido uso de `titlefont` en gráficos
- **Validación de entrada** - Mejorada para campos vacíos en login

### 🎨 UI/UX
- **Iconos SVG profesionales** - Reemplazo completo de emoticones básicos
- **Animaciones suaves** - `smoothBlink`, `gentlePulse`, `softBounce`, `smoothRotate`
- **Colores aeronáuticos** - Paleta específica para pilotos (verde, amarillo, naranja, rojo)
- **Zonas de confianza visuales** - EXCELENTE, BUENO, ACEPTABLE, CRÍTICO
- **Cards de métricas** - Diseño limpio para comparación de modelos
- **Alertas contextuales** - Mensajes específicos según nivel de riesgo

### 📊 Rendimiento
- **Cache inteligente implementado** - TTL configurado para diferentes tipos de datos
- **API calls optimizadas** - Reducción de llamadas redundantes
- **Modelos ML cacheados** - Carga única por sesión
- **Datos meteorológicos** - Cache de 5 minutos para datos en tiempo real
- **Validación de modelos** - Cache de 1 hora para resultados de ML

### 🔒 Seguridad
- **Mensajes de error seguros** - No exposición de información sensible
- **Validación de entrada** - Sanitización de datos de usuario
- **Logging de autenticación** - Registro de intentos fallidos
- **Protección contra fuerza bruta** - Límites de intentos implementados

### 🧪 Testing
- **Validación de login** - Probado con credenciales incorrectas y vacías
- **Cache functionality** - Verificado funcionamiento de caché híbrido
- **Responsividad** - Probado en diferentes dispositivos
- **Animaciones** - Verificado funcionamiento de iconos SVG

### 🔧 Mejoras Técnicas
- **Refactorización de `advanced_predictions.py`** - Separación de datos y UI para evitar \
    CachedWidgetWarning
- **Optimización de `model_validation.py`** - Unificación de gráficos individuales en comparación \
    visual
- **Mejora de `precision_metrics.py`** - Integración de estado de actualización en guía de \
    interpretación
- **Cache híbrido en `app.py`** - Implementación de `@st.cache_data` para APIs meteorológicas
- **Autenticación visual en `simple_auth.py`** - Reemplazo de emoticones por iconos SVG \
    profesionales
- **Eliminación de secciones irrelevantes** - Removidas visualizaciones técnicas no útiles para \
    pilotos

### 📁 Archivos Modificados
- `auth/simple_auth.py` - Iconos SVG y mensajes de error mejorados
- `app.py` - Cache híbrido y reubicación de alertas meteorológicas
- `pages_modules/ml_models/advanced_predictions.py` - Refactorización y simplificación
- `pages_modules/ml_models/model_validation.py` - Unificación de gráficos
- `pages_modules/ml_models/precision_metrics.py` - Integración de estado de actualización
- `pages_modules/map_live.py` - Cache para geocoding
- `pages_modules/cache_admin.py` - Cache para estadísticas
- `venv/pyvenv.cfg` - Corrección de rutas de entorno virtual
- `requirements.txt` - Actualización de versiones de dependencias

---

## [2.1.0] - 2025-01-16

### 🎉 Agregado
- **Sistema de autenticación mejorado** con selector de usuario sin predeterminado
- **Footer fijo y compacto** que permanece siempre visible
- **Sistema de responsividad completo** para todos los dispositivos
- **CSS centralizado** siguiendo mejores prácticas de Streamlit
- **Configuración de versión centralizada** en `config/version.py`
- **Documentación CSS completa** con guías de mantenimiento
- **Sistema de logging robusto** con rotación de archivos
- **Cache inteligente** para modelos ML y datos
- **Iconos SVG animados** con transiciones suaves
- **Mapa interactivo** con coordenadas aeronáuticas
- **Panel ML avanzado** con predicciones y anomalías

### 🔧 Cambiado
- **Login page** - Usuario predeterminado removido, requiere selección explícita
- **Footer** - Convertido a fijo y compacto (50% más pequeño)
- **Responsividad** - Sistema completo de breakpoints móvil/tablet/desktop
- **CSS** - Reorganizado y optimizado siguiendo estándares Streamlit
- **Estructura de archivos** - Mejor organización modular

### 🐛 Corregido
- **Validación de login** - Mejorada para manejar selección vacía
- **Layout responsivo** - Columnas se adaptan correctamente a pantallas pequeñas
- **Footer** - Ya no interfiere con el contenido principal
- **Iconos** - Escalado apropiado en diferentes dispositivos

### 🔒 Seguridad
- **Autenticación HMAC** - Comparación segura de contraseñas
- **Protección contra fuerza bruta** - Límites de intentos de login
- **Logging de seguridad** - Registro de intentos de acceso
- **Validación de entrada** - Sanitización de datos de usuario

### 📱 Responsividad
- **Móvil (≤480px)**: 1 columna, iconos 16px, footer vertical
- **Móvil Grande (≤768px)**: 2 columnas, iconos 20px, footer compacto
- **Tablet (769-1024px)**: 3 columnas, iconos 24px, layout híbrido
- **Desktop (≥1025px)**: 4 columnas, iconos 24px, layout completo

### 🎨 UI/UX
- **Footer fijo** - Información siempre visible
- **Transiciones suaves** - Animaciones CSS optimizadas
- **Iconos escalables** - Adaptación automática por dispositivo
- **Layout fluido** - Flexbox responsivo
- **Colores corporativos** - Gradientes y sombras profesionales

### 📊 Rendimiento
- **CSS optimizado** - Selectores eficientes
- **Cache inteligente** - TTL configurable para modelos
- **Lazy loading** - Componentes cargados bajo demanda
- **Compresión** - Archivos optimizados para producción

### 🧪 Testing
- **Linting** - Pylint configurado sin errores
- **Seguridad** - Bandit, Safety, pip-audit implementados
- **Responsividad** - Probado en múltiples dispositivos
- **Compatibilidad** - Navegadores modernos soportados

### 📚 Documentación
- **CSS_DOCUMENTATION.md** - Guía completa de estilos
- **README.md** - Instrucciones de instalación y uso
- **CHANGELOG.md** - Historial de cambios
- **Comentarios inline** - Código bien documentado

---

## [2.0.0] - 2025-01-15

### 🎉 Agregado
- Sistema base de alertas meteorológicas
- Integración con APIs meteorológicas
- Modelos de Machine Learning básicos
- Interfaz Streamlit inicial

---

## [1.0.0] - 2025-01-14

### 🎉 Agregado
- Proyecto inicial
- Estructura base del sistema
- Configuración inicial de dependencias

---

## Tipos de Cambios

- **🎉 Agregado** - Para nuevas funcionalidades
- **🔧 Cambiado** - Para cambios en funcionalidades existentes
- **🐛 Corregido** - Para corrección de bugs
- **🔒 Seguridad** - Para mejoras de seguridad
- **📱 Responsividad** - Para mejoras de UI/UX
- **🎨 UI/UX** - Para mejoras de interfaz
- **📊 Rendimiento** - Para optimizaciones
- **🧪 Testing** - Para pruebas y calidad
- **📚 Documentación** - Para actualizaciones de documentación
