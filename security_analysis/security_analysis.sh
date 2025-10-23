#!/bin/bash
# Script de análisis de seguridad para CorAlertIntel
# Ejecutar en entorno virtual: venv_security\Scripts\activate

echo "🔍 Iniciando análisis de seguridad de CorAlertIntel..."
echo "=================================================="

# Verificar que estamos en el entorno virtual
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Advertencia: No se detectó entorno virtual activo"
    echo "   Ejecutar: venv_security\Scripts\activate"
fi

echo ""
echo "📊 1. ANÁLISIS PYLINT (Calidad de código)"
echo "=========================================="
pylint --rcfile=.pylintrc src/ pages/ app.py

echo ""
echo "🔒 2. ANÁLISIS BANDIT (Seguridad)"
echo "=================================="
bandit -r src/ pages/ app.py -f json -o bandit_report.json

echo ""
echo "📦 3. ANÁLISIS SAFETY (Dependencias vulnerables)"
echo "================================================="
safety check --json --output safety_report.json

echo ""
echo "🔍 4. ANÁLISIS PIP-AUDIT (Auditoría de paquetes)"
echo "================================================="
pip-audit --format=json --output=pip_audit_report.json

echo ""
echo "✅ Análisis completado!"
echo "📁 Reportes generados:"
echo "   - bandit_report.json"
echo "   - safety_report.json"
echo "   - pip_audit_report.json"
