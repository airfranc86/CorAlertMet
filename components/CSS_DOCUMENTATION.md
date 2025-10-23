# 📋 Documentación CSS - CorAlertIntel Intelligence

## 🎯 **Cumplimiento con Streamlit**

### ✅ **Clases CSS Oficiales Utilizadas**
- `.stButton` - Botones de Streamlit
- `.stSelectbox` - Selectores desplegables
- `.stRadio` - Botones de radio
- `.stMarkdown` - Contenido markdown
- `.stDataFrame` - Tablas de datos
- `.stColumn` - Columnas de Streamlit
- `.element-container` - Contenedores de elementos
- `.main .block-container` - Contenedor principal

### ✅ **Data Attributes Oficiales**
- `[data-testid="stToolbar"]` - Toolbar de Streamlit
- `[data-testid="stDecoration"]` - Decoración de Streamlit

### ✅ **IDs Oficiales**
- `#MainMenu` - Menú hamburguesa
- `footer` - Footer nativo

---

## 📱 **Sistema de Responsividad**

### **Breakpoints Implementados**
```css
/* Móvil pequeño */
@media (max-width: 480px) { ... }

/* Móvil */
@media (max-width: 768px) { ... }

/* Tablet */
@media (min-width: 769px) and (max-width: 1024px) { ... }

/* Desktop */
/* Sin media query - estilos base */
```

### **Estrategia de Columnas**
- **Desktop**: 4 columnas completas
- **Tablet**: 3 columnas (33.333%)
- **Móvil**: 2 columnas (50%)
- **Móvil pequeño**: 1 columna (100%)

---

## 🎨 **Mejoras Visuales**

### **1. Ocultación de Elementos Nativos**
```css
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display: none;}
```

### **2. Sidebar Personalizado**
```css
.css-1d391kg {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
}
```

### **3. Botones Mejorados**
```css
.stButton > button {
    border-radius: 0.5rem;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
```

### **4. Métricas Estilizadas**
```css
.metric-container {
    padding: 1rem;
    border-radius: 0.5rem;
    background-color: rgba(255, 255, 255, 0.05);
}
```

---

## 🔧 **Mejores Prácticas Implementadas**

### **1. Uso de `!important`**
- ✅ Solo cuando es necesario para sobrescribir estilos de Streamlit
- ✅ Documentado y justificado
- ✅ Agrupado por funcionalidad

### **2. Selectores Específicos**
- ✅ Uso de clases específicas de Streamlit
- ✅ Evitar selectores genéricos
- ✅ Jerarquía clara de especificidad

### **3. Transiciones Suaves**
```css
.stButton > button,
.stSelectbox > div,
.stRadio > div > label {
    transition: all 0.3s ease;
}
```

### **4. Animaciones CSS**
```css
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
```

---

## 📊 **Compatibilidad**

### **Navegadores Soportados**
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

### **Dispositivos Soportados**
- ✅ Desktop (1920x1080+)
- ✅ Laptop (1366x768+)
- ✅ Tablet (768x1024)
- ✅ Móvil (375x667+)
- ✅ Móvil pequeño (320x568+)

---

## 🚀 **Optimizaciones de Rendimiento**

### **1. CSS Eficiente**
- ✅ Media queries agrupadas
- ✅ Selectores optimizados
- ✅ Propiedades agrupadas lógicamente

### **2. Transiciones Optimizadas**
- ✅ Solo en elementos interactivos
- ✅ Duración consistente (0.3s)
- ✅ Easing suave (ease)

### **3. Responsividad Ligera**
- ✅ Flexbox para layouts
- ✅ Porcentajes para dimensiones
- ✅ Min/max-width para límites

---

## 📝 **Mantenimiento**

### **Estructura del Archivo**
1. **Ocultación de elementos nativos**
2. **Responsividad móvil**
3. **Responsividad tablet**
4. **Mejoras generales**
5. **Mejoras específicas de Streamlit**
6. **Animaciones**

### **Convenciones de Naming**
- `.smooth-icon` - Iconos SVG personalizados
- `.footer-container` - Contenedor del footer
- `.metric-container` - Contenedor de métricas

### **Comentarios**
- ✅ Secciones claramente marcadas
- ✅ Explicación de cada media query
- ✅ Justificación de `!important`

---

## 🔍 **Testing**

### **Dispositivos de Prueba**
- iPhone SE (375x667)
- iPhone 12 (390x844)
- iPad (768x1024)
- MacBook Air (1440x900)
- Desktop (1920x1080)

### **Funcionalidades Verificadas**
- ✅ Navegación responsiva
- ✅ Formularios adaptativos
- ✅ Gráficos escalables
- ✅ Tablas con scroll
- ✅ Botones táctiles

---

## 📚 **Referencias**

- [Streamlit CSS Documentation](https://docs.streamlit.io/library/advanced-features/theming)
- [CSS Media Queries](https://developer.mozilla.org/en-US/docs/Web/CSS/Media_Queries)
- [Flexbox Guide](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)
- [CSS Best Practices](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Best_Practices)

---

**Última actualización**: 16 de Octubre de 2025  
**Versión**: 2.1.0  
**Mantenido por**: Francisco Aucar
