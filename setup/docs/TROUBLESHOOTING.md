# 🛠️ Solución de Problemas - Matriz de Rol

## 🎯 Guía Rápida de Diagnóstico

Esta guía te ayudará a resolver los problemas más comunes durante la instalación y uso de la aplicación Matriz de Rol.

## 🔍 Diagnóstico Automático

### Script de Verificación

**Antes de revisar esta guía, ejecuta el diagnóstico automático:**

```bash
python setup/scripts/verificar_sistema.py
```

Este script identificará automáticamente la mayoría de problemas comunes.

## 🚨 Problemas Comunes de Instalación

### ❌ Error: "Python no encontrado"

**Síntomas:**
- El instalador dice que Python no está disponible
- Comando `python --version` no funciona

**Soluciones:**

1. **Verificar instalación de Python:**
   ```bash
   # Probar diferentes comandos
   python --version
   python3 --version
   py --version
   ```

2. **Instalar Python correctamente:**
   - Descargar desde [python.org](https://python.org/downloads/)
   - **IMPORTANTE:** Marcar "Add Python to PATH" durante instalación
   - Reiniciar terminal después de instalar

3. **Agregar Python al PATH manualmente:**
   ```bash
   # Encontrar ubicación de Python
   where python

   # Si no está en PATH, agregar ubicación:
   # Windows: Panel de Control > Sistema > Variables de entorno
   # Agregar a PATH: C:\Python3x\ y C:\Python3x\Scripts\
   ```

4. **Usar Python desde Microsoft Store:**
   ```bash
   # Instalar desde Microsoft Store si otras opciones fallan
   # Buscar "Python" en Microsoft Store
   ```

### ❌ Error: "Versión de Python incompatible"

**Síntomas:**
- Python está instalado pero es muy antiguo
- Error: "Se requiere Python 3.9+"

**Soluciones:**

1. **Actualizar Python:**
   ```bash
   # Verificar versión actual
   python --version

   # Descargar versión nueva desde python.org
   # Instalar Python 3.9, 3.10, 3.11 o 3.12
   ```

2. **Usar múltiples versiones:**
   ```bash
   # Si tienes varias versiones instaladas
   py -3.9 --version
   py -3.10 --version

   # Usar launcher de Python específico
   py -3.11 setup/scripts/verificar_sistema.py
   ```

### ❌ Error: "No se puede crear entorno virtual"

**Síntomas:**
- Error durante creación de venv
- "No module named venv"

**Soluciones:**

1. **Verificar módulo venv:**
   ```bash
   python -m venv --help
   ```

2. **Instalar venv (Ubuntu/Debian):**
   ```bash
   # Si estás en WSL o Linux
   sudo apt install python3-venv
   ```

3. **Usar virtualenv alternativo:**
   ```bash
   pip install virtualenv
   virtualenv venv
   ```

4. **Verificar permisos:**
   ```bash
   # Verificar permisos de escritura
   echo test > test_permissions.txt
   del test_permissions.txt
   ```

### ❌ Error: "pip no funciona"

**Síntomas:**
- "pip is not recognized"
- Errores durante instalación de dependencias

**Soluciones:**

1. **Usar pip como módulo:**
   ```bash
   python -m pip --version
   python -m pip install --upgrade pip
   ```

2. **Reinstalar pip:**
   ```bash
   # Descargar get-pip.py
   python get-pip.py
   ```

3. **Verificar ubicación de pip:**
   ```bash
   where pip
   # Debería estar en Python3x\Scripts\pip.exe
   ```

### ❌ Error: "Espacio insuficiente en disco"

**Síntomas:**
- Error de espacio durante instalación
- No se pueden crear archivos

**Soluciones:**

1. **Liberar espacio:**
   - Eliminar archivos temporales
   - Limpiar papelera de reciclaje
   - Usar Disk Cleanup de Windows

2. **Cambiar ubicación:**
   ```bash
   # Mover proyecto a disco con más espacio
   # Ejecutar instalador desde nueva ubicación
   ```

### ❌ Error: "Permisos insuficientes"

**Síntomas:**
- "Access denied" durante instalación
- No se pueden crear archivos/carpetas

**Soluciones:**

1. **Ejecutar como administrador:**
   - Clic derecho en script → "Ejecutar como administrador"

2. **Cambiar permisos de carpeta:**
   - Clic derecho en carpeta del proyecto
   - Propiedades → Seguridad → Editar
   - Dar control total al usuario actual

3. **Usar ubicación diferente:**
   ```bash
   # Mover proyecto a carpeta del usuario
   C:\Users\[TuUsuario]\Documents\matriz-rol\
   ```

## 🚨 Problemas Durante la Ejecución

### ❌ Error: "No se puede importar módulo principal"

**Síntomas:**
- Error al ejecutar aplicación
- "ModuleNotFoundError"

**Soluciones:**

1. **Verificar entorno virtual:**
   ```bash
   # Activar entorno
   venv\Scripts\activate

   # Verificar instalación
   pip list | findstr matriz
   ```

2. **Reinstalar en modo desarrollo:**
   ```bash
   venv\Scripts\activate
   pip install -e .
   ```

3. **Verificar estructura del proyecto:**
   ```bash
   # Debe existir:
   src\matriz_rol\__init__.py
   src\matriz_rol\gui\aplicacion_principal.py
   ```

### ❌ Error: "tkinter no disponible"

**Síntomas:**
- Error: "No module named tkinter"
- Interfaz gráfica no se abre

**Soluciones:**

1. **Verificar tkinter:**
   ```bash
   python -c "import tkinter; print('tkinter OK')"
   ```

2. **Instalar tkinter (Linux/WSL):**
   ```bash
   sudo apt install python3-tk
   ```

3. **Usar Python completo:**
   - En Windows, tkinter viene incluido
   - Verificar que Python no sea versión "embebida"

### ❌ Error: "Aplicación se cierra inmediatamente"

**Síntomas:**
- Ventana aparece y desaparece rápidamente
- No hay interfaz visible

**Soluciones:**

1. **Ejecutar desde línea de comandos:**
   ```bash
   # Ver errores completos
   venv\Scripts\python -c "from src.matriz_rol.gui.aplicacion_principal import AplicacionMatrizRol; app = AplicacionMatrizRol(); app.mainloop()"
   ```

2. **Verificar logs:**
   ```bash
   # Revisar logs de error
   type setup\logs\setup.log
   ```

3. **Modo debug:**
   ```bash
   # Activar entorno y ejecutar con más información
   activar_entorno_dev.bat
   python -u -c "from src.matriz_rol.gui.aplicacion_principal import AplicacionMatrizRol; app = AplicacionMatrizRol(); app.mainloop()"
   ```

## 🚨 Problemas Específicos de Windows

### ❌ Error: "Execution Policy" (PowerShell)

**Síntomas:**
- No se puede ejecutar script .ps1
- Error de política de ejecución

**Soluciones:**

```powershell
# Cambiar política temporalmente
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# O ejecutar bypass
powershell -ExecutionPolicy Bypass -File setup\scripts\configurar_ambiente.ps1
```

### ❌ Error: "PATH muy largo"

**Síntomas:**
- Error sobre longitud de PATH
- Comandos no se encuentran

**Soluciones:**

1. **Limpiar PATH:**
   - Panel de Control → Sistema → Variables de entorno
   - Eliminar entradas duplicadas o innecesarias

2. **Usar rutas cortas:**
   ```bash
   # Mover proyecto a ubicación con ruta más corta
   C:\matriz\
   ```

### ❌ Error: "Antivirus bloquea instalación"

**Síntomas:**
- Archivos desaparecen después de crearse
- Instalación se interrumpe

**Soluciones:**

1. **Agregar excepción:**
   - Configurar antivirus para excluir carpeta del proyecto
   - Temporalmente deshabilitar protección en tiempo real

2. **Usar Windows Defender únicamente:**
   - Desinstalar antivirus de terceros temporalmente

## 🚨 Problemas de Red y Conectividad

### ❌ Error: "No se pueden descargar paquetes"

**Síntomas:**
- pip timeout
- "No connection to PyPI"

**Soluciones:**

1. **Verificar conectividad:**
   ```bash
   ping pypi.org
   ```

2. **Usar mirror alternativo:**
   ```bash
   pip install -i https://pypi.python.org/simple/ -e .
   ```

3. **Configurar proxy (si aplica):**
   ```bash
   pip install --proxy http://proxy.company.com:8080 -e .
   ```

4. **Instalación offline:**
   ```bash
   # Descargar paquetes en PC con internet
   pip download -r requirements.txt -d packages/

   # Instalar offline
   pip install --find-links packages/ -r requirements.txt
   ```

## 🔧 Herramientas de Diagnóstico

### Script de Información del Sistema

```bash
# Crear archivo de diagnóstico completo
echo "=== INFORMACIÓN DEL SISTEMA ===" > diagnostico.txt
systeminfo >> diagnostico.txt
echo "=== VERSIÓN DE PYTHON ===" >> diagnostico.txt
python --version >> diagnostico.txt 2>&1
echo "=== VARIABLES DE ENTORNO ===" >> diagnostico.txt
set | findstr PYTHON >> diagnostico.txt
echo "=== CONTENIDO DE PATH ===" >> diagnostico.txt
echo %PATH% >> diagnostico.txt
```

### Verificación Manual Paso a Paso

```bash
# 1. Verificar Python
python --version

# 2. Verificar pip
python -m pip --version

# 3. Verificar venv
python -m venv test_env
rmdir /s test_env

# 4. Verificar permisos
echo test > test.txt & del test.txt

# 5. Verificar espacio
dir

# 6. Verificar estructura
dir src\matriz_rol\gui\
```

## 📞 Obtener Ayuda Adicional

### Información Necesaria para Reportar Problemas

Cuando solicites ayuda, incluye:

1. **Sistema operativo:** `winver`
2. **Versión de Python:** `python --version`
3. **Contenido de logs:** `setup/logs/`
4. **Resultado de verificación:** `python setup/scripts/verificar_sistema.py`
5. **Error exacto:** Copia completa del mensaje de error

### Generar Reporte Automático

```bash
# Ejecutar diagnóstico completo
python setup/scripts/verificar_sistema.py > reporte_completo.txt 2>&1

# El reporte se guarda automáticamente en:
# setup/logs/reporte_verificacion.txt
```

## 🔄 Soluciones de Último Recurso

### Reinstalación Completa

```bash
# 1. Eliminar entorno virtual
rmdir /s venv

# 2. Limpiar archivos temporales
del *.pyc /s
del __pycache__ /s

# 3. Reinstalar desde cero
setup\scripts\configurar_ambiente.bat
```

### Reset Total del Proyecto

```bash
# 1. Mantener solo código fuente
# 2. Eliminar: venv/, .env, setup/logs/
# 3. Re-ejecutar instalación rápida
setup\scripts\instalador_rapido.bat
```

## 📋 Lista de Verificación Rápida

- [ ] Python 3.9+ instalado y en PATH
- [ ] pip funciona correctamente
- [ ] Permisos de escritura en directorio
- [ ] Espacio suficiente en disco (500+ MB)
- [ ] Estructura completa del proyecto
- [ ] No hay conflictos de antivirus
- [ ] Conexión a internet (para descarga inicial)

---

## 🎯 Próximos Pasos

Si ninguna solución funciona:

1. **Ejecutar verificación completa:** `python setup/scripts/verificar_sistema.py`
2. **Revisar logs detallados** en `setup/logs/`
3. **Probar instalación en PC diferente** para descartar problemas de hardware
4. **Reportar problema** con información completa del sistema

---

*Si resolviste tu problema, considera contribuir a esta documentación agregando tu solución.*
