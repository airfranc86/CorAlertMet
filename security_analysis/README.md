# 🔒 Análisis de Seguridad - CorAlertIntel

Esta carpeta contiene todos los archivos relacionados con el análisis de seguridad del proyecto \
    CorAlertIntel.

## 📁 Contenido de la Carpeta

### **📊 Reportes de Análisis**
- `bandit_report.json` - Análisis inicial de seguridad (Bandit)
- `bandit_report_fixed.json` - Análisis después de correcciones
- `safety_report.json` - Análisis de dependencias vulnerables (Safety)
- `pip_audit_report.json` - Auditoría de paquetes (pip-audit)

### **📋 Documentación**
- `SECURITY_ANALYSIS_REPORT.md` - Reporte completo inicial
- `SECURITY_FIXES_COMPLETED.md` - Reporte de correcciones aplicadas
- `README.md` - Este archivo

### **🛠️ Scripts de Análisis**
- `security_analysis.sh` - Script para Linux/Mac
- `security_analysis.bat` - Script para Windows

## 🚀 Cómo Usar

### **Ejecutar Análisis Completo:**
```bash
# Windows
security_analysis.bat

# Linux/Mac
./security_analysis.sh
```

### **Análisis Individual:**
```bash
# Pylint (calidad de código)
pylint --rcfile=.pylintrc src/ pages/ app.py

# Bandit (seguridad)
bandit -r src/ pages/ app.py -f json -o security_analysis/bandit_report.json

# Safety (dependencias)
safety check --json > security_analysis/safety_report.json

# pip-audit (auditoría de paquetes)
pip-audit --format=json --output=security_analysis/pip_audit_report.json
```

## 📈 Estado Actual

- **✅ Vulnerabilidades críticas**: 0
- **✅ Vulnerabilidades de seguridad**: 3 (severidad baja)
- **✅ Dependencias**: Seguras
- **✅ Código**: Limpio y organizado

## 🔄 Actualización de Reportes

Los reportes se actualizan automáticamente cuando se ejecutan los scripts. Para mantener la \
    documentación actualizada:

1. Ejecutar análisis después de cambios significativos
2. Actualizar reportes de documentación
3. Revisar vulnerabilidades nuevas

## 📞 Contacto

**Desarrollador**: Francisco Aucar  
**Proyecto**: CorAlertIntel Intelligence  
**Última actualización**: 15 de Octubre de 2025
