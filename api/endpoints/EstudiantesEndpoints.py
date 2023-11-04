from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http.response import JsonResponse

from api.models import Estudiante
from api.serializers import EstudianteSerializer


@api_view(["POST"])
@permission_classes([IsAdminUser])
def create_estudiante(request):
    tipo_documento = request.data["tipo_documento"]
    documento_identidad = request.data["documento_identidad"]
    duplicated_student = Estudiante.objects.all().filter(
        tipo_documento=tipo_documento,
        documento_identidad=documento_identidad,
    )
    if duplicated_student.exists():
        return JsonResponse(
            {
                "message": "Ya existe un/a estudiante con este documento de identidad",
                "data": [],
            },
            safe=False,
            status=status.HTTP_400_BAD_REQUEST,
        )

    data_serializer = EstudianteSerializer(data=request.data)
    data_serializer.is_valid(raise_exception=True)
    data_serializer.save()
    return JsonResponse({"message": "OK"}, safe=False, status=status.HTTP_201_CREATED)


@api_view(["PATCH"])
@permission_classes([IsAdminUser])
def update_estudiante(request, pk=None):
    data = Estudiante.objects.all().filter(pk=pk)

    if data.exists():
        data_serializer = EstudianteSerializer(data[0], data=request.data, partial=True)
        data_serializer.is_valid(raise_exception=True)
        data_serializer.save()

        return JsonResponse(
            {"message": "OK", "data": data_serializer.data},
            safe=False,
            status=status.HTTP_200_OK,
        )
    else:
        return JsonResponse(
            {"message": "Estudiante no encontrado", "data": []},
            safe=False,
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_estudiante(request):
    qfilter = request.GET.get("filter", False)

    data = Estudiante.objects.all()
    if qfilter:
        data = data.filter(documento_identidad__icontains=qfilter)

    data_serializer = EstudianteSerializer(data, many=True)
    return JsonResponse(
        {"message": "OK", "data": data_serializer.data},
        safe=False,
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_one_estudiante(request, pk: int):
    data = Estudiante.objects.all().filter(pk=pk)

    if data.exists():
        data_serializer = EstudianteSerializer(data[0], many=False)
        return JsonResponse(
            {"message": "OK", "data": data_serializer.data},
            safe=False,
            status=status.HTTP_200_OK,
        )
    else:
        return JsonResponse(
            {"message": "Estudiante no encontrado", "data": []},
            safe=False,
            status=status.HTTP_404_NOT_FOUND,
        )
