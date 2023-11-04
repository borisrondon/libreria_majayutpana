from django.contrib import admin
from api.models import TipoDocumento, Sexo, Estudiante, Libro, Renta, Notificacion


# Register your models here.
class Admin_Estudiante(admin.ModelAdmin):
    list_display = ("nombres", "apellidos", "documento_identidad")


class Admin_Libro(admin.ModelAdmin):
    list_display = ("isbn", "nombre")


class Admin_Renta(admin.ModelAdmin):
    list_display = (
        "estudiante",
        "libro",
        "fecha_renta",
        "fecha_entrega",
    )

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False



class Admin_Notificacion(admin.ModelAdmin):
    list_display = (
        "renta",
        "fecha_evento",
        "titulo",
        "evento",
    )

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(TipoDocumento)
admin.site.register(Sexo)
admin.site.register(Estudiante, Admin_Estudiante)
admin.site.register(Libro, Admin_Libro)
admin.site.register(Renta, Admin_Renta)
admin.site.register(Notificacion, Admin_Notificacion)
