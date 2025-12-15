# Script para configurar la variable de entorno GEMINI_API_KEY en Windows
# Ejecutar en PowerShell como Administrador

$GEMINI_API_KEY = "AIzaSyDHfLmtrYnDgkTWb43DXFftk2XMZGy_4wY"

Write-Host "Configurando GEMINI_API_KEY..." -ForegroundColor Green

# Configurar para el usuario actual (permanente)
[System.Environment]::SetEnvironmentVariable('GEMINI_API_KEY', $GEMINI_API_KEY, 'User')

Write-Host "✅ Variable de entorno GEMINI_API_KEY configurada correctamente" -ForegroundColor Green
Write-Host ""
Write-Host "⚠️  IMPORTANTE: Debe cerrar y volver a abrir la terminal para que los cambios surtan efecto" -ForegroundColor Yellow
Write-Host ""
Write-Host "Para verificar, ejecute en una nueva terminal:" -ForegroundColor Cyan
Write-Host "  echo `$env:GEMINI_API_KEY" -ForegroundColor White
