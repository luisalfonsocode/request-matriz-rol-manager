# 🎯 Utilitarios Matriz de Rol

**Sistema avanzado de gestión de matrices de roles empresariales con interfaz gráfica moderna e instalación automatizada**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://microsoft.com/windows)
[![Setup](https://img.shields.io/badge/Setup-Automated-brightgreen.svg)](#instalación-rápida)

## 🚀 Instalación Rápida

### Método 1: Un Solo Clic (Recomendado)
```bash
# Ejecutar con doble clic:
INSTALAR.bat
```

### Método 2: Instalación Directa
```bash
# Instalación rápida
setup\scripts\instalador_rapido.bat

# Instalación completa
setup\scripts\configurar_ambiente.bat

# Instalación avanzada (PowerShell)
setup\scripts\configurar_ambiente.ps1 -DevMode
```

## 📋 Requisitos del Sistema

| Componente  | Requisito      |
| ----------- | -------------- |
| **SO**      | Windows 10/11  |
| **Python**  | 3.9 o superior |
| **Espacio** | 500 MB libres  |
| **RAM**     | 4 GB mínimo    |

## 🎯 Características Principales

✅ **Interfaz Gráfica Moderna** - Desarrollada con tkinter
✅ **Instalación Automatizada** - Sistema de setup inteligente
✅ **Gestión de Roles** - Matrices de permisos empresariales
✅ **Gestión de Solicitudes** - Crear y hacer seguimiento de solicitudes de conformidad
✅ **Base de Datos de Autorizadores** - Gestión centralizada de autorizadores por código
✅ **Generación de Correos** - Archivos MSG individuales para cada autorizador
✅ **Estados de Workflow** - Seguimiento completo del ciclo de vida
✅ **Edición en Grilla** - Modificación directa de estados y observaciones
✅ **Dashboard de Gestión** - Estadísticas y filtros en tiempo real
✅ **Validación de Datos** - Verificación automática de integridad
✅ **Sistema de Logs** - Seguimiento detallado de operaciones
✅ **Portabilidad Total** - Funciona en cualquier PC Windows

## 🔧 Uso de la Aplicación

### Ejecutar Aplicación
```bash
# Después de la instalación:
ejecutar_matriz_rol.bat
```

### Modo Desarrollo
```bash
# Para desarrolladores:
activar_entorno_dev.bat
```

### Reinstalar
```bash
# Si hay problemas:
reinstalar.bat
```

## 📚 Documentación Completa

| Documento                                                        | Descripción                  |
| ---------------------------------------------------------------- | ---------------------------- |
| [`setup/docs/INSTALACION.md`](setup/docs/INSTALACION.md)         | Guía completa de instalación |
| [`setup/docs/TROUBLESHOOTING.md`](setup/docs/TROUBLESHOOTING.md) | Solución de problemas        |
| [`setup/docs/CONFIGURACION.md`](setup/docs/CONFIGURACION.md)     | Configuración avanzada       |

## 🏗️ Estructura del Proyecto

```
utilitarios-matriz-de-rol/
├── 🚀 INSTALAR.bat                    # Instalador maestro
├── 📱 ejecutar_matriz_rol.bat         # Ejecutar aplicación
├── 🔧 activar_entorno_dev.bat         # Modo desarrollo
├── 🔄 reinstalar.bat                  # Reinstalación rápida
├── src/                               # Código fuente
│   └── matriz_rol/                    # Paquete principal
├── setup/                             # Sistema de instalación
│   ├── scripts/                       # Scripts de instalación
│   ├── docs/                          # Documentación
│   └── logs/                          # Logs de instalación
├── tests/                             # Pruebas automatizadas
└── docs/                              # Documentación del proyecto
```

## 🎮 Inicio Rápido

### Ejecutar la aplicación:
```bash
# Método 1: Desde módulo principal
python -m matriz_rol.gui.aplicacion_principal

# Método 2: Script directo
python src/matriz_rol/gui/aplicacion_principal.py

# Método 3: Si está instalado el paquete
matriz-rol
```

### Inicializar por primera vez:
```bash
python scripts/inicializar_bd_autorizadores.py
```

## 📁 Estructura del Proyecto

```
📦 utilitarios-matriz-de-rol/
├── 🚀 INSTALAR.bat                 # INSTALADOR PRINCIPAL (un clic)
├── 📄 setup.py                     # Configuración del paquete Python
├── 📄 README.md                    # Documentación principal
├── � LICENSE                      # Licencia MIT
│
├── �📁 src/matriz_rol/              # 🎯 CÓDIGO PRINCIPAL
│   ├── data/                       # 📊 Gestión de datos (3 módulos)
│   ├── email/                      # 📧 Generación correos (2 módulos)
│   └── gui/                        # 🖥️ Interfaz gráfica (4 módulos)
│
├── 📁 setup/                       # 🛠️ Sistema de instalación automatizada
│   ├── scripts/                    # Scripts de configuración
│   ├── docs/                       # Documentación de instalación
│   └── logs/                       # Logs del sistema
│
├── 📁 config/                      # ⚙️ Configuraciones del proyecto
│   ├── matrices.yaml               # Matrices de rol disponibles
│   └── tools/                      # Configuraciones de herramientas
│
├── 📁 requirements/                # 📦 Dependencias por ambiente
│   ├── base.txt                    # Dependencias principales
│   ├── dev.txt                     # Herramientas de desarrollo
│   └── test.txt                    # Dependencias de testing
│
├── 📁 scripts/                     # 🔧 Scripts de utilidad
│   ├── inicializar_bd_autorizadores.py
│   └── otros scripts...
│
├── 📁 data/                        # 💾 Base de datos JSON local
├── 📁 output/                      # 📤 Correos generados
├── 📁 tests/                       # 🧪 Suite de pruebas
└── 📁 docs/                        # 📚 Documentación completa
```

## 📚 Documentación

- 📖 **[Documentación Completa](docs/README.md)** - Guías de usuario y desarrollador
- 🔧 **[Instalación Detallada](docs/INSTALACION.md)** - Configuración paso a paso
- 💻 **[Documentación del Código](docs/CODIGO_FINAL.md)** - Arquitectura técnica

## 🛠️ Instalación

### ⚡ Instalación Rápida (Un Clic)
```bash
# Ejecutar instalador principal
INSTALAR.bat
```

### 📋 Requisitos
- Python 3.9+
- Windows 10/11 (para generación de archivos MSG)
- Microsoft Outlook instalado

### 🔧 Instalación Manual
```bash
# 1. Clonar proyecto
git clone <url-del-repositorio>
cd utilitarios-matriz-de-rol

# 2. Ejecutar instalación automatizada
setup\scripts\instalador_rapido.bat

# 3. Inicializar base de datos
python scripts/inicializar_bd_autorizadores.py

# 4. Ejecutar aplicación
python -m matriz_rol.gui.aplicacion_principal
```

### 🎛️ Instalación para Desarrolladores
```bash
# Instalación completa con herramientas de desarrollo
setup\scripts\configurar_ambiente.bat

# O con PowerShell (más opciones)
setup\scripts\configurar_ambiente.ps1 -DevMode -CreateVenv
```

## 🎯 Funcionalidades

### 📝 **Nueva Solicitud**
- Selección de matrices de rol desde configuración
- Editor integrado de autorizadores
- Generación automática de correos MSG personalizados
- Validación de grupos de red

### 📊 **Gestión de Solicitudes**
- Lista completa con filtros dinámicos
- **Edición en grilla**: Doble-click para editar Estado, Ticket, Observaciones
- Vista de detalles con componentes visuales
- Estadísticas en tiempo real por estado

### 🔄 **Estados de Workflow**
```
EN_SOLICITUD_CONFORMIDADES → EN_HELPDESK → ATENDIDO → CERRADO
```

### 👥 **Base de Datos Centralizada**
- Autorizadores por código de aplicación
- Sincronización automática entre componentes
- Backup diario automático

## 🛠️ Scripts Útiles

```bash
# Generar datos de prueba
python scripts/generar_datos_ficticios.py

# Cargar datos específicos
python scripts/llenar_datos_completos.py
```

## �️ Para Desarrolladores

### Configuración del Entorno
```bash
# Instalar en modo desarrollo
setup\scripts\configurar_ambiente.ps1 -DevMode

# Activar entorno
activar_entorno_dev.bat

# Ejecutar tests
python -m pytest tests/

# Formatear código
black src/ tests/
```

### Herramientas Incluidas
- **Black** - Formateador de código
- **isort** - Organizador de importaciones
- **Flake8** - Linter de código
- **mypy** - Verificador de tipos
- **pytest** - Framework de testing

### Estructura del Proyecto (Detallada)
```
utilitarios-matriz-de-rol/
├── src/                    # Código fuente
│   └── matriz_rol/        # Paquete principal
├── setup/                 # Sistema de instalación
│   ├── scripts/           # Scripts de instalación
│   ├── docs/              # Documentación de instalación
│   └── logs/              # Logs de instalación
├── tests/                 # Tests automatizados
├── docs/                  # Documentación del proyecto
├── requirements/          # Archivos de dependencias
└── scripts/              # Scripts de utilidad
```

## 🔍 Verificación del Sistema

```bash
# Diagnóstico completo
python setup\scripts\verificar_sistema.py

# Verificación rápida
setup\scripts\verificar_sistema.py
```

## 📊 Logs y Diagnóstico

Ubicación de logs después de la instalación:
```
setup/logs/
├── setup.log                 # Log instalación batch
├── setup_powershell.log      # Log instalación PowerShell
├── verificacion.log          # Log verificación sistema
└── reporte_verificacion.txt  # Reporte detallado
```

## 🌐 Compatibilidad y Portabilidad

### Sistemas Soportados
- ✅ Windows 10 (todas las versiones)
- ✅ Windows 11 (todas las versiones)
- ✅ Windows Server 2019/2022

### Portabilidad
1. **Copiar proyecto** a nuevo PC
2. **Ejecutar** `INSTALAR.bat`
3. **¡Listo!** - Funciona automáticamente

## 🆘 Soporte y Ayuda

### Problemas Comunes
1. **Python no encontrado** → Instalar desde [python.org](https://python.org)
2. **Permisos insuficientes** → Ejecutar como administrador
3. **Errores de red** → Verificar conectividad a PyPI

### Obtener Ayuda
1. Consultar [`TROUBLESHOOTING.md`](setup/docs/TROUBLESHOOTING.md)
2. Ejecutar diagnóstico: `python setup\scripts\verificar_sistema.py`
3. Revisar logs en `setup\logs\`

## 📈 Actualizaciones

```bash
# Reinstalar completamente
reinstalar.bat

# Actualizar dependencias
activar_entorno_dev.bat
pip install --upgrade -r requirements.txt
```

## 📝 Notas de Versión

### v3.0 (Actual)
- ✅ Sistema de instalación completamente refactorizado
- ✅ Documentación exhaustiva en markdown
- ✅ Scripts organizados en estructura profesional
- ✅ Instalador maestro con múltiples opciones
- ✅ Verificación automática del sistema
- ✅ Soporte completo para PowerShell
- ✅ Logs detallados y diagnóstico

### v2.x (Anterior)
- Sistema de instalación básico
- Scripts en directorio raíz
- Documentación limitada

---

## �📄 Archivos Generados (Funcionalidad Original)

### 📧 Correos Individuales
```
output/correos_individuales/Solicitud_YYYYMMDD_HHMM_*/
├── 01_Conformidad_CODIGO_Nombre_FECHA.msg
├── 02_Conformidad_CODIGO_Nombre_FECHA.msg
└── RESUMEN_SOLICITUD.txt
```

### 💾 Base de Datos
```
data/
├── autorizadores_bd.json           # BD central autorizadores
├── solicitudes_conformidad.json    # Solicitudes activas
└── backup_solicitudes_*.json       # Backups automáticos
```

## 🔧 Para Desarrolladores

### 📚 **Documentación Técnica**
- [Guía PEP 8](docs/PEP8_GUIDE.md) - Estándares de código
- [Type Hints](docs/TYPE_HINTS.md) - Anotaciones de tipos
- [Docstrings](docs/DOCSTRINGS_GUIDE.md) - Documentación de funciones
- [Configuración VS Code](docs/VSCODE_CONFIG.md) - Entorno de desarrollo

### 🏗️ **Arquitectura**
- **Patrón MVC**: Separación clara entre datos, lógica y vista
- **Sistema de eventos**: Callbacks entre componentes
- **Persistencia JSON**: Base de datos local simple
- **Configuración externa**: YAML para flexibilidad

## 📊 Estado del Proyecto

✅ **Completamente funcional y documentado**
- 🧹 Código limpio y organizado
- 📚 Documentación exhaustiva
- 🔧 Solo código activo en producción
- 🛠️ Scripts de utilidad organizados
- 📁 Estructura clara y mantenible

## 📞 Soporte

1. 📖 Consulta la [documentación completa](docs/README.md)
2. 🔍 Revisa los logs de la aplicación
3. 🛠️ Verifica la configuración en `config/matrices.yaml`

---

**📅 Última actualización**: 23 de agosto de 2025
**📊 Estado**: Proyecto limpio y completamente documentado
**🎯 Versión**: 1.0.0
   - Python
   - Pylance
   - autoDocstring

2. Configurar el entorno:
   - Ver [Configuración de VS Code](docs/VSCODE_CONFIG.md) para la configuración del editor
   - Ver [Herramientas de Desarrollo](docs/DEVELOPMENT_TOOLS.md) para detalles de las herramientas
   - Aplicar la configuración recomendada del workspace

## Desarrollo (Documentación Original)

### Configuración Recomendada de VS Code

1. Instalar extensiones requeridas:
   - Python
   - Pylance
   - autoDocstring

2. Configurar el entorno:
   - Ver [Configuración de VS Code](docs/VSCODE_CONFIG.md) para la configuración del editor
   - Ver [Herramientas de Desarrollo](docs/DEVELOPMENT_TOOLS.md) para detalles de las herramientas
   - Aplicar la configuración recomendada del workspace

### Documentación Adicional

- [Guía de Estilo PEP 8](docs/PEP8_GUIDE.md)
- [Guía de Type Hints](docs/TYPE_HINTS.md)
- [Guía de Docstrings](docs/DOCSTRINGS_GUIDE.md)
- [Herramientas de Desarrollo](docs/DEVELOPMENT_TOOLS.md)

### Testing
```bash
pytest              # Ejecutar tests
pytest --cov=src    # Tests con cobertura
```

### Control de Calidad

Usar pre-commit para verificaciones automáticas:
```bash
pre-commit install    # Instalar hooks
pre-commit run -a     # Verificar todos los archivos
```

Ver [Herramientas de Desarrollo](docs/DEVELOPMENT_TOOLS.md) para más detalles sobre:
- Formateo de código (black, isort)
- Linting (flake8, pylint, ruff)
- Verificación de tipos (mypy)
- Testing (pytest)
- Documentación (sphinx, mkdocs)

## Uso (API Original)

```python
from matriz_rol import MatrizRoles

# Crear una matriz de roles
matriz = MatrizRoles()

# Agregar roles y permisos
matriz.agregar_rol("admin", ["leer", "escribir", "eliminar"])
matriz.agregar_rol("editor", ["leer", "escribir"])
matriz.agregar_rol("viewer", ["leer"])

# Verificar permisos
tiene_permiso = matriz.verificar_permiso("editor", "escribir")  # True
```

## 🎉 Conclusión

### ¡Primera vez usando la aplicación?

1. **Descargar/Clonar** el proyecto
2. **Ejecutar** `INSTALAR.bat`
3. **Seguir** las instrucciones en pantalla
4. **Ejecutar** `ejecutar_matriz_rol.bat`
5. **¡Disfrutar!** de la aplicación

### Sistema de Instalación v3.0

El nuevo sistema de instalación incluye:
- ✅ **Instalador maestro** con múltiples opciones
- ✅ **Verificación automática** del sistema
- ✅ **Documentación completa** en markdown
- ✅ **Soporte para PowerShell** con parámetros avanzados
- ✅ **Logs detallados** para diagnóstico
- ✅ **Portabilidad total** entre PCs Windows

---

*¿Problemas durante la instalación? Consulta [`setup/docs/TROUBLESHOOTING.md`](setup/docs/TROUBLESHOOTING.md) para soluciones detalladas.*

## Contribuir

1. Fork el repositorio
2. Crear una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit los cambios (`git commit -am 'feat: agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## Autor

Luis Alfonso - [luisalfonsocode](https://github.com/luisalfonsocode)
