#Requires -Version 5.1

<#
.SYNOPSIS
    Configurador avanzado de entorno para Matriz de Rol - Versión PowerShell

.DESCRIPTION
    Script de PowerShell para configuración automatizada del entorno de desarrollo
    de la aplicación Matriz de Rol. Incluye detección automática de Python,
    configuración de entorno virtual, instalación de dependencias y verificación.

.PARAMETER Force
    Fuerza la recreación del entorno virtual aunque ya exista

.PARAMETER SkipTests
    Omite la ejecución de pruebas de verificación

.PARAMETER Quiet
    Ejecuta en modo silencioso con salida mínima

.PARAMETER DevMode
    Instala dependencias adicionales de desarrollo

.EXAMPLE
    .\configurar_ambiente.ps1
    Ejecuta la configuración estándar

.EXAMPLE
    .\configurar_ambiente.ps1 -Force -DevMode
    Fuerza recreación con modo desarrollo

.NOTES
    Autor: Sistema de Configuración Automática
    Versión: 3.0
    Ubicación: setup/scripts/configurar_ambiente.ps1
#>

param(
    [switch]$Force,
    [switch]$SkipTests,
    [switch]$Quiet,
    [switch]$DevMode
)

# =============================================================================
# CONFIGURACIÓN INICIAL
# =============================================================================

# Configuración de variables globales
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# Rutas del proyecto
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SetupDir = Split-Path -Parent $ScriptDir
$ProjectRoot = Split-Path -Parent $SetupDir
$VenvDir = Join-Path $ProjectRoot "venv"
$LogsDir = Join-Path $SetupDir "logs"
$LogFile = Join-Path $LogsDir "setup_powershell.log"

# Crear directorio de logs
if (-not (Test-Path $LogsDir)) {
    New-Item -ItemType Directory -Path $LogsDir -Force | Out-Null
}

# Funciones de logging y salida
function Write-Log {
    param($Message, $Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp [$Level] $Message" | Out-File -FilePath $LogFile -Append
}

function Write-ColorOutput {
    param($Message, $Color = "White")
    if (-not $Quiet) {
        Write-Host $Message -ForegroundColor $Color
    }
    Write-Log $Message
}

function Write-Header {
    param($Title)
    if (-not $Quiet) {
        Write-Host ""
        Write-Host "═══════════════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
        Write-Host "  $Title" -ForegroundColor Yellow
        Write-Host "═══════════════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
        Write-Host ""
    }
    Write-Log "=== $Title ==="
}

function Write-Success {
    param($Message)
    Write-ColorOutput "✅ $Message" "Green"
}

function Write-Warning {
    param($Message)
    Write-ColorOutput "⚠️  $Message" "Yellow"
}

function Write-Error {
    param($Message)
    Write-ColorOutput "❌ $Message" "Red"
}

function Write-Info {
    param($Message)
    Write-ColorOutput "ℹ️  $Message" "Cyan"
}

# =============================================================================
# FUNCIONES PRINCIPALES
# =============================================================================

function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Find-Python {
    Write-Header "DETECCIÓN DE PYTHON"

    $pythonCandidates = @(
        "python",
        "python3",
        "py"
    )

    # Buscar en PATH
    foreach ($cmd in $pythonCandidates) {
        try {
            $version = & $cmd --version 2>&1
            if ($LASTEXITCODE -eq 0) {
                $executable = & $cmd -c "import sys; print(sys.executable)" 2>&1
                if ($LASTEXITCODE -eq 0) {
                    Write-Success "Python encontrado: $executable"
                    Write-Info "Versión: $version"
                    return $executable
                }
            }
        }
        catch {
            continue
        }
    }

    # Buscar en ubicaciones comunes
    $commonPaths = @(
        "$env:LOCALAPPDATA\Programs\Python\Python*\python.exe",
        "$env:PROGRAMFILES\Python*\python.exe",
        "${env:PROGRAMFILES(X86)}\Python*\python.exe",
        "C:\Python*\python.exe"
    )

    foreach ($pattern in $commonPaths) {
        $paths = Get-ChildItem -Path $pattern -ErrorAction SilentlyContinue
        foreach ($path in $paths) {
            try {
                $version = & $path.FullName --version 2>&1
                if ($LASTEXITCODE -eq 0) {
                    Write-Success "Python encontrado: $($path.FullName)"
                    Write-Info "Versión: $version"
                    return $path.FullName
                }
            }
            catch {
                continue
            }
        }
    }

    throw "Python no encontrado. Instala Python 3.9+ desde https://python.org"
}

function Test-PythonVersion {
    param($PythonExe)

    $versionOutput = & $PythonExe --version 2>&1
    $versionMatch = $versionOutput | Select-String "Python (\d+)\.(\d+)\.(\d+)"

    if ($versionMatch) {
        $major = [int]$versionMatch.Matches[0].Groups[1].Value
        $minor = [int]$versionMatch.Matches[0].Groups[2].Value

        if ($major -ge 3 -and $minor -ge 9) {
            Write-Success "Versión de Python compatible: $versionOutput"
            return $true
        }
        else {
            Write-Error "Se requiere Python 3.9+. Versión actual: $versionOutput"
            return $false
        }
    }
    else {
        Write-Error "No se pudo determinar la versión de Python"
        return $false
    }
}

function New-VirtualEnvironment {
    param($PythonExe)

    Write-Header "CONFIGURACIÓN DE ENTORNO VIRTUAL"

    if (Test-Path $VenvDir) {
        if ($Force) {
            Write-Warning "Eliminando entorno virtual existente..."
            Remove-Item -Path $VenvDir -Recurse -Force
            Write-Success "Entorno virtual anterior eliminado"
        }
        else {
            Write-Info "Entorno virtual ya existe. Usa -Force para recrear."
            return $true
        }
    }

    Write-Info "Creando entorno virtual..."
    try {
        & $PythonExe -m venv $VenvDir
        if ($LASTEXITCODE -ne 0) {
            throw "Error creando entorno virtual"
        }
        Write-Success "Entorno virtual creado exitosamente"
        return $true
    }
    catch {
        Write-Error "No se pudo crear el entorno virtual: $_"
        return $false
    }
}

function Install-Dependencies {
    Write-Header "INSTALACIÓN DE DEPENDENCIAS"

    $venvPython = Join-Path $VenvDir "Scripts\python.exe"
    $venvPip = Join-Path $VenvDir "Scripts\pip.exe"

    if (-not (Test-Path $venvPython)) {
        Write-Error "No se encontró Python en el entorno virtual"
        return $false
    }

    # Cambiar al directorio del proyecto
    Push-Location $ProjectRoot

    try {
        # Actualizar pip
        Write-Info "Actualizando pip..."
        & $venvPython -m pip install --upgrade pip --quiet

        # Instalar paquete principal
        Write-Info "Instalando paquete principal..."
        & $venvPip install -e . --quiet
        if ($LASTEXITCODE -ne 0) {
            throw "Error instalando paquete principal"
        }

        # Instalar dependencias de desarrollo si está en modo dev
        if ($DevMode) {
            Write-Info "Instalando dependencias de desarrollo..."
            & $venvPip install -e ".[dev]" --quiet 2>$null

            Write-Info "Instalando dependencias de testing..."
            & $venvPip install -e ".[test]" --quiet 2>$null
        }

        Write-Success "Dependencias instaladas correctamente"
        return $true
    }
    catch {
        Write-Error "Error instalando dependencias: $_"
        return $false
    }
    finally {
        Pop-Location
    }
}

function Test-Installation {
    if ($SkipTests) {
        Write-Info "Omitiendo pruebas de verificación"
        return $true
    }

    Write-Header "VERIFICACIÓN DE INSTALACIÓN"

    $venvPython = Join-Path $VenvDir "Scripts\python.exe"

    # Test 1: Módulo principal
    Write-Info "Verificando módulo principal..."
    try {
        & $venvPython -c "from src.matriz_rol.gui.aplicacion_principal import AplicacionMatrizRol; print('Módulo principal OK')" 2>$null
        if ($LASTEXITCODE -ne 0) {
            throw "Error importando módulo principal"
        }
        Write-Success "Módulo principal verificado"
    }
    catch {
        Write-Error "No se puede importar el módulo principal"
        return $false
    }

    # Test 2: Módulo refactorizado
    Write-Info "Verificando módulo refactorizado..."
    try {
        & $venvPython -c "from src.matriz_rol.gui.gestion_solicitudes import GestionSolicitudesFrame; print('Módulo refactorizado OK')" 2>$null
        if ($LASTEXITCODE -ne 0) {
            throw "Error importando módulo refactorizado"
        }
        Write-Success "Módulo refactorizado verificado"
    }
    catch {
        Write-Error "No se puede importar el módulo refactorizado"
        return $false
    }

    Write-Success "Verificación completada exitosamente"
    return $true
}

function New-AccessScripts {
    Write-Header "CREACIÓN DE SCRIPTS DE ACCESO"

    $venvPython = Join-Path $VenvDir "Scripts\python.exe"

    # Script principal de ejecución
    $ejecutarScript = @"
@echo off
title Matriz de Rol
cd /d "$ProjectRoot"
"$venvPython" -c "from src.matriz_rol.gui.aplicacion_principal import AplicacionMatrizRol; app = AplicacionMatrizRol(); app.mainloop()"
if errorlevel 1 (
    echo.
    echo ❌ Error ejecutando la aplicación
    echo 📋 Revisa el log: $LogFile
    pause
)
"@

    $ejecutarPath = Join-Path $ProjectRoot "ejecutar_matriz_rol.bat"
    Set-Content -Path $ejecutarPath -Value $ejecutarScript -Encoding UTF8
    Write-Success "Script de ejecución creado: ejecutar_matriz_rol.bat"

    # Script de activación de entorno
    $activarScript = @"
@echo off
title Entorno de Desarrollo - Matriz de Rol
cd /d "$ProjectRoot"
call "$VenvDir\Scripts\activate.bat"
echo.
echo 🎯 Entorno de desarrollo activado
echo 📋 Comandos disponibles:
echo    python -c "from src.matriz_rol.gui.aplicacion_principal import AplicacionMatrizRol; app = AplicacionMatrizRol(); app.mainloop()"
echo    python -m pytest tests/
echo    black src/
echo.
cmd /k
"@

    $activarPath = Join-Path $ProjectRoot "activar_entorno_dev.bat"
    Set-Content -Path $activarPath -Value $activarScript -Encoding UTF8
    Write-Success "Script de desarrollo creado: activar_entorno_dev.bat"

    # Script de reinstalación
    $reinstalarScript = @"
@echo off
title Reinstalación Rápida - Matriz de Rol
echo 🔄 Reinstalando Matriz de Rol...
powershell -ExecutionPolicy Bypass -File "$ScriptDir\configurar_ambiente.ps1" -Force
"@

    $reinstalarPath = Join-Path $ProjectRoot "reinstalar.bat"
    Set-Content -Path $reinstalarPath -Value $reinstalarScript -Encoding UTF8
    Write-Success "Script de reinstalación creado: reinstalar.bat"

    return $true
}

function New-EnvironmentConfig {
    Write-Header "CONFIGURACIÓN DEL ENTORNO"

    $configContent = @"
# Configuración del Entorno - Matriz de Rol
# Generado automáticamente: $(Get-Date)

PROJECT_ROOT=$ProjectRoot
VENV_DIR=$VenvDir
PYTHON_EXE=$(Join-Path $VenvDir "Scripts\python.exe")
SETUP_DATE=$(Get-Date)
LOG_FILE=$LogFile
SETUP_MODE=PowerShell
"@

    $envPath = Join-Path $ProjectRoot ".env"
    Set-Content -Path $envPath -Value $configContent -Encoding UTF8
    Write-Success "Configuración guardada en .env"

    return $true
}

function Show-Summary {
    param($PythonVersion, $Success)

    if (-not $Quiet) {
        Write-Host ""
        Write-Host "════════════════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
        if ($Success) {
            Write-Host "    🎉 CONFIGURACIÓN COMPLETADA EXITOSAMENTE 🎉" -ForegroundColor Green
        } else {
            Write-Host "    ❌ CONFIGURACIÓN FALLIDA ❌" -ForegroundColor Red
        }
        Write-Host "════════════════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
        Write-Host ""

        if ($Success) {
            Write-Host "📋 RESUMEN:" -ForegroundColor Yellow
            Write-Host "   ✅ Python $PythonVersion verificado" -ForegroundColor Green
            Write-Host "   ✅ Entorno virtual configurado" -ForegroundColor Green
            Write-Host "   ✅ Dependencias instaladas" -ForegroundColor Green
            Write-Host "   ✅ Verificación exitosa" -ForegroundColor Green
            Write-Host "   ✅ Scripts de acceso creados" -ForegroundColor Green
            Write-Host "   ✅ Configuración guardada" -ForegroundColor Green
            Write-Host ""

            Write-Host "🚀 EJECUTAR LA APLICACIÓN:" -ForegroundColor Yellow
            Write-Host "   📱 Doble clic en: ejecutar_matriz_rol.bat" -ForegroundColor Cyan
            Write-Host ""

            Write-Host "🔧 DESARROLLO:" -ForegroundColor Yellow
            Write-Host "   💻 Doble clic en: activar_entorno_dev.bat" -ForegroundColor Cyan
            Write-Host ""

            Write-Host "🔄 REINSTALAR:" -ForegroundColor Yellow
            Write-Host "   🛠️  Doble clic en: reinstalar.bat" -ForegroundColor Cyan
            Write-Host ""

            Write-Host "📖 DOCUMENTACIÓN:" -ForegroundColor Yellow
            Write-Host "   📋 setup\docs\INSTALACION.md" -ForegroundColor Cyan
            Write-Host "   🔧 setup\docs\TROUBLESHOOTING.md" -ForegroundColor Cyan
            Write-Host ""
        }
    }
}

# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================

function Main {
    # Inicializar log
    "===============================================================================" | Out-File -FilePath $LogFile
    "INICIO DE CONFIGURACIÓN POWERSHELL - $(Get-Date)" | Out-File -FilePath $LogFile -Append
    "===============================================================================" | Out-File -FilePath $LogFile -Append

    Write-Header "🚀 CONFIGURADOR MATRIZ DE ROL v3.0 - PowerShell"

    Write-Info "📂 Directorio del proyecto: $ProjectRoot"
    Write-Info "📋 Log de instalación: $LogFile"

    if (Test-Administrator) {
        Write-Warning "Ejecutándose como Administrador"
    }

    try {
        # 1. Buscar Python
        $pythonExe = Find-Python

        # 2. Verificar versión
        if (-not (Test-PythonVersion $pythonExe)) {
            throw "Versión de Python incompatible"
        }

        # 3. Crear entorno virtual
        if (-not (New-VirtualEnvironment $pythonExe)) {
            throw "Error configurando entorno virtual"
        }

        # 4. Instalar dependencias
        if (-not (Install-Dependencies)) {
            throw "Error instalando dependencias"
        }

        # 5. Verificar instalación
        if (-not (Test-Installation)) {
            throw "Error en verificación"
        }

        # 6. Crear scripts de acceso
        if (-not (New-AccessScripts)) {
            throw "Error creando scripts de acceso"
        }

        # 7. Configurar entorno
        if (-not (New-EnvironmentConfig)) {
            throw "Error configurando entorno"
        }

        # Obtener versión para el resumen
        $versionOutput = & $pythonExe --version 2>&1
        $pythonVersion = ($versionOutput | Select-String "Python (.+)").Matches[0].Groups[1].Value

        Show-Summary $pythonVersion $true

        Write-Log "Configuración completada exitosamente"

        if (-not $Quiet) {
            Write-Host "¿Deseas ejecutar la aplicación ahora? (s/n): " -NoNewline -ForegroundColor Yellow
            $response = Read-Host
            if ($response -eq "s" -or $response -eq "S") {
                Write-Info "🚀 Ejecutando aplicación..."
                Start-Process -FilePath (Join-Path $ProjectRoot "ejecutar_matriz_rol.bat")
            }
        }

        Write-Success "👋 ¡Configuración finalizada! La aplicación está lista para usar."
        return 0

    }
    catch {
        Write-Error "Error durante la configuración: $_"
        Write-Log "ERROR: $_" "ERROR"
        Show-Summary "" $false
        return 1
    }
}

# =============================================================================
# EJECUCIÓN
# =============================================================================

exit (Main)
