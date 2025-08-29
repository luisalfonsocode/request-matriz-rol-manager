# 📋 Guía Completa de Instalación - Matriz de Rol

## 🎯 Descripción General

Esta guía te ayudará a instalar y configurar la aplicación **Matriz de Rol** en tu sistema Windows. El proyecto incluye un sistema de instalación automática que detecta tu configuración y configura todo lo necesario.

## 📁 Estructura del Sistema de Instalación

```
setup/
├── scripts/                    # Scripts de instalación
│   ├── configurar_ambiente.bat    # Instalador completo (Batch)
│   ├── configurar_ambiente.ps1    # Instalador avanzado (PowerShell)
│   ├── instalador_rapido.bat      # Instalador simplificado
│   └── verificar_sistema.py       # Verificación del sistema
├── docs/                       # Documentación
│   ├── INSTALACION.md            # Esta guía
│   ├── TROUBLESHOOTING.md        # Solución de problemas
│   └── CONFIGURACION.md          # Configuración avanzada
└── logs/                       # Logs de instalación
    ├── setup.log                 # Log del instalador batch
    ├── setup_powershell.log      # Log del instalador PowerShell
    └── verificacion.log          # Log de verificación
```

## 🚀 Métodos de Instalación

### Método 1: Instalación Rápida (Recomendado para usuarios)

**Ideal para:** Usuarios que quieren la instalación más simple

```bash
# Ejecutar con doble clic:
setup/scripts/instalador_rapido.bat
```

**Características:**
- ✅ Instalación con un solo clic
- ✅ Verificación automática del sistema
- ✅ Configuración completa automática
- ✅ Creación de accesos directos

### Método 2: Instalación Completa (Batch)

**Ideal para:** Usuarios con experiencia básica en sistemas

```bash
# Ejecutar con doble clic:
setup/scripts/configurar_ambiente.bat
```

**Características:**
- ✅ Control completo del proceso
- ✅ Logs detallados de instalación
- ✅ Verificación paso a paso
- ✅ Manejo de errores avanzado

### Método 3: Instalación Avanzada (PowerShell)

**Ideal para:** Desarrolladores y usuarios técnicos

```powershell
# Desde PowerShell:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup\scripts\configurar_ambiente.ps1

# Con opciones avanzadas:
.\setup\scripts\configurar_ambiente.ps1 -Force -DevMode
```

**Opciones disponibles:**
- `-Force`: Fuerza recreación del entorno virtual
- `-DevMode`: Instala dependencias de desarrollo
- `-SkipTests`: Omite pruebas de verificación
- `-Quiet`: Modo silencioso

### Método 4: Verificación Previa

**Ideal para:** Diagnóstico de problemas

```bash
# Desde línea de comandos:
python setup/scripts/verificar_sistema.py
```

## 📋 Requisitos del Sistema

### Requisitos Mínimos

| Componente            | Requisito        | Verificación       |
| --------------------- | ---------------- | ------------------ |
| **Sistema Operativo** | Windows 10/11    | `winver`           |
| **Python**            | 3.9 o superior   | `python --version` |
| **Espacio en Disco**  | 500 MB libres    | Automático         |
| **RAM**               | 4 GB mínimo      | Recomendado        |
| **Permisos**          | Usuario estándar | Automático         |

### Dependencias Automáticas

El instalador configura automáticamente:
- ✅ Entorno virtual de Python
- ✅ Todas las dependencias del proyecto
- ✅ Configuración de GUI (tkinter)
- ✅ Herramientas de desarrollo (opcional)

## 🔧 Instalación Paso a Paso

### Preparación

1. **Descargar el proyecto:**
   ```bash
   git clone <url-del-repositorio>
   cd utilitarios-matriz-de-rol
   ```

2. **Verificar Python:**
   ```bash
   python --version
   # Debe mostrar: Python 3.9.x o superior
   ```

### Ejecución

1. **Elegir método de instalación:**
   - Para usuarios: `setup/scripts/instalador_rapido.bat`
   - Para técnicos: `setup/scripts/configurar_ambiente.bat`
   - Para desarrolladores: `setup/scripts/configurar_ambiente.ps1`

2. **Seguir las instrucciones en pantalla:**
   - El instalador te guiará paso a paso
   - Lee los mensajes y confirma cuando se solicite
   - Espera a que termine completamente

3. **Verificar instalación:**
   - Al final aparecerá un resumen de éxito
   - Se crearán archivos de acceso directo
   - La aplicación estará lista para usar

### Post-Instalación

Después de la instalación exitosa encontrarás:

