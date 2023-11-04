from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes
from rest_framework.viewsets import ViewSet
from django.http.response import JsonResponse

from api.models import TipoDocumento, Sexo
from api.serializers import (
    TipoDocumentoSerializer,
    SexoSerializer,
)


# Endpoints para los tipos de documentos
class TipoDocumentoAPIViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        data = TipoDocumento.objects.all()
        data_serializer = TipoDocumentoSerializer(data, many=True)
        return JsonResponse(
            {"message": "OK", "data": data_serializer.data},
            safe=False,
            status=status.HTTP_200_OK,
        )


# Endpoints para los sexos
class SexoAPIViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        data = Sexo.objects.all()
        data_serializer = SexoSerializer(data, many=True)
        return JsonResponse(
            {"message": "OK", "data": data_serializer.data},
            safe=False,
            status=status.HTTP_200_OK,
        )
