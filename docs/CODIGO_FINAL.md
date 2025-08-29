# 📚 DOCUMENTACIÓN DEL CÓDIGO FINAL

## 🎯 Resumen del Proyecto

**Utilitarios Matriz de Rol** es una aplicación de escritorio desarrollada en Python para gestionar solicitudes de conformidad de roles en sistemas empresariales. Permite crear solicitudes, gestionar autorizadores y hacer seguimiento del estado de las solicitudes.

## 📁 Estructura del Proyecto Final

### 🚀 **Instalación y Configuración**

```
📦 Raíz del Proyecto
├── INSTALAR.bat                # 🎯 Instalador principal (punto de entrada)
├── setup.py                    # 📦 Configuración del paquete Python
├── README.md                   # 📖 Documentación principal
├── LICENSE                     # ⚖️ Licencia MIT
│
├── setup/                      # 🛠️ Sistema de instalación automatizada
│   ├── scripts/                # Scripts de configuración
│   │   ├── instalador_rapido.bat
│   │   ├── configurar_ambiente.bat
│   │   ├── configurar_ambiente.ps1
│   │   └── verificar_sistema.py
│   ├── docs/                   # Documentación de instalación
│   └── logs/                   # Logs del sistema
│
├── config/                     # ⚙️ Configuraciones del proyecto
│   ├── matrices.yaml           # Matrices de rol disponibles
│   └── tools/                  # Configuraciones de herramientas
│       ├── pyproject.toml      # Black, isort, build
│       ├── setup.cfg          # flake8, coverage
│       └── mypy.ini           # Verificación de tipos
│
└── requirements/               # 📦 Dependencias por ambiente
    ├── base.txt               # Dependencias principales
    ├── dev.txt                # Herramientas de desarrollo
    └── test.txt               # Dependencias de testing
```

### 🔧 **Código Principal (`src/matriz_rol/`)**

```
src/matriz_rol/
├── __init__.py                 # Módulo principal
├── data/                       # 📊 Gestión de datos
│   ├── __init__.py
│   ├── gestor_autorizadores.py # 👥 BD central de autorizadores
│   ├── gestor_solicitudes.py   # 📋 Gestión de solicitudes
│   └── persistencia.py         # 💾 Persistencia de datos
├── email/                      # 📧 Generación de correos
│   ├── __init__.py
│   ├── generador_correos.py    # 📧 Correos masivos
│   └── generador_correos_individuales.py # 📧 Correos personalizados
└── gui/                        # 🖥️ Interfaz gráfica
    ├── __init__.py
    ├── aplicacion_principal.py # 🎮 Aplicación principal
    ├── autorizadores_editor.py # ✏️ Editor de autorizadores
    ├── gestion_solicitudes.py  # 📊 Gestión de solicitudes
    └── solicitud_matriz.py     # 📝 Creación de solicitudes
```

### � **Scripts Utilitarios (`scripts/`)**

```
scripts/
├── inicializar_bd_autorizadores.py  # 🏗️ Inicialización de BD (movido desde raíz)
├── generar_datos_ficticios.py       # 🎭 Genera datos de prueba
├── llenar_datos_completos.py        # 📝 Inicializa datos específicos
├── mostrar_bd.py                    # 👁️ Visualiza BD de autorizadores
└── migrar_bd.py                     # 🔄 Migración de datos
```

## 🔍 Descripción Detallada de Módulos

### 📊 **data/gestor_autorizadores.py**
**Propósito**: Gestión centralizada de la base de datos de autorizadores.

**Funciones principales**:
- `cargar_autorizadores()` - Carga autorizadores desde JSON
- `guardar_autorizadores()` - Persiste cambios en BD
- `obtener_autorizadores_por_codigos()` - Filtra por códigos específicos
- `agregar_autorizador()` - Añade nuevo autorizador
- `actualizar_autorizador()` - Modifica datos existentes

**Archivo BD**: `data/autorizadores_bd.json`

### 📋 **data/gestor_solicitudes.py**
**Propósito**: Gestión completa del ciclo de vida de solicitudes.

**Funciones principales**:
- `crear_solicitud()` - Crea nueva solicitud de conformidad
- `obtener_solicitudes()` - Lista todas las solicitudes
- `actualizar_estado_solicitud()` - Cambia estado de solicitud
- `obtener_estadisticas()` - Genera estadísticas del sistema

**Estados de solicitud**:
- `EN_SOLICITUD_CONFORMIDADES` - Estado inicial
- `EN_HELPDESK` - Enviado a helpdesk
- `ATENDIDO` - Procesado por helpdesk
- `CERRADO` - Solicitud completada

