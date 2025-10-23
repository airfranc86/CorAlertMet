# 🐍 Ecosistema Completo de Librerías Python para Data Science & ML

Una guía integral y estructurada de módulos y librerías esenciales, desde la base del lenguaje hasta IA, forecasting y automatización.

---

## 📘 Índice
1. [Biblioteca Estándar de Python](#%EF%B8%8F-1-biblioteca-estándar-de-python)
2. [Manipulación de Datos](#%EF%B8%8F-2-manipulación-de-datos)
3. [Ciencia de Datos y Análisis Numérico](#-3-ciencia-de-datos-y-análisis-numérico)
4. [Visualización de Datos](#-4-visualización-de-datos)
5. [Aprendizaje Automático y Deep Learning](#-5-aprendizaje-automático-y-deep-learning)
6. [Procesamiento del Lenguaje Natural (NLP)](#-6-procesamiento-del-lenguaje-natural-nlp)
7. [Series Temporales y Forecasting](#%EF%B8%8F-7-series-temporales-y-forecasting)
8. [Bases de Datos y Big Data](#%EF%B8%8F-8-bases-de-datos-y-big-data)
9. [Desarrollo Web y APIs](#-9-desarrollo-web-y-apis)
10. [Automatización y Web Scraping](#-10-automatización-y-web-scraping)
11. [Interfaces Gráficas y Procesamiento Multimedia](#%EF%B8%8F-11-interfaces-gráficas-y-procesamiento-multimedia)
12. [Testing y Calidad de Código](#-12-testing-y-calidad-de-código)
13. [Resumen Ejecutivo](#-13-resumen-ejecutivo)

---

## ⚙️ 1. Biblioteca Estándar de Python

El corazón del lenguaje: herramientas integradas sin necesidad de instalar nada extra.

| Módulo | Descripción |
|:-------|:-------------|
| **os** | Interacción con el sistema operativo (rutas, procesos, variables de entorno). |
| **sys** | Control del intérprete, argumentos y configuración del entorno de ejecución. |
| **collections** | Estructuras de datos avanzadas (`Counter`, `deque`, `defaultdict`). |
| **datetime** | Manejo de fechas, horas y zonas horarias. |
| **json** | Lectura y escritura de datos en formato JSON. |
| **pathlib** | Manejo moderno y orientado a objetos de rutas de archivos. |
| **subprocess** | Ejecución y control de comandos del sistema. |

---

## 🗂️ 2. Manipulación de Datos

Cuando necesites limpiar, transformar o manejar grandes volúmenes de datos:

| Librería | Propósito Principal |
|:----------|:--------------------|
| **Pandas** | Estándar para análisis tabular tipo DataFrame. |
| **Polars** | Versión ultrarrápida basada en Rust. |
| **CuPy** | Operaciones tipo NumPy aceleradas por GPU. |
| **Vaex** | Ideal para datasets enormes (sin cargar todo en memoria). |
| **Datatable** | Para datos tipo R, muy eficiente. |
| **Modin** | Acelera Pandas usando múltiples núcleos. |

---

## 📊 3. Ciencia de Datos y Análisis Numérico

| Librería | Propósito Principal |
|:----------|:--------------------|
| **NumPy** | Cálculo numérico, vectores, matrices y álgebra lineal de alto rendimiento. |
| **SciPy** | Funciones científicas y matemáticas avanzadas. |
| **StatsModels** | Modelado estadístico, regresión y análisis econométrico. |
| **Pingouin** | Estadística descriptiva avanzada con sintaxis sencilla. |
| **Lifelines** | Análisis de supervivencia (útil en salud y biomedicina). |
| **PyMC3** | Inferencia bayesiana. |
| **PyStan** | Modelado estadístico jerárquico. |

---

## 📈 4. Visualización de Datos

Para gráficos y dashboards interactivos:

| Librería | Propósito Principal |
|:----------|:--------------------|
| **Matplotlib** | Base para gráficos 2D tradicionales. |
| **Seaborn** | Visualizaciones estadísticas elegantes y simples. |
| **Plotly** | Gráficos interactivos (ideal para dashboards Streamlit). |
| **Altair** | Visualizaciones limpias con enfoque declarativo y rápido para prototipos. |
| **Bokeh** | Dashboards web interactivos. |
| **Folium** | Mapas interactivos basados en Leaflet. |
| **Geoplotlib** | Mapas y análisis geoespacial técnico y preciso. |
| **Pygal** | Gráficos SVG escalables para reportes. |

---

## 🧮 5. Aprendizaje Automático y Deep Learning

Para modelos predictivos y entrenamiento supervisado/no supervisado:

| Librería | Propósito Principal |
|:----------|:--------------------|
| **Scikit-learn** | Machine Learning clásico generalista (clasificación, regresión, clustering). |
| **TensorFlow** | Framework completo de deep learning (Google). |
| **Keras** | API de alto nivel para TensorFlow. |
| **PyTorch** | Framework flexible y moderno de IA (Meta). |
| **JAX** | Computación automática acelerada y modelos modernos (Google). |
| **XGBoost** | Modelos basados en árboles de alto rendimiento, rendimiento top en tabulares. |
| **Theano** | Base histórica y teórica del deep learning clásico. |

---

## 🧠 6. Procesamiento del Lenguaje Natural (NLP)

Si necesitas analizar texto, sentimientos o generar lenguaje:

| Librería | Propósito Principal |
|:----------|:--------------------|
| **NLTK** | Procesamiento clásico de texto y análisis lingüístico académico. |
| **spaCy** | Tokenización y análisis gramatical de alto rendimiento, rápido y moderno. |
| **TextBlob** | Análisis de sentimiento simple y directo. |
| **BERT** | Representaciones semánticas profundas del lenguaje (embeddings). |
| **Polyglot** | Soporte multilingüe para NLP. |

---

## ⏱️ 7. Series Temporales y Forecasting

Si trabajas con indicadores, métricas o señales temporales (KPI, sensores, etc.):

### 📊 Comparativa de Librerías de Forecasting

| Librería | Enfoque Principal | Backend / Core | Ventajas Clave | Limitaciones | Ideal Para |
|-----------|------------------|----------------|----------------|---------------|-------------|
| **Prophet** | Modelos aditivos interpretables (tendencia + estacionalidad + feriados) | Core en `Stan` (Bayesiano) | - Interpretabilidad muy alta<br>- Ajuste automático de estacionalidad<br>- Fácil manejo de feriados<br>- Ideal para datos diarios o con patrones estacionales claros | - No maneja bien series con gran ruido o sin estacionalidad<br>- Escasa flexibilidad con *features* externas | Analistas que necesitan modelos interpretables y rápidos sin tuning complejo. Previsiones rápidas y automáticas (Facebook). |
| **NeuralProphet** | Extiende Prophet con redes neuronales (basado en PyTorch) | `PyTorch` | - Combina interpretabilidad de Prophet con potencia de *deep learning*<br>- Soporta *lagged regressors* y *autoregresión*<br>- Mejor desempeño con contexto local o señales exógenas | - Mayor complejidad en ajuste<br>- Entrenamiento más lento<br>- Dependencia fuerte de PyTorch | Casos con datos complejos y necesidad de combinar *features locales* o señales externas |
| **Darts** | Framework general de *time series forecasting* | `PyTorch`, `LightGBM`, `XGBoost`, `ARIMA`, etc. | - Soporta múltiples modelos (ARIMA, Prophet, RNNs, TFT, N-BEATS, etc.)<br>- Pipelines robustos y fáciles de comparar<br>- Incluye backtesting y métricas integradas | - Mayor curva de aprendizaje<br>- Dependencia de varias librerías<br>- Puede ser más pesado para proyectos simples | Data Scientists que desean experimentar con varios enfoques y comparar resultados. Modelos clásicos y de deep learning para forecasting. |
| **Sktime** | Machine Learning clásico y pipelines para series temporales | `Scikit-learn` | - Integración nativa con Scikit-learn<br>- Soporta clasificación, regresión y clustering temporal<br>- Herramientas de validación cruzada y métricas específicas | - Menor soporte para deep learning<br>- Visualización más limitada<br>- Menos intuitiva que Prophet/Darts | Casos de uso ML con estructura temporal: *forecasting, classification, anomaly detection*. ML especializado en series de tiempo. |
| **Kats** | Análisis temporal completo | Meta | Librería completa de Meta para análisis temporal y forecasting | - | Análisis temporal profesional |
| **AutoTS** | Auto-ML para predicciones temporales | Múltiple | Búsqueda automática del mejor modelo | - | Automatización de selección de modelos |
| **tsfresh** | Extracción de características | - | Extracción de características de series temporales para ML | - | Feature engineering temporal |

### 🔍 Recomendaciones según caso de uso

| Escenario | Recomendación |
|------------|----------------|
| Forecast interpretable, datos diarios o estacionales | **Prophet** |
| Forecast con *contexto local* o señales externas, mejor precisión | **NeuralProphet** |
| Pruebas comparativas entre múltiples modelos, pipelines productivos | **Darts** |
| Modelos ML tradicionales, validaciones cruzadas complejas | **Sktime** |

### 🧠 Integración y uso en stack Python

| Librería | Integración con | Output estándar |
|-----------|----------------|-----------------|
| Prophet / NeuralProphet | `Pandas`, `Plotly`, `Streamlit`, `Dash` | DataFrames |
| Darts | `NumPy`, `Torch`, `Pandas`, `Plotly` | `TimeSeries` objects |
| Sktime | `Scikit-learn`, `NumPy`, `Pandas` | `Estimator` compatible |

---

## 🗄️ 8. Bases de Datos y Big Data

Para procesar datos distribuidos o conectar con bases masivas:

| Librería | Propósito Principal |
|:----------|:--------------------|
| **SQLAlchemy** | ORM para bases SQL. |
| **Psycopg2 / AsyncPG** | Conexión con PostgreSQL. |
| **Dask** | Procesamiento paralelo en memoria local, paralelización de tareas. |
| **PySpark** | Procesamiento distribuido tipo Spark. |
| **Kafka** | Ingesta y transmisión de datos en tiempo real (streaming), flujos de datos. |
| **RAY** | Escalabilidad de ML/AI distribuida. |
| **Koalas** | Combina Pandas con Spark fácilmente. |
| **Hadoop** | Ecosistema de almacenamiento y procesamiento masivo, big data. |

---

## 🌐 9. Desarrollo Web y APIs

| Framework | Propósito Principal |
|:-----------|:--------------------|
| **Django** | Framework completo para aplicaciones web robustas. |
| **Flask** | Microframework minimalista y flexible. |
| **FastAPI** | API moderna y asíncrona, de alto rendimiento. |

---

## 🧰 10. Automatización y Web Scraping

Cuando necesites extraer datos desde la web:

| Librería | Propósito Principal |
|:----------|:--------------------|
| **BeautifulSoup** | Parsing de HTML y XML, parsear HTML fácilmente. |
| **Scrapy** | Framework completo y escalable de scraping, potente para crawling. |
| **Selenium** | Automatización de navegadores web (ideal para páginas dinámicas). |
| **Octoparse** | Herramienta visual de scraping (sin tanto código). |

---

## 🖼️ 11. Interfaces Gráficas y Procesamiento Multimedia

| Librería | Propósito Principal |
|:----------|:--------------------|
| **Tkinter** | GUI nativa de Python. |
| **PyQt / PySide** | Interfaz moderna con Qt. |
| **Kivy** | Interfaces táctiles y multiplataforma. |
| **Pillow** | Procesamiento básico de imágenes. |
| **OpenCV** | Visión por computadora avanzada. |

---

## 🧪 12. Testing y Calidad de Código

| Librería | Propósito Principal |
|:----------|:--------------------|
| **unittest** | Testing integrado en la biblioteca estándar. |
| **pytest** | Testing potente y legible. |
| **mock** | Simulación de objetos para tests. |

---

## 💬 13. Resumen Ejecutivo

> **Python es un ecosistema que crece por capas:**
> 
> - La **biblioteca estándar** cubre lo esencial.  
> - Las **librerías de manipulación de datos** optimizan el procesamiento masivo.
> - Las **librerías científicas** amplían el análisis y la modelización.  
> - Los **frameworks de ML/DL** permiten construir modelos predictivos avanzados.
> - Las **librerías de forecasting** especializan el análisis temporal con múltiples enfoques.
> - Los **frameworks web y de IA** lo convierten en una herramienta completa.  
> - Y su **ecosistema de automatización, visualización y testing** garantiza eficiencia y escalabilidad.

### 🚀 Conclusión sobre Forecasting

- **Prophet** → Simplicidad y claridad: ideal para dashboards y analistas.  
- **NeuralProphet** → Un paso adelante con redes neuronales interpretables.  
- **Darts** → Ecosistema completo de *forecasting experimental*.  
- **Sktime** → Orientado al *ML clásico temporal*, más académico o para pipelines integrados.

---

**Stack Base Recomendado:** Python + Pandas + Plotly + Streamlit + Supabase + GitHub  
**Versión:** Octubre 2025