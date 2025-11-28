#!/bin/bash

# -----------------------------------------------------
# Script para añadir, commitear y pushear cambios a Git
# Uso: ./actualiza.sh "Tu mensaje de commit"
# -----------------------------------------------------

# Termina el script inmediatamente si cualquier comando falla
set -e

# 1. Verificar que se ha proporcionado un mensaje de commit
if [ $# -eq 0 ]; then
    echo ""
    echo "🛑 Error: No se proporcionó un mensaje de commit."
    echo "Uso: $0 \"Tu mensaje de commit\""
    exit 1
fi

# 2. Tomar todos los argumentos como el mensaje del commit
#    Esto permite usar: ./actualiza.sh "un mensaje largo"
#    O también:         ./actualiza.sh un mensaje simple
MENSAJE_COMMIT="$*"

# 3. Ejecutar la secuencia de Git
echo ""
echo "🔄 1/3: Añadiendo todos los archivos (git add -A)..."
git add .

echo ""
echo "📝 2/3: Creando commit con mensaje: \"$MENSAJE_COMMIT\"..."
git commit -m "$MENSAJE_COMMIT"

echo ""
echo "🚀 3/3: Subiendo cambios al repositorio remoto (git push)..."
git push origin main

echo ""
echo "✅ ¡Proceso completado!"
echo ""
