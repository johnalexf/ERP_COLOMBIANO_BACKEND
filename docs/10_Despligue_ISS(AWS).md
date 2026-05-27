# 🌐 Manual de Despliegue: Django API en un IIS Existente (2026)

Este manual guía la creación de un nuevo sitio para el Backend corriendo en su propio entorno aislado (`venv`) en un servidor que ya tiene el Frontend funcionando, evitando conflictos de puertos.

---

## 1. 🛡️ Configuración de Red en AWS
Para que el Frontend (Puerto 80) pueda hablar con la API (Puerto 8000), el puerto debe estar abierto en la nube.

1. Entra a tu consola de **AWS** > **EC2** > **Security Groups**.
2. Selecciona el grupo de tu instancia.
3. En **Inbound Rules**, añade:
   - **Type:** Custom TCP
   - **Port Range:** `8000`
   - **Source:** `0.0.0.0/0` (Acceso total para pruebas)

---

## 2. 🏗️ Preparación del Servidor (IIS & CGI)
Verificar que el motor de procesos externos esté activo.

1. **Server Manager** > **Add Roles and Features**.
2. **Server Roles** > **Web Server (IIS)** > **Web Server** > **Application Development**.
3. **MÁXIMA PRIORIDAD:** Asegúrate de que **CGI** tenga el check de instalado. Si no, instálalo.

---

## 3. 🐍 Habilitar el Puente "wfastcgi" (Solo una vez)
Este paso registra a Python dentro de la configuración global de IIS., registra la capacidad de FastCGI en el sistema operativo.

1. Abre PowerShell como **Administrador**.
2. Ejecuta:
   ```powershell
   pip install wfastcgi
   wfastcgi-enable
   ```
 *Nota: Esto habilita el motor a nivel sistema. Las rutas del proyecto las definiremos en el paso 8.*

---

## 4. 📥 Clonación y Entorno Virtual
Bajar el código y "activarlo".

1. En `C:\inetpub\wwwroot\`, clona tu repo de backend:

   ```powershell
   git clone https://tu-repo.git erp_backend
   cd erp_backend
   ```
2. Crea el entorno virtual (Solo la primera vez) y actívalo:

   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Instala todo y genera los estáticos:
   ```powershell
   pip install -r requirements.txt
   pip install wfastcgi
   ```
4. Sincronizar Base de Datos y Estáticos
```powershell
   #verificar conectividad con la base de datos
   python manage.py check

   #Crear las tablas en la base de datos
   python manage.py migrate
   ```

---

## 5. 🏗️ Preparación de Archivos Estáticos (Producción)
Este paso es el "build" de Django para que el Admin y la API se vean bien.

1. En `core/settings.py` (en el servidor), verificar que estas configuraciones existan:
   ```python
   import os
   STATIC_URL = '/static/'
   STATIC_ROOT = os.path.join(BASE_DIR, 'static')
   ```
2. Ejecutar la recolección (con venv activo):
   ```powershell
   python manage.py collectstatic
   ```
   *(Esto creará la carpeta `static/` en la raíz del proyecto con todos los estilos).*

---

## 6. 🔑 Configuración del Entorno (.env)

1. Localice el archivo `.env.template`.
2. Cree una copia llamada `.env` en la raíz.
3. Defina sus credenciales de **PostgreSQL 18** y su `SECRET_KEY`.
4. **Asegúrate de cambiar:**
- `DEBUG=False`
- `ALLOWED_HOSTS=IP_DE_AWS,localhost,127.0.0.1`
- `CORS_ALLOWED_ORIGINS=http://IP_DE_AWS` (Puerto 80 de tu Front)

---

## 7. ⚙️ Creación del Nuevo "Web Site" en IIS
Aquí es donde configuramos que la API viva en el puerto 8000.

1. Abre el **IIS Manager**.
2. En el panel izquierdo, clic derecho en **Sites** > **Add Website**.
3. Configura los campos así:
   - **Site name:** `ERP_Backend`
   - **Physical path:** `C:\inetpub\wwwroot\erp_backend`
   - **Binding (Type):** http
   - **IP Address:** All Unassigned
   - **Port:** `8000`  <-- (Esto evita el conflicto con tu página web)
4. Dale a **OK**.

---

## 8. 🔐 Permisos y web.config 

### A. Permisos de Usuario
1. Clic derecho en la carpeta `erp_backend` > **Properties** > **Security**.
2. Clic en **Edit** > **Add** > escribe `IIS_IUSRS` > **Check Names** > **OK**.
3. Dale permisos de **Read & Execute**, **List folder contents** y **Read**.

### B. Crear el archivo web.config
Crea un archivo llamado `web.config` en la raíz (donde está el `manage.py`) y pega este código (ajustando las rutas a tu proyecto):

```xml
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <system.webServer>
    <handlers>
      <add name="PythonHandler" 
           path="*" 
           verb="*" 
           modules="FastCgiModule" 
           scriptProcessor="C:\inetpub\wwwroot\erp_backend\venv\Scripts\python.exe|C:\inetpub\wwwroot\erp_backend\venv\Lib\site-packages\wfastcgi.py" 
           resourceType="Unspecified" 
           requireAccess="Script" />
    </handlers>
  </system.webServer>
  <appSettings>
    <add key="PYTHONPATH" value="C:\inetpub\wwwroot\erp_backend" />
    <add key="WSGI_HANDLER" value="core.wsgi.application" />
    <add key="DJANGO_SETTINGS_MODULE" value="core.settings" />
  </appSettings>
</configuration>
```

> [!IMPORTANTE]
> **Usa las rutas de TU carpeta erp_backend y su venv**

---
## 9. 🔄 Flujo de Actualización Futura
Cuando hagas cambios en tu PC y quieras verlos en AWS:
1. `git pull origin main`
2. `.\venv\Scripts\activate`
3. `pip install -r requirements.txt` (Para nuevas librerías)
4.  `python manage.py migrate` <-- (Vital por si se realizaron cambios en los modelos)
5. `python manage.py collectstatic` (Si cambiaste algo visual o del Admin)
6. **Reiniciar el sitio en IIS Manager.**

---
## 10. ✅ Verificación
1. Reinicia el sitio desde el panel derecho de IIS Manager.

2. Desde tu PC personal, abre el navegador en: `http://IP_PUBLICA_AWS:8000/api/users/`.

3. Si obtienes una respuesta JSON o un mensaje de error de autenticación de Django, el despliegue ha sido **exitoso**.
---
