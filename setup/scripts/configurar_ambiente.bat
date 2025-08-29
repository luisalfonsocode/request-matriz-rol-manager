@echo off
setlocal enabledelayedexpansion

:: =============================================================================
:: CONFIGURADOR AUTOMÁTICO MATRIZ DE ROL - Versión Refactorizada
:: =============================================================================
:: Script principal de configuración del entorno de desarrollo
:: Ubicación: setup/scripts/configurar_ambiente.bat
:: =============================================================================

:: Variables de configuración
set "SCRIPT_DIR=%~dp0"
set "SETUP_DIR=%SCRIPT_DIR%.."
set "PROJECT_ROOT=%SETUP_DIR%\.."
set "VENV_DIR=%PROJECT_ROOT%\venv"
set "LOG_FILE=%SETUP_DIR%\logs\setup.log"
set "PYTHON_EXE="

:: Crear directorio de logs si no existe
if not exist "%SETUP_DIR%\logs" mkdir "%SETUP_DIR%\logs"

:: Inicializar log
echo =============================================================================== > "%LOG_FILE%"
echo INICIO DE CONFIGURACIÓN - %date% %time% >> "%LOG_FILE%"
echo =============================================================================== >> "%LOG_FILE%"

echo.
echo ████████████████████████████████████████████████████████████████████████████
echo ██                                                                        ██
echo ██    🚀 CONFIGURADOR MATRIZ DE ROL v3.0                                 ██
echo ██    Instalación automatizada y configuración completa                  ██
echo ██                                                                        ██
echo ████████████████████████████████████████████████████████████████████████████
echo.

echo 📂 Directorio del proyecto: %PROJECT_ROOT%
echo 📋 Log de instalación: %LOG_FILE%
echo.

:: =============================================================================
:: FUNCIÓN: Buscar Python
:: =============================================================================
echo 🔍 Verificando instalación de Python...
echo [%time%] Buscando Python... >> "%LOG_FILE%"

:: Buscar en comandos comunes
for %%i in (python python3 py) do (
    %%i --version >nul 2>&1
    if !errorlevel! equ 0 (
        for /f "tokens=*" %%j in ('%%i -c "import sys; print(sys.executable)"') do (
            set "PYTHON_EXE=%%j"
            echo [%time%] Python encontrado: %%j >> "%LOG_FILE%"
            goto :python_found
        )
    )
)

:: Buscar en ubicaciones específicas
for %%p in (
    "C:\Python*\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python*\python.exe"
    "%PROGRAMFILES%\Python*\python.exe"
    "%PROGRAMFILES(X86)%\Python*\python.exe"
) do (
    for /f "delims=" %%f in ('dir /b "%%p" 2^>nul') do (
        "%%f" --version >nul 2>&1
        if !errorlevel! equ 0 (
            set "PYTHON_EXE=%%f"
            echo [%time%] Python encontrado en: %%f >> "%LOG_FILE%"
            goto :python_found
        )
    )
)

:python_not_found
echo ❌ ERROR: Python no está instalado o no se encuentra en el PATH
echo [%time%] ERROR: Python no encontrado >> "%LOG_FILE%"
echo.
echo 📥 Para instalar Python:
echo    1. Ve a: https://python.org/downloads/
echo    2. Descarga Python 3.9 o superior
echo    3. Durante la instalación, marca "Add Python to PATH"
echo    4. Ejecuta este script nuevamente
echo.
echo 📖 Consulta: %SETUP_DIR%\docs\INSTALACION.md para más información
pause
exit /b 1

:python_found
echo ✅ Python encontrado: %PYTHON_EXE%

:: Verificar versión
for /f "tokens=2 delims= " %%v in ('"%PYTHON_EXE%" --version') do set "PYTHON_VERSION=%%v"
echo    Versión: %PYTHON_VERSION%
echo [%time%] Versión de Python: %PYTHON_VERSION% >> "%LOG_FILE%"

:: Verificar compatibilidad
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set /a major=%%a
    set /a minor=%%b
)

if %major% lss 3 (
    echo ❌ ERROR: Se requiere Python 3.9+. Versión actual: %PYTHON_VERSION%
    echo [%time%] ERROR: Versión incompatible: %PYTHON_VERSION% >> "%LOG_FILE%"
    pause
    exit /b 1
)

if %major% equ 3 if %minor% lss 9 (
    echo ❌ ERROR: Se requiere Python 3.9+. Versión actual: %PYTHON_VERSION%
    echo [%time%] ERROR: Versión incompatible: %PYTHON_VERSION% >> "%LOG_FILE%"
    pause
    exit /b 1
)

echo ✅ Versión compatible
echo.

:: =============================================================================
:: FUNCIÓN: Configurar entorno virtual
:: =============================================================================
echo 🔧 Configurando entorno virtual...
echo [%time%] Configurando entorno virtual >> "%LOG_FILE%"

if exist "%VENV_DIR%" (
    echo    Eliminando entorno virtual anterior...
    echo [%time%] Eliminando venv existente >> "%LOG_FILE%"
    rmdir /s /q "%VENV_DIR%"
)

echo    Creando nuevo entorno virtual...
"%PYTHON_EXE%" -m venv "%VENV_DIR%"
if !errorlevel! neq 0 (
    echo ❌ ERROR: No se pudo crear el entorno virtual
    echo [%time%] ERROR: Falló creación de venv >> "%LOG_FILE%"
    pause
    exit /b 1
)

echo ✅ Entorno virtual creado
echo [%time%] Entorno virtual creado exitosamente >> "%LOG_FILE%"
echo.

:: =============================================================================
:: FUNCIÓN: Instalar dependencias
:: =============================================================================
echo 📦 Instalando dependencias...
echo [%time%] Iniciando instalación de dependencias >> "%LOG_FILE%"

set "VENV_PYTHON=%VENV_DIR%\Scripts\python.exe"
set "VENV_PIP=%VENV_DIR%\Scripts\pip.exe"

:: Verificar entorno virtual
if not exist "%VENV_PYTHON%" (
    echo ❌ ERROR: No se pudo activar el entorno virtual
    echo [%time%] ERROR: Entorno virtual no accesible >> "%LOG_FILE%"
    pause
    exit /b 1
)

:: Actualizar pip
echo    Actualizando pip...
"%VENV_PYTHON%" -m pip install --upgrade pip --quiet
echo [%time%] pip actualizado >> "%LOG_FILE%"

:: Cambiar al directorio del proyecto
cd /d "%PROJECT_ROOT%"

:: Instalar paquete principal
echo    Instalando paquete principal...
"%VENV_PIP%" install -e . --quiet
if !errorlevel! neq 0 (
    echo ❌ ERROR: No se pudieron instalar las dependencias principales
    echo [%time%] ERROR: Falló instalación principal >> "%LOG_FILE%"
    pause
    exit /b 1
)

echo [%time%] Paquete principal instalado >> "%LOG_FILE%"

:: Instalar dependencias de desarrollo
echo    Instalando dependencias de desarrollo...
"%VENV_PIP%" install -e .[dev] --quiet 2>nul
echo [%time%] Dependencias de desarrollo instaladas >> "%LOG_FILE%"

:: Instalar dependencias de testing
echo    Instalando dependencias de testing...
"%VENV_PIP%" install -e .[test] --quiet 2>nul
echo [%time%] Dependencias de testing instaladas >> "%LOG_FILE%"

echo ✅ Dependencias instaladas correctamente
echo.

:: =============================================================================
:: FUNCIÓN: Verificar instalación
:: =============================================================================
echo 🧪 Verificando instalación...
echo [%time%] Verificando instalación >> "%LOG_FILE%"