```
📁 Proyecto/
├── ejecutar_matriz_rol.bat      # 🚀 Ejecutar aplicación
├── activar_entorno_dev.bat      # 🔧 Modo desarrollo
├── reinstalar.bat               # 🔄 Reinstalar rápidamente
├── .env                         # ⚙️ Configuración del entorno
└── venv/                        # 📦 Entorno virtual Python
```

## 🚀 Uso de la Aplicación

### Ejecución Normal

```bash
# Método 1: Doble clic
ejecutar_matriz_rol.bat

# Método 2: Desde línea de comandos
.\ejecutar_matriz_rol.bat
```

### Modo Desarrollo

```bash
# Activar entorno de desarrollo
.\activar_entorno_dev.bat

# Ejecutar desde código fuente
python -c "from src.matriz_rol.gui.aplicacion_principal import AplicacionMatrizRol; app = AplicacionMatrizRol(); app.mainloop()"
```

### Reinstalación

```bash
# Reinstalar completamente
.\reinstalar.bat

# O usar PowerShell con opciones
.\setup\scripts\configurar_ambiente.ps1 -Force
```

## 🔍 Verificación de la Instalación

### Verificación Básica

1. **Comprobar entorno virtual:**
   ```bash
   venv\Scripts\python.exe --version
   ```

2. **Verificar módulos principales:**
   ```bash
   venv\Scripts\python.exe -c "from src.matriz_rol.gui.aplicacion_principal import AplicacionMatrizRol; print('OK')"
   ```

3. **Ejecutar aplicación:**
   ```bash
   .\ejecutar_matriz_rol.bat
   ```

### Verificación Avanzada

```bash
# Ejecutar script de verificación completa
python setup/scripts/verificar_sistema.py
```

## 📊 Logs y Diagnóstico

### Ubicación de Logs

- **Instalación Batch:** `setup/logs/setup.log`
- **Instalación PowerShell:** `setup/logs/setup_powershell.log`
- **Verificación:** `setup/logs/verificacion.log`
- **Configuración:** `.env`

### Información de Logs

Los logs contienen:
- ✅ Pasos de instalación ejecutados
- ✅ Errores encontrados y soluciones
- ✅ Configuración del entorno
- ✅ Versiones de software detectadas

## 🌐 Portabilidad

### Uso en Diferentes PCs

La instalación es totalmente portable:

1. **Copiar proyecto completo** a otro PC
2. **Ejecutar** `setup/scripts/instalador_rapido.bat`
3. **Listo** - funciona automáticamente

### Requisitos para Portabilidad

- ✅ Windows 10/11
- ✅ Python 3.9+ instalado
- ✅ Permisos de usuario estándar

## 🛠️ Personalización

### Variables de Entorno

El archivo `.env` contiene la configuración:

```bash
PROJECT_ROOT=F:\ws\utilitarios-matriz-de-rol
VENV_DIR=F:\ws\utilitarios-matriz-de-rol\venv
PYTHON_EXE=F:\ws\utilitarios-matriz-de-rol\venv\Scripts\python.exe
PYTHON_VERSION=3.11.5
SETUP_DATE=2024-01-XX XX:XX:XX
```

### Configuración Avanzada

Ver: [CONFIGURACION.md](CONFIGURACION.md) para opciones avanzadas.

## 📞 Soporte

### Problemas Comunes

Ver: [TROUBLESHOOTING.md](TROUBLESHOOTING.md) para soluciones detalladas.

### Reportar Problemas

1. **Ejecutar verificación:** `python setup/scripts/verificar_sistema.py`
2. **Revisar logs** en `setup/logs/`
3. **Incluir información** del sistema y logs al reportar

## 📈 Actualizaciones

### Actualizar Instalación

```bash
# Método 1: Reinstalación completa
.\reinstalar.bat

# Método 2: Actualización de dependencias
.\activar_entorno_dev.bat
pip install -e . --upgrade
```

### Mantener Entorno

```bash
# Verificar estado regularmente
python setup/scripts/verificar_sistema.py

# Actualizar dependencias cuando sea necesario
.\activar_entorno_dev.bat
pip install --upgrade -r requirements.txt
```

---

## 🎉 ¡Felicidades!

Si llegaste hasta aquí, tu aplicación **Matriz de Rol** debería estar funcionando perfectamente.

### Próximos Pasos

1. **Ejecutar la aplicación:** `ejecutar_matriz_rol.bat`
2. **Explorar funcionalidades** de la interfaz gráfica
3. **Consultar documentación** adicional en `docs/`

### Recursos Adicionales

- 📋 [Guía de Usuario](../docs/USUARIO.md)
- 🔧 [Guía de Desarrollo](../docs/DESARROLLO.md)
- 🐛 [Solución de Problemas](TROUBLESHOOTING.md)

---

*Documentación generada automáticamente por el Sistema de Configuración v3.0*
