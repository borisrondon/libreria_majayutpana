from django.db import models
from django.db.models.deletion import RESTRICT
from django.core.validators import EmailValidator
from api.validators import ESTUDIANTE_REGEXS, LIBRO_REGEXS


# Create your models here.
class TipoDocumento(models.Model):
    # Llave primaria
    id = models.AutoField(primary_key=True)

    titulo = models.CharField(max_length=40, unique=True)

    def __str__(self):  # Modificar el método to_str
        return str(self.titulo)


class Sexo(models.Model):
    # Llave primaria
    id = models.AutoField(primary_key=True)

    sexo = models.CharField(max_length=19, unique=True)

    def __str__(self):  # Modificar el método to_str
        return str(self.sexo)


class Estudiante(models.Model):
    # Llave primaria
    documento_identidad = models.CharField(
        primary_key=True, max_length=20, validators=[ESTUDIANTE_REGEXS["dni"]]
    )

    # LLaves foráneas
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.RESTRICT)
    sexo = models.ForeignKey(Sexo, on_delete=RESTRICT)

    # Información personal
    nombres = models.CharField(max_length=30, validators=[ESTUDIANTE_REGEXS["nombres"]])
    apellidos = models.CharField(
        max_length=30, validators=[ESTUDIANTE_REGEXS["apellidos"]]
    )
    correo = models.EmailField(validators=[EmailValidator])
    celular = models.CharField(max_length=10, validators=[ESTUDIANTE_REGEXS["celular"]])


class Libro(models.Model):
    # Llave primaria
    isbn = models.CharField(
        max_length=13, primary_key=True, validators=[LIBRO_REGEXS["isbn"]]
    )

    nombre = models.CharField(max_length=60)


class Renta(models.Model):
    # Llave primaria
    id = models.AutoField(primary_key=True)

    # LLaves foráneas
    estudiante = models.ForeignKey(Estudiante, on_delete=RESTRICT)
    libro = models.ForeignKey(Libro, on_delete=RESTRICT)

    fecha_renta = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateTimeField()
    entregado = models.BooleanField(default=False)
    fecha_entregado = models.DateTimeField(null=True)


class Notificacion(models.Model):
    # Llave primaria
    id = models.AutoField(primary_key=True)

    # LLaves foráneas
    renta = models.ForeignKey(Renta, on_delete=RESTRICT)

    # Publicación
    fecha_evento = models.DateTimeField(auto_now_add=True, blank=True)
    titulo = models.CharField(max_length=50, blank=True)
    evento = models.CharField(max_length=300, blank=True)

    class Meta:
        # Nombre en el sitio de admin
        verbose_name = "Notificacion"
        verbose_name_plural = "Notificaciones"