### 📧 **email/generador_correos_individuales.py**
**Propósito**: Genera archivos MSG individuales para cada autorizador.

**Funciones principales**:
- `generar_correos_individuales()` - Crea correos personalizados
- `crear_archivo_msg()` - Genera archivo MSG con Outlook
- `generar_contenido_correo()` - Crea contenido del correo

**Output**: `output/correos_individuales/Solicitud_YYYYMMDD_HHMM_*/`

### 🖥️ **gui/aplicacion_principal.py**
**Propósito**: Ventana principal con navegación por pestañas.

**Pestañas**:
1. **Nueva Solicitud** - Crear solicitudes de conformidad
2. **Gestión de Solicitudes** - Seguimiento y edición de estado

**Funcionalidades**:
- Sistema de callbacks entre pestañas
- Actualización automática de datos
- Navegación fluida entre vistas

### 📝 **gui/solicitud_matriz.py**
**Propósito**: Interfaz para crear nuevas solicitudes.

**Funcionalidades**:
- Carga matrices desde `config/matrices.yaml`
- Editor de autorizadores integrado
- Validación de grupos de red
- Generación automática de correos

### 📊 **gui/gestion_solicitudes.py**
**Propósito**: Gestión avanzada de solicitudes existentes.

**Funcionalidades**:
- **Edición en grilla**: Doble-click para editar Estado, Ticket, Observaciones
- **Filtros dinámicos**: Por estado y otros criterios
- **Vista de detalles visual**: Componentes gráficos mejorados
- **Cambio de estados**: Con validaciones de transición
- **Estadísticas en tiempo real**: Contadores por estado

## 🚀 Flujo de Uso Principal

### 1. **Crear Nueva Solicitud**
```
Usuario → Nueva Solicitud → Selecciona Matrices →
Completa Autorizadores → Genera Correos →
Solicitud creada en BD
```

### 2. **Gestión de Solicitudes**
```
Usuario → Gestión → Ve lista → Edita campos →
Cambia estados → Actualiza observaciones
```

### 3. **Seguimiento**
```
Solicitud creada → EN_SOLICITUD_CONFORMIDADES →
EN_HELPDESK (con ticket) → ATENDIDO → CERRADO
```

## ⚙️ Configuración Técnica

### **Dependencias principales**:
- `tkinter` / `customtkinter` - Interfaz gráfica
- `pyyaml` - Lectura de configuración
- `pywin32` - Generación de archivos MSG
- `pathlib` - Manejo de rutas

### **Arquitectura**:
- **Patrón MVC**: Separación clara entre datos, lógica y vista
- **Sistema de eventos**: Callbacks entre componentes
- **Persistencia JSON**: Base de datos local simple
- **Configuración externa**: matrices.yaml para flexibilidad

## 🎯 Puntos de Entrada

### **Instalación Principal**:
```bash
# Un solo clic
INSTALAR.bat

# Instalación rápida
setup\scripts\instalador_rapido.bat
```

### **Ejecución de la Aplicación**:
```bash
# Método 1: Módulo principal
python -m matriz_rol.gui.aplicacion_principal

# Método 2: Script directo
python src/matriz_rol/gui/aplicacion_principal.py

# Método 3: Si está instalado
matriz-rol
```

### **Inicialización**:
```bash
python scripts/inicializar_bd_autorizadores.py
```

### **Scripts de utilidad**:
```bash
python scripts/generar_datos_ficticios.py
python scripts/llenar_datos_completos.py
python scripts/mostrar_bd.py
```
```bash
python scripts/generar_datos_ficticios.py
python scripts/llenar_datos_completos.py
```

## 📋 Archivos de Datos

### **autorizadores_bd.json**
```json
{
  "CODIGO": {
    "autorizador": "Nombre Completo",
    "correo": "email@empresa.com"
  }
}
```

### **solicitudes_conformidad.json**
```json
[
  {
    "id_solicitud": "SOL_20250823_HHMMSS_NNN",
    "fecha_creacion": "2025-08-23T18:12:23",
    "estado": "EN_SOLICITUD_CONFORMIDADES",
    "grupos_red": ["GRUPO1", "GRUPO2"],
    "autorizadores": [...],
    "ticket_helpdesk": null,
    "observaciones": ""
  }
]
```

## 🔧 Mantenimiento

### **Backup automático**:
- Se crea backup diario de solicitudes
- Formato: `backup_solicitudes_YYYYMMDD.json`

### **Logs del sistema**:
- Output detallado en consola
- Emojis para facilitar seguimiento
- Debug información para desarrollo

---

**Estado**: Documentación completa del código final limpio y optimizado.
**Última actualización**: 23 de agosto de 2025
