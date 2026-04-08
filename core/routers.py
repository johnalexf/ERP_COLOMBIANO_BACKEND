class ErpDatabaseRouter:
    """
    Enrutador principal ESTRICTO (Strict Allowlist) para la arquitectura Multi-Tenant.
    Controla el tráfico entre la base de datos administrativa y la de inquilinos.
    No permite ambigüedades. Toda aplicación debe estar declarada explícitamente.
    """
    
    # 1. Apps que viven en la base de datos de los clientes inquilinos (empresas)
    TENANT_APPS = ['tenant_users']

    # 2. Apps que viven en la base de datos central administrativa
    # aplicaciones (nativas y nuestras) que van a la base administrativa
    # Incluimos las apps internas de Django para que no se pierdan
    ADMIN_APPS = [
        'admin_users', 
        'admin', 
        'auth', 
        'contenttypes', 
        'sessions',
    ]

    def _get_db(self, app_label):
        """
        Motor de decisión central con Fallo Rápido (Fail-Fast).
        Si un programador instala una librería y no la declara aquí, estalla.
        """
        if app_label in self.TENANT_APPS:
            return 'tenant'
        elif app_label in self.ADMIN_APPS:
            return 'default'
        else:
            # Aquí aplicamos tu regla: Cero ignorancia. Error forzado.
            raise ValueError(f"¡ALERTA ARQUITECTÓNICA! La aplicación '{app_label}' está intentando acceder a la base de datos, pero no ha sido declarada en las listas del ErpDatabaseRouter.")


    def db_for_read(self, model, **hints):
        """
        FIN: Decidir de dónde traer la información (Lectura).
        """
        return self._get_db(model._meta.app_label)

    def db_for_write(self, model, **hints):
        """
        FIN: Decidir dónde guardar la información (Escritura).
        Asegura que si se crea un administrador, se guarde en la DB central, 
        y si se crea un producto, se guarde en la DB del cliente.
        """
        return self._get_db(model._meta.app_label)

    def allow_relation(self, obj1, obj2, **hints):
        """
        FIN: Blindaje de integridad.
        Su fin es prohibir que una tabla de 'Negocio' intente amarrarse físicamente
        a una tabla de 'Administración'. Esto evita errores catastróficos si 
        mañana se decide mover una base de datos a otro servidor.
        """
        """Solo permite relaciones si AMBOS modelos pertenecen a la misma base de datos."""
        db1 = self._get_db(obj1._meta.app_label)
        db2 = self._get_db(obj2._meta.app_label)
        return db1 == db2

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        FIN: Constructor de infraestructura.
        Cuando se ejecuta el comando 'migrate', esta función le dice a Django:
        'Crea estas tablas SÓLO en esta base de datos'. 
        Evita que la tabla de Usuarios Administrativos aparezca por error en la DB del Cliente.
        """
        expected_db = self._get_db(app_label)
        return db == expected_db
    
 