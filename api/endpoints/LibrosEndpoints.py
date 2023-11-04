from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from django.http.response import JsonResponse
from django.db.models import Q

from api.models import Libro
from api.serializers import LibroSerializer


@api_view(["POST"])
@permission_classes([IsAdminUser])
def create_libro(request):
    data_serializer = LibroSerializer(data=request.data)
    data_serializer.is_valid(raise_exception=True)
    data_serializer.save()
    return JsonResponse({"message": "OK"}, safe=False, status=status.HTTP_201_CREATED)


@api_view(["PATCH"])
@permission_classes([IsAdminUser])
def update_libro(request, pk=None):
    data = Libro.objects.all().filter(pk=pk)

    if data.exists():
        data_serializer = LibroSerializer(data[0], data=request.data, partial=True)
        data_serializer.is_valid(raise_exception=True)
        data_serializer.save()

        return JsonResponse(
            {"message": "OK", "data": data_serializer.data},
            safe=False,
            status=status.HTTP_200_OK,
        )
    else:
        return JsonResponse(
            {"message": "Libro no encontrado", "data": []},
            safe=False,
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_libro(request):
    qfilter = request.GET.get("filter", False)

    data = Libro.objects.all()
    if qfilter:
        data = data.filter(Q(nombre__icontains=qfilter) | Q(isbn__icontains=qfilter))

    data_serializer = LibroSerializer(data, many=True)
    return JsonResponse(
        {"message": "OK", "data": data_serializer.data},
        safe=False,
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_one_libro(request, pk: int):
    data = Libro.objects.all().filter(pk=pk)

    if data.exists():
        data_serializer = LibroSerializer(data[0], many=False)
        return JsonResponse(
            {"message": "OK", "data": data_serializer.data},
            safe=False,
            status=status.HTTP_200_OK,
        )
    else:
        return JsonResponse(
            {"message": "Libro no encontrado", "data": []},
            safe=False,
            status=status.HTTP_404_NOT_FOUND,
        )