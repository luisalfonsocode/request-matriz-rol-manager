@echo off
setlocal enabledelayedexpansion

:: =============================================================================
:: INSTALADOR RÁPIDO MATRIZ DE ROL
:: =============================================================================
:: Script simplificado para usuarios finales
:: Ubicación: setup/scripts/instalador_rapido.bat
:: =============================================================================

title Instalador Rápido - Matriz de Rol

:: Variables
set "SCRIPT_DIR=%~dp0"
set "SETUP_DIR=%SCRIPT_DIR%.."
set "PROJECT_ROOT=%SETUP_DIR%\.."

echo.
echo ████████████████████████████████████████████████████████████████████████████
echo ██                                                                        ██
echo ██    ⚡ INSTALADOR RÁPIDO - MATRIZ DE ROL                               ██
echo ██    Instalación automática con un solo clic                           ██
echo ██                                                                        ██
echo ████████████████████████████████████████████████████████████████████████████
echo.

echo 🎯 Este instalador configurará automáticamente todo lo necesario
echo    para ejecutar la aplicación Matriz de Rol.
echo.
echo 📋 Pasos que se ejecutarán:
echo    1. Verificar sistema
echo    2. Detectar Python
echo    3. Crear entorno virtual
echo    4. Instalar dependencias
echo    5. Configurar accesos directos
echo.

echo ¿Deseas continuar con la instalación? (s/n)
set /p "continuar="
if /i not "!continuar!"=="s" (
    echo.
    echo ❌ Instalación cancelada por el usuario
    pause
    exit /b 0
)

echo.
echo 🚀 Iniciando instalación automática...
echo.

:: =============================================================================
:: PASO 1: Verificación del sistema
:: =============================================================================
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo  📋 PASO 1/5: Verificando sistema...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

:: Buscar Python para verificación
for %%i in (python python3 py) do (
    %%i --version >nul 2>&1
    if !errorlevel! equ 0 (
        echo ✅ Python encontrado: %%i
        set "PYTHON_CMD=%%i"
        goto :python_ok
    )
)

echo ❌ Python no encontrado
echo.
echo 📥 Para continuar, necesitas instalar Python:
echo    1. Ve a: https://python.org/downloads/
echo    2. Descarga Python 3.9 o superior
echo    3. Durante la instalación, marca "Add Python to PATH"
echo    4. Reinicia este instalador
echo.
pause
exit /b 1

:python_ok

:: Ejecutar verificación completa
echo    Ejecutando verificación completa del sistema...
!PYTHON_CMD! "%SCRIPT_DIR%\verificar_sistema.py"
if !errorlevel! neq 0 (
    echo.
    echo ❌ La verificación del sistema encontró problemas críticos
    echo 📋 Revisa los detalles arriba y corrige los errores antes de continuar
    echo.
    pause
    exit /b 1
)

echo ✅ Verificación del sistema completada

:: =============================================================================
:: PASO 2-5: Ejecutar configuración principal
:: =============================================================================
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo  🔧 PASOS 2-5: Configurando entorno e instalando...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

call "%SCRIPT_DIR%\configurar_ambiente.bat"
if !errorlevel! neq 0 (
    echo.
    echo ❌ Error durante la configuración
    echo 📋 Revisa los logs en setup\logs\ para más información
    echo.
    pause
    exit /b 1
)

:: =============================================================================
:: RESUMEN FINAL
:: =============================================================================
echo.
echo ████████████████████████████████████████████████████████████████████████████
echo ██                                                                        ██
echo ██    🎉 ¡INSTALACIÓN COMPLETADA EXITOSAMENTE! 🎉                        ██
echo ██                                                                        ██
echo ████████████████████████████████████████████████████████████████████████████
echo.

echo 🚀 LA APLICACIÓN ESTÁ LISTA PARA USAR
echo.
echo 📱 Para ejecutar la aplicación:
echo    Doble clic en: ejecutar_matriz_rol.bat
echo.
echo 🔧 Para desarrollo:
echo    Doble clic en: activar_entorno_dev.bat
echo.
echo 📋 Documentación:
echo    Consulta: setup\docs\INSTALACION.md
echo.

echo ¿Deseas ejecutar la aplicación ahora? (s/n)
set /p "ejecutar_ahora="
if /i "!ejecutar_ahora!"=="s" (
    echo.
    echo 🚀 Ejecutando Matriz de Rol...
    start "" "%PROJECT_ROOT%\ejecutar_matriz_rol.bat"
    echo.
    echo ✅ Aplicación iniciada
    echo 👋 Puedes cerrar esta ventana
    timeout /t 3 >nul
) else (
    echo.
    echo 👋 ¡Instalación finalizada!
    echo    Puedes ejecutar la aplicación cuando quieras con ejecutar_matriz_rol.bat
    pause
)

exit /b 0
