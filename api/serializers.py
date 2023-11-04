from rest_framework import serializers
from api.models import TipoDocumento, Sexo, Estudiante, Libro, Renta, Notificacion
from django.contrib.auth.models import User


class TipoDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDocumento
        fields = "__all__"


class SexoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sexo
        fields = "__all__"


class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = (
            "documento_identidad",
            "tipo_documento",
            "nombres",
            "apellidos",
            "correo",
            "celular",
            "sexo",
        )


class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = ("isbn", "nombre")


class RentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Renta
        fields = (
            "id",
            "estudiante",
            "libro",
            "fecha_renta",
            "fecha_entrega",
            "entregado",
            "fecha_entregado",
        )
        read_only_fields = ("id", "fecha_renta", "entregado", "fecha_entregado")


class RentaFinishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Renta
        fields = (
            "id",
            "estudiante",
            "libro",
            "fecha_renta",
            "fecha_entrega",
            "entregado",
            "fecha_entregado",
        )
        read_only_fields = ("id", "estudiante", "libro", "fecha_renta", "fecha_entrega")


class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = (
            "renta",
            "fecha_evento",
            "titulo",
            "evento",
        )


class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "is_staff",
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "email",
        )


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
