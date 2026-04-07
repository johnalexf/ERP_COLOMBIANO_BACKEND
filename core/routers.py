class ErpDatabaseRouter:
    """
    Este es el 'Semáforo' del sistema. Su fin es evitar que los datos de las 
    empresas se mezclen con los datos de administración del software.
    """
    
    # 1. EL LISTADO MAESTRO:
    # Aquí se define qué aplicaciones son el 'Cerebro' del sistema.
    # Todo lo que esté aquí se guardará SÓLO en la base de datos Administrativa.
    admin_apps = {'users_admin', 'admin', 'auth', 'contenttypes', 'sessions'}

    def db_for_read(self, model, **hints):
        """
        FIN: Decidir de dónde traer la información (Lectura).
        Si Django va a buscar un dato, esta función le dice a qué base de datos ir.
        """
        if model._meta.app_label in self.admin_apps:
            return 'default'  # Ve a la base de datos Administrativa
        return 'tenant'       # Para todo lo demás, ve a la base de datos de Negocio

    def db_for_write(self, model, **hints):
        """
        FIN: Decidir dónde guardar la información (Escritura).
        Asegura que si se crea un administrador, se guarde en la DB central, 
        y si se crea un producto, se guarde en la DB del cliente.
        """
        if model._meta.app_label in self.admin_apps:
            return 'default'
        return 'tenant'

    def allow_relation(self, obj1, obj2, **hints):
        """
        FIN: Blindaje de integridad.
        Su fin es prohibir que una tabla de 'Negocio' intente amarrarse físicamente
        a una tabla de 'Administración'. Esto evita errores catastróficos si 
        mañana se decide mover una base de datos a otro servidor.
        """
        db_obj1 = 'default' if obj1._meta.app_label in self.admin_apps else 'tenant'
        db_obj2 = 'default' if obj2._meta.app_label in self.admin_apps else 'tenant'
        
        if db_obj1 == db_obj2:
            return True # Solo permite la relación si viven en la misma casa
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        FIN: Constructor de infraestructura.
        Cuando se ejecuta el comando 'migrate', esta función le dice a Django:
        'Crea estas tablas SÓLO en esta base de datos'. 
        Evita que la tabla de Usuarios Administrativos aparezca por error en la DB del Cliente.
        """
        if app_label in self.admin_apps:
            return db == 'default'
        return db == 'tenant'