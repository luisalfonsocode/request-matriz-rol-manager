@echo off
setlocal enabledelayedexpansion

:: =============================================================================
:: INSTALADOR MAESTRO MATRIZ DE ROL
:: =============================================================================
:: Script principal que redirige a los instaladores organizados
:: Ubicación: INSTALAR.bat (raíz del proyecto)
:: =============================================================================

title Instalador Matriz de Rol

echo.
echo ████████████████████████████████████████████████████████████████████████████
echo ██                                                                        ██
echo ██    🎯 INSTALADOR MATRIZ DE ROL v3.0                                   ██
echo ██    Sistema de instalación automática refactorizado                   ██
echo ██                                                                        ██
echo ████████████████████████████████████████████████████████████████████████████
echo.

echo 📁 Directorio del proyecto: %~dp0
echo 📋 Sistema de instalación organizado en: setup\
echo.

:: Verificar estructura del setup
if not exist "%~dp0setup\scripts\instalador_rapido.bat" (
    echo ❌ ERROR: No se encuentra el sistema de instalación
    echo    Falta: setup\scripts\instalador_rapido.bat
    echo.
    echo 📥 Solución:
    echo    1. Verifica que descargaste el proyecto completo
    echo    2. Asegúrate que existe la carpeta setup\scripts\
    echo.
    pause
    exit /b 1
)

echo ┌─────────────────────────────────────────────────────────────────────────────┐
echo │                        OPCIONES DE INSTALACIÓN                             │
echo ├─────────────────────────────────────────────────────────────────────────────┤
echo │                                                                             │
echo │  1️⃣  INSTALACIÓN RÁPIDA (Recomendada)                                      │
echo │     • Un solo clic                                                         │
echo │     • Configuración automática                                             │
echo │     • Ideal para usuarios finales                                          │
echo │                                                                             │
echo │  2️⃣  INSTALACIÓN COMPLETA                                                  │
echo │     • Control detallado del proceso                                        │
echo │     • Logs de instalación                                                  │
echo │     • Ideal para usuarios técnicos                                         │
echo │                                                                             │
echo │  3️⃣  INSTALACIÓN AVANZADA (PowerShell)                                     │
echo │     • Opciones de configuración avanzadas                                  │
echo │     • Modo desarrollo disponible                                           │
echo │     • Ideal para desarrolladores                                           │
echo │                                                                             │
echo │  4️⃣  VERIFICACIÓN DEL SISTEMA                                              │
echo │     • Diagnóstico previo a instalación                                     │
echo │     • Identificación de problemas                                          │
echo │     • Recomendado si hay errores                                           │
echo │                                                                             │
echo │  5️⃣  VER DOCUMENTACIÓN                                                     │
echo │     • Guías de instalación detalladas                                      │
echo │     • Solución de problemas                                                │
echo │     • Configuración avanzada                                               │
echo │                                                                             │
echo └─────────────────────────────────────────────────────────────────────────────┘
echo.

:menu
set /p "opcion=Elige una opción (1-5): "

if "!opcion!"=="1" goto instalacion_rapida
if "!opcion!"=="2" goto instalacion_completa
if "!opcion!"=="3" goto instalacion_avanzada
if "!opcion!"=="4" goto verificacion_sistema
if "!opcion!"=="5" goto ver_documentacion

echo ❌ Opción inválida. Por favor elige 1, 2, 3, 4 o 5.
echo.
goto menu

:instalacion_rapida
echo.
echo 🚀 Iniciando INSTALACIÓN RÁPIDA...
echo    Script: setup\scripts\instalador_rapido.bat
echo.
call "%~dp0setup\scripts\instalador_rapido.bat"
goto final

:instalacion_completa
echo.
echo 🔧 Iniciando INSTALACIÓN COMPLETA...
echo    Script: setup\scripts\configurar_ambiente.bat
echo.
call "%~dp0setup\scripts\configurar_ambiente.bat"
goto final

:instalacion_avanzada
echo.
echo ⚡ Iniciando INSTALACIÓN AVANZADA...
echo    Script: setup\scripts\configurar_ambiente.ps1
echo.

:: Verificar PowerShell
powershell -Command "Get-Host" >nul 2>&1
if !errorlevel! neq 0 (
    echo ❌ PowerShell no está disponible
    echo    Usando instalación completa como alternativa...
    echo.
    call "%~dp0setup\scripts\configurar_ambiente.bat"
    goto final
)

