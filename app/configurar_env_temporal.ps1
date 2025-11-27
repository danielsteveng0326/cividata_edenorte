# Script para configurar la variable de entorno temporalmente
# Ejecutar ANTES de iniciar el servidor

Write-Host "Configurando variable de entorno GEMINI_API_KEY..." -ForegroundColor Green
$env:GEMINI_API_KEY="AIzaSyDHfLmtrYnDgkTWb43DXFftk2XMZGy_4wY"

Write-Host "✅ Variable configurada para esta sesión" -ForegroundColor Green
Write-Host ""
Write-Host "Ahora ejecute:" -ForegroundColor Cyan
Write-Host "  python manage.py runserver" -ForegroundColor White
Write-Host ""
Write-Host "Verificando variable..." -ForegroundColor Yellow
Write-Host "GEMINI_API_KEY = $env:GEMINI_API_KEY" -ForegroundColor White
