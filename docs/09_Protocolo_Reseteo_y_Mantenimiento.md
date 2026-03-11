# 🛠️ Manual de Mantenimiento, Reseteo y Despliegue Local
Este documento constituye el protocolo de recuperación y puesta en marcha del ERP. Contiene los procedimientos técnicos para limpiar la persistencia de datos, reconstruir el esquema de la base de datos desde cero y verificar la disponibilidad del servicio. Se debe utilizar principalmente durante cambios estructurales en los modelos o en la configuración inicial de nuevos entornos de desarrollo.

## 1. 🔄 Mantenimiento: Reseteo Total de Base de Datos y Migraciones

Este procedimiento elimina toda la estructura y datos existentes para reconstruir el sistema desde cero. Es la solución definitiva ante conflictos de integridad cuando se realizan cambios estructurales profundos (como cambiar el modelo de Usuario).

> **Tip de seguridad:** "Si pgAdmin no permite borrar la base de datos por 'conexiones activas', asegúrese de cerrar Visual Studio Code o detener el servidor de Django, ya que estos mantienen túneles abiertos."

---

### Paso 1: Limpieza en PostgreSQL (pgAdmin)
Antes de reiniciar Django, se debe eliminar el contenedor físico de los datos.

1. Cerrar cualquier conexión activa a la base de datos en pgAdmin.
2. Hacer clic derecho sobre la base de datos (`erp_db`) y seleccionar **Delete/Drop**.
3. Crear nuevamente la base de datos con el mismo nombre: **Create > Database... > `erp_db`**.

---

### Paso 2: Limpieza de Historial de Migraciones
Django almacena el historial de cambios en archivos locales. Para un reseteo total, estos deben ser eliminados.

* **Opcion 1: Eliminación Manual**
1. Navegar a la carpeta de cada aplicación (ej. `apps/users/migrations/`).
2. Borrar todos los archivos numerados (ej. `0001_initial.py`, `0002_...`).
3. **ADVERTENCIA:** No eliminar el archivo `__init__.py`. Este archivo debe permanecer en la carpeta para que Python reconozca que es un paquete.

* **Opcion 2: Eliminación por comando**
> **Nota:** Ejecutar desde la raíz de la aplicación específica
```Bash
# Borrar migraciones excepto __init__.py desde la carpeta de la app:
del /f /q migrations\0*.py
```


---

### Paso 3: Reconstrucción del Esquema
Una vez limpia la base de datos y los archivos locales, se procede a la generación de la nueva estructura.

1. **Asegurar que el Entorno Virtual esté activo:**
   ```bash
   .\venv\Scripts\activate
   ```

2. **Generar la migración inicial única:**
   ```bash
   python manage.py makemigrations
   ```

3. **Ejecutar la creación física en PostgreSQL:**
   ```bash
   python manage.py migrate
   ```

---

### ⚠️ Consecuencias del Reseteo
* **Pérdida de Datos:** Se eliminan todos los registros (Usuarios, Productos, Clientes).
* **Pérdida de Superusuario:** Es obligatorio ejecutar `python manage.py createsuperuser` nuevamente para recuperar el acceso al panel administrativo.


## 2. 🏗️ Ejecutar todas las Migraciones (Crear Tablas)
### Flujo Estándar de Actualización
Este paso construye físicamente las tablas de usuarios y administración en la base de datos PostgreSQL.

```bash
# 1. Preparar las instrucciones (Opcional si no hay cambios en modelos):
python manage.py makemigrations

# 2. Ejecutar la construcción en la base de datos:
python manage.py migrate

# RESULTADO ESPERADO: 
# Una lista de confirmaciones terminando en "OK".
```

---

## 3. 🏃 Lanzamiento del Servidor de Desarrollo
Comprobación final para asegurar que el backend está escuchando peticiones.

```bash
python manage.py runserver

# RESULTADO: El servidor debe informar que está corriendo en [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

#Para terminar la ejecucion usar Ctrl + C
```

---