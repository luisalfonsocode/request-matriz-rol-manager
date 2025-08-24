# Estructura Final de Archivos JSON

## Archivos Activos (Mantener)

### 📁 data/ (Raíz del proyecto)
- ✅ `autorizadores_bd.json` - **BASE DE DATOS CENTRAL DE AUTORIZADORES**
  - Contiene información de autorizadores para TODAS las aplicaciones
  - Usado por `GestorAutorizadores`
  - Estructura: metadata + autorizadores por código de aplicación

- ✅ `solicitudes_conformidad.json` - **BASE DE DATOS DE SOLICITUDES**
  - BD principal de solicitudes de conformidad
  - Usado por `GestorSolicitudes`
  - Migrado desde Documents a la raíz del proyecto

- ✅ `backup_solicitudes_YYYYMMDD.json` - **BACKUPS AUTOMÁTICOS**
  - Backups diarios automáticos de solicitudes
  - Generados automáticamente por el sistema

### 📁 .vscode/
- ✅ `settings.json` - Configuración de VS Code

## Archivos Eliminados (Limpieza Realizada)

### ❌ src/matriz_rol/data/
- ❌ `solicitudes_conformidad.json` - BD antigua (duplicada)
- ❌ `autorizadores_datos.json` - BD antigua de autorizadores

### ❌ matriz_rol/data/
- ❌ `autorizadores_datos.json` - BD antigua de autorizadores (duplicada)

## Archivos de Respaldo (Mantener como Fallback)

### 📁 src/matriz_rol/data/
- ✅ `persistencia.py` - Gestor de persistencia (fallback)
  - Mantiene compatibilidad con sistema anterior
  - Usado como fallback en `AutorizadoresEditorFrame`

## Beneficios de la Nueva Estructura

1. **Centralización**: Todos los datos en `data/` en la raíz
2. **No duplicación**: Eliminados archivos duplicados y obsoletos
3. **Separación clara**:
   - `autorizadores_bd.json` = BD central de TODAS las aplicaciones
   - `solicitudes_conformidad.json` = BD de solicitudes específicas
4. **Backup automático**: Sistema de respaldos diarios
5. **Fallback**: Sistema anterior disponible como respaldo

## Cambios en la Interfaz

- **Ventana de detalles ampliada**: 800x600 → 1000x800 pixeles
- **Mejor experiencia visual**: Más espacio para mostrar información completa