echo 📋 Opciones avanzadas disponibles:
echo    • Usar -Force para forzar recreación
echo    • Usar -DevMode para herramientas de desarrollo
echo    • Usar -Quiet para modo silencioso
echo.

set /p "usar_opciones=¿Deseas usar opciones avanzadas? (s/n): "
if /i "!usar_opciones!"=="s" (
    echo.
    echo Opciones disponibles:
    echo   -Force     : Forzar recreación del entorno
    echo   -DevMode   : Instalar herramientas de desarrollo
    echo   -Quiet     : Modo silencioso
    echo.
    set /p "parametros=Introduce parámetros (ej: -Force -DevMode): "
    powershell -ExecutionPolicy Bypass -File "%~dp0setup\scripts\configurar_ambiente.ps1" !parametros!
) else (
    powershell -ExecutionPolicy Bypass -File "%~dp0setup\scripts\configurar_ambiente.ps1"
)
goto final

:verificacion_sistema
echo.
echo 🔍 Iniciando VERIFICACIÓN DEL SISTEMA...
echo    Script: setup\scripts\verificar_sistema.py
echo.

:: Buscar Python
for %%i in (python python3 py) do (
    %%i --version >nul 2>&1
    if !errorlevel! equ 0 (
        echo ✅ Ejecutando verificación con: %%i
        %%i "%~dp0setup\scripts\verificar_sistema.py"
        goto verificacion_completada
    )
)

echo ❌ Python no encontrado
echo.
echo 📥 Para ejecutar la verificación necesitas Python instalado:
echo    1. Ve a: https://python.org/downloads/
echo    2. Descarga Python 3.9 o superior
echo    3. Durante la instalación, marca "Add Python to PATH"
echo    4. Ejecuta este script nuevamente
echo.

:verificacion_completada
echo.
echo 📋 Verificación completada.
echo    Revisa los resultados arriba para identificar problemas.
echo.
echo ¿Deseas proceder con la instalación? (s/n)
set /p "proceder="
if /i "!proceder!"=="s" goto menu

goto final

:ver_documentacion
echo.
echo 📖 DOCUMENTACIÓN DISPONIBLE:
echo.
echo    📋 Guía de Instalación Completa:
echo       setup\docs\INSTALACION.md
echo.
echo    🛠️  Solución de Problemas:
echo       setup\docs\TROUBLESHOOTING.md
echo.
echo    ⚙️  Configuración Avanzada:
echo       setup\docs\CONFIGURACION.md
echo.

set /p "abrir_doc=¿Deseas abrir una guía? (1=Instalación, 2=Problemas, 3=Configuración, n=No): "

if "!abrir_doc!"=="1" (
    echo 📖 Abriendo guía de instalación...
    start "" "%~dp0setup\docs\INSTALACION.md"
)
if "!abrir_doc!"=="2" (
    echo 🛠️ Abriendo guía de problemas...
    start "" "%~dp0setup\docs\TROUBLESHOOTING.md"
)
if "!abrir_doc!"=="3" (
    echo ⚙️ Abriendo configuración avanzada...
    start "" "%~dp0setup\docs\CONFIGURACION.md"
)

echo.
echo 🔙 Regresando al menú principal...
echo.
goto menu

:final
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo  INSTALADOR MATRIZ DE ROL - PROCESO COMPLETADO
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

if exist "%~dp0ejecutar_matriz_rol.bat" (
    echo ✅ La instalación parece haber sido exitosa
    echo.
    echo 🚀 ARCHIVOS DISPONIBLES:
    echo    📱 ejecutar_matriz_rol.bat - Ejecutar aplicación
    echo    🔧 activar_entorno_dev.bat - Modo desarrollo
    echo    🔄 reinstalar.bat - Reinstalar rápidamente
    echo.
    echo 📋 DOCUMENTACIÓN:
    echo    📖 setup\docs\ - Guías completas
    echo.
) else (
    echo ⚠️  No se detectaron archivos de instalación exitosa
    echo    Revisa los mensajes de error anteriores
    echo.
    echo 📋 Para diagnóstico:
    echo    • Ejecuta opción 4 (Verificación del Sistema)
    echo    • Revisa setup\logs\ para logs detallados
    echo    • Consulta setup\docs\TROUBLESHOOTING.md
    echo.
)

echo 👋 Gracias por usar el instalador de Matriz de Rol
pause
exit /b 0