:: Test 1: Módulo principal
"%VENV_PYTHON%" -c "from src.matriz_rol.gui.aplicacion_principal import AplicacionMatrizRol; print('Módulo principal OK')" >nul 2>&1
if !errorlevel! neq 0 (
    echo ❌ ERROR: No se puede importar el módulo principal
    echo [%time%] ERROR: Fallo en verificación módulo principal >> "%LOG_FILE%"
    pause
    exit /b 1
)

:: Test 2: Módulo refactorizado
"%VENV_PYTHON%" -c "from src.matriz_rol.gui.gestion_solicitudes import GestionSolicitudesFrame; print('Módulo refactorizado OK')" >nul 2>&1
if !errorlevel! neq 0 (
    echo ❌ ERROR: No se puede importar el módulo refactorizado
    echo [%time%] ERROR: Fallo en verificación módulo refactorizado >> "%LOG_FILE%"
    pause
    exit /b 1
)

echo ✅ Verificación exitosa
echo [%time%] Verificación completada exitosamente >> "%LOG_FILE%"
echo.

:: =============================================================================
:: FUNCIÓN: Crear scripts de acceso
:: =============================================================================
echo 🔗 Creando scripts de acceso directo...
echo [%time%] Creando scripts de acceso >> "%LOG_FILE%"

:: Script principal de ejecución
echo @echo off > "%PROJECT_ROOT%\ejecutar_matriz_rol.bat"
echo title Matriz de Rol >> "%PROJECT_ROOT%\ejecutar_matriz_rol.bat"
echo cd /d "%PROJECT_ROOT%" >> "%PROJECT_ROOT%\ejecutar_matriz_rol.bat"
echo "%VENV_PYTHON%" -c "from src.matriz_rol.gui.aplicacion_principal import AplicacionMatrizRol; app = AplicacionMatrizRol(); app.mainloop()" >> "%PROJECT_ROOT%\ejecutar_matriz_rol.bat"
echo if errorlevel 1 ( >> "%PROJECT_ROOT%\ejecutar_matriz_rol.bat"
echo     echo. >> "%PROJECT_ROOT%\ejecutar_matriz_rol.bat"
echo     echo ❌ Error ejecutando la aplicación >> "%PROJECT_ROOT%\ejecutar_matriz_rol.bat"
echo     echo 📋 Revisa el log: %LOG_FILE% >> "%PROJECT_ROOT%\ejecutar_matriz_rol.bat"
echo     pause >> "%PROJECT_ROOT%\ejecutar_matriz_rol.bat"
echo ) >> "%PROJECT_ROOT%\ejecutar_matriz_rol.bat"

:: Script de activación de entorno
echo @echo off > "%PROJECT_ROOT%\activar_entorno_dev.bat"
echo title Entorno de Desarrollo - Matriz de Rol >> "%PROJECT_ROOT%\activar_entorno_dev.bat"
echo cd /d "%PROJECT_ROOT%" >> "%PROJECT_ROOT%\activar_entorno_dev.bat"
echo call "%VENV_DIR%\Scripts\activate.bat" >> "%PROJECT_ROOT%\activar_entorno_dev.bat"
echo echo. >> "%PROJECT_ROOT%\activar_entorno_dev.bat"
echo echo 🎯 Entorno de desarrollo activado >> "%PROJECT_ROOT%\activar_entorno_dev.bat"
echo echo 📋 Comandos disponibles: >> "%PROJECT_ROOT%\activar_entorno_dev.bat"
echo echo    python -c "from src.matriz_rol.gui.aplicacion_principal import AplicacionMatrizRol; app = AplicacionMatrizRol(); app.mainloop()" >> "%PROJECT_ROOT%\activar_entorno_dev.bat"
echo echo    python -m pytest tests/ >> "%PROJECT_ROOT%\activar_entorno_dev.bat"
echo echo    black src/ >> "%PROJECT_ROOT%\activar_entorno_dev.bat"
echo echo. >> "%PROJECT_ROOT%\activar_entorno_dev.bat"
echo cmd /k >> "%PROJECT_ROOT%\activar_entorno_dev.bat"

:: Script de reinstalación rápida
echo @echo off > "%PROJECT_ROOT%\reinstalar.bat"
echo title Reinstalación Rápida - Matriz de Rol >> "%PROJECT_ROOT%\reinstalar.bat"
echo echo 🔄 Reinstalando Matriz de Rol... >> "%PROJECT_ROOT%\reinstalar.bat"
echo call "%SCRIPT_DIR%\configurar_ambiente.bat" >> "%PROJECT_ROOT%\reinstalar.bat"

echo ✅ Scripts creados:
echo    📱 ejecutar_matriz_rol.bat - Ejecutar aplicación
echo    🔧 activar_entorno_dev.bat - Modo desarrollo
echo    🔄 reinstalar.bat - Reinstalación rápida
echo.

:: =============================================================================
:: FUNCIÓN: Crear archivo de configuración
:: =============================================================================
echo 📄 Creando configuración del entorno...
echo [%time%] Creando configuración >> "%LOG_FILE%"

echo # Configuración del Entorno - Matriz de Rol > "%PROJECT_ROOT%\.env"
echo # Generado automáticamente: %date% %time% >> "%PROJECT_ROOT%\.env"
echo. >> "%PROJECT_ROOT%\.env"
echo PROJECT_ROOT=%PROJECT_ROOT% >> "%PROJECT_ROOT%\.env"
echo VENV_DIR=%VENV_DIR% >> "%PROJECT_ROOT%\.env"
echo PYTHON_EXE=%VENV_PYTHON% >> "%PROJECT_ROOT%\.env"
echo PYTHON_VERSION=%PYTHON_VERSION% >> "%PROJECT_ROOT%\.env"
echo SETUP_DATE=%date% %time% >> "%PROJECT_ROOT%\.env"
echo LOG_FILE=%LOG_FILE% >> "%PROJECT_ROOT%\.env"

echo ✅ Configuración guardada en .env
echo.

:: =============================================================================
:: RESUMEN FINAL
:: =============================================================================
echo [%time%] Configuración completada exitosamente >> "%LOG_FILE%"
echo =============================================================================== >> "%LOG_FILE%"

echo.
echo ████████████████████████████████████████████████████████████████████████████
echo ██                                                                        ██
echo ██    🎉 CONFIGURACIÓN COMPLETADA EXITOSAMENTE 🎉                        ██
echo ██                                                                        ██
echo ████████████████████████████████████████████████████████████████████████████
echo.

echo 📋 RESUMEN:
echo    ✅ Python %PYTHON_VERSION% verificado
echo    ✅ Entorno virtual configurado
echo    ✅ Dependencias instaladas
echo    ✅ Verificación exitosa
echo    ✅ Scripts de acceso creados
echo    ✅ Configuración guardada
echo.

echo 🚀 EJECUTAR LA APLICACIÓN:
echo    📱 Doble clic en: ejecutar_matriz_rol.bat
echo.

echo 🔧 DESARROLLO:
echo    💻 Doble clic en: activar_entorno_dev.bat
echo.

echo 🔄 REINSTALAR:
echo    🛠️  Doble clic en: reinstalar.bat
echo.

echo 📖 DOCUMENTACIÓN:
echo    📋 setup\docs\INSTALACION.md
echo    🔧 setup\docs\TROUBLESHOOTING.md
echo.

pause

echo.
echo ¿Deseas ejecutar la aplicación ahora? (s/n)
set /p "ejecutar_ahora="
if /i "!ejecutar_ahora!"=="s" (
    echo.
    echo 🚀 Ejecutando aplicación...
    call "%PROJECT_ROOT%\ejecutar_matriz_rol.bat"
)

echo.
echo 👋 ¡Configuración finalizada! La aplicación está lista para usar.
exit /b 0
