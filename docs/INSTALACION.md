# 📦 Instalación y Configuración

## 📋 Requisitos del Sistema

### 🖥️ Sistema Operativo
- Windows 10/11 (requerido para generación de archivos MSG)
- Microsoft Outlook instalado (para generación de correos)

### 🐍 Python
- Python 3.8 o superior
- pip (gestor de paquetes)

## 🚀 Instalación

### 1. Clonar o Descargar el Proyecto
```bash
git clone <url-del-repositorio>
cd utilitarios-matriz-de-rol
```

### 2. Crear Entorno Virtual
```bash
python -m venv venv
```

### 3. Activar Entorno Virtual
```bash
# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 4. Instalar Dependencias
```bash
pip install -r requirements/base.txt
```

### 5. Inicializar Base de Datos
```bash
python inicializar_bd_autorizadores.py
```

## ⚙️ Configuración

### 🔧 Matrices de Rol
El archivo `config/matrices.yaml` contiene las matrices disponibles:

```yaml
matrices_rol:
  - nombre: "Matriz Básica"
    id: "BASIC"
    descripcion: "Matriz de roles básicos del sistema"
  - nombre: "Matriz Avanzada"
    id: "ADVANCED"
    descripcion: "Matriz de roles con permisos avanzados"
```

### 📧 Configuración de Correos
- Asegúrese de que Microsoft Outlook esté instalado
- La aplicación generará archivos .MSG automáticamente

### 💾 Base de Datos
- Los datos se almacenan en archivos JSON en la carpeta `data/`
- Se crean backups automáticos diarios

## 🎮 Primer Uso

### 1. Ejecutar la Aplicación
```bash
# Método recomendado
python -m matriz_rol.gui.aplicacion_principal

# O directamente
python src/matriz_rol/gui/aplicacion_principal.py
```

### 2. Completar Datos de Autorizadores
1. Ve a la pestaña "Nueva Solicitud"
2. Haz clic en "Editar Autorizadores"
3. Completa los datos de nombre y correo para cada código

### 3. Crear Primera Solicitud
1. Selecciona las matrices de rol
2. Ingresa los grupos de red
3. Haz clic en "Crear Solicitud"

## 🛠️ Scripts Útiles

### Generar Datos de Prueba
```bash
python scripts/generar_datos_ficticios.py
```

### Llenar Datos Específicos
```bash
python scripts/llenar_datos_completos.py
```

## 📁 Estructura de Archivos Generados

```
data/
├── autorizadores_bd.json      # Base de datos de autorizadores
├── solicitudes_conformidad.json  # Solicitudes creadas
└── backup_solicitudes_*.json  # Backups automáticos

output/
└── correos_individuales/
    └── Solicitud_*/
        ├── *.msg              # Archivos de correo
        └── RESUMEN_SOLICITUD.txt
```

## 🔧 Solución de Problemas

### Error: "No module named 'matriz_rol'"
- Asegúrese de estar en el directorio correcto
- Verifique que el entorno virtual esté activado

### Error al generar correos MSG
- Verifique que Microsoft Outlook esté instalado
- Ejecute la aplicación como administrador si es necesario

### Base de datos no se carga
- Ejecute `python inicializar_bd_autorizadores.py`
- Verifique permisos de escritura en la carpeta `data/`

## 📞 Soporte

Para problemas técnicos:
1. Revise los logs en la consola
2. Verifique la documentación en `docs/`
3. Consulte los archivos de configuración

---
**✅ Estado**: Guía de instalación completa
**📅 Última actualización**: 23 de agosto de 2025
