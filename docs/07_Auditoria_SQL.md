# 🔍 Manual de Auditoría y Verificación de Estructura SQL

Este documento detalla las herramientas y comandos disponibles para inspeccionar la integridad del sistema y visualizar las instrucciones de lenguaje SQL puro que Django genera antes de impactar la base de datos PostgreSQL o despues de haber creado las tablas, según la ópcion que se elija a continuación.

Si se desea obtener la totalidad del código SQL que define la estructura actual de la base de datos o el historial de cambios ejecutados, existen tres métodos técnicos principales, dependiendo de qué información exacta se requiera documentar

---

## 1. Respaldo de Estructura (DUMP)
Es la forma más directa de obtener el SQL de todas las tablas, relaciones, índices y restricciones en un solo archivo. Este comando se ejecuta desde la terminal de Windows (CMD como administrador) utilizando la herramienta propia de PostgreSQL, esto genera un archivo con el codigo SQL desde donde se ejecute el comando.

> **Nota:**
> Al ejecutar el siguiente comando se creara un archivo, es recomendable dirigirse primero a la carpeta donde se desee guardar dicho documento, preferiblemente en esta misma carpeta del repositorio para tenerlo a la mano.

```bash
# Exportar solo la estructura (sin datos) de toda la base de datos:
pg_dump -U postgres -s nombre_base_datos > estructura_completa.sql
```
> Cambiar `nombre_base_datos` por el nombre de la base de datos a obtener codigo SQL

* `-s`: Indica que solo se desea el "schema" (la estructura), no los registros.
* **Resultado:** Un archivo `.sql` con todos los `CREATE TABLE` y `ALTER TABLE` necesarios para replicar el ERP desde cero en cualquier servidor.

> **Requisito para pg_dump**
Para que el comando `pg_dump` funcione directamente en la terminal de Windows, la carpeta bin de PostgreSQL 18 debe estar en las Variables de Entorno (PATH) del sistema.

Si al ejecutarlo recibe el error: `"pg_dump no se reconoce como un comando"`, deberá ejecutarlo desde la ruta completa:
```bash
"C:\Program Files\PostgreSQL\18\bin\pg_dump.exe" -U postgres -s nombre_base_datos > estructura_completa.sql
```



---

## 2. Auditoría por Aplicación (sqlmigrate)
El comando `sqlmigrate` está diseñado para auditar cambios específicos **antes** de que se apliquen o para entender la lógica de un archivo de migración puntual. Si se han realizado múltiples migraciones (0001, 0002, 0003), se debe ejecutar el comando por cada una para ver el historial de evolución de esa tabla.

```Bash
python manage.py sqlmigrate users 0001
python manage.py sqlmigrate users 0002
```

Este método es útil para el manual técnico si se desea explicar cómo fue evolucionando el modelo de datos paso a paso.

* **Ver estado de migraciones**	

    ```bash
    python manage.py showmigrations
    ```
    *(Las marcadas con [X] ya existen en la DB; las [ ] están pendientes). Allí se podrá ver el número exacto (ej. 0001) de una lista de aplicaciones*
    

* **Ver SQL de una tabla específica**
    
    ```bash
    python manage.py sqlmigrate users 0001
    ```
    Permite visualizar el código SQL puro que se envió a la base de datos. Es útil para documentar la estructura en el manual técnico del sistema.

    > **Nota Técnica:** Es importante tener en cuenta que sqlmigrate requiere dos parámetros: el nombre de la aplicación (users) y el número de la migración (0001). Esto permite auditar exactamente qué código SQL se generó para ese cambio específico.

* **Verificar errores generales**

     ```bash
    python manage.py check
    ```


---

## 3. Registro en Tiempo Real (SQL Logging)
Existe una configuración avanzada que permite ver en la terminal de VS Code cada instrucción SQL que Django envía a PostgreSQL mientras el servidor está corriendo. Esto es sumamente útil para entender qué hace Django "tras bambalinas".

Para activar esta función, se debe agregar el siguiente bloque al **final** del archivo `core/settings.py`:

```Python
# Habilita poder visualizar cada instrucción SQL que Django envía a PostgreSQL mientras el servidor está corriendo 
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    },
}
```

Al activar esto, cada vez que se ejecute un `migrate`, un `check` o incluso cuando un usuario inicie sesión desde el Frontend, la terminal de Django imprimirá el código SQL exacto que se está procesando en ese instante.

> [!WARNING]
> **Uso en Producción:** Se recomienda **comentar o eliminar** este bloque de `LOGGING` una vez que el sistema pase a producción. Mantenerlo activo puede generar archivos de registro (logs) excesivamente grandes y exponer información sensible de las consultas en los servidores de despliegue.

---


## 📊 Comparativa de Métodos

| Método | Resultado | Uso Recomendado |
| :--- | :--- | :--- |
| **`pg_dump`** | Un solo archivo con toda la BD. | Para respaldos y documentación final del esquema. |
| **`sqlmigrate`** | SQL de un cambio específico. | Para entender una migración puntual. |
| **`LOGGING`** | Flujo constante de SQL en consola. | Para depuración (debugging) y aprendizaje. |

