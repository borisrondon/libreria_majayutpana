import datetime
from pytz import timezone

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.http.response import JsonResponse

from api.models import Renta
from api.serializers import RentaSerializer, RentaFinishSerializer

from start_cronloop import start_cronloop, get_last_process_pid

tz = timezone("America/Bogota")


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_renta(request):
    data_serializer = RentaSerializer(data=request.data)
    data_serializer.is_valid(raise_exception=True)

    # Se valida si el libro está ocupado
    libro__pk = data_serializer.validated_data.__getitem__("libro").pk
    libro_ocupado = Renta.objects.all().filter(
        fecha_entregado__isnull=True, libro=libro__pk
    )
    if libro_ocupado.exists():
        return JsonResponse(
            {"message": "El libro solicitado se encuentra ocupado", "data": []},
            safe=False,
            status=status.HTTP_410_GONE,
        )

    # Se valida si el estudiante ha alcanzado el máximo de rentas activas
    estudiante__pk = data_serializer.validated_data.__getitem__("estudiante").pk
    rentas_estudiante = Renta.objects.all().filter(
        fecha_entregado__isnull=True, estudiante=estudiante__pk
    )
    if len(rentas_estudiante) >= 3:
        return JsonResponse(
            {
                "message": "El estudiante ha alcanzado el tope de rentas activas (3)",
                "data": [],
            },
            safe=False,
            status=status.HTTP_410_GONE,
        )

    date_now = datetime.datetime.now(tz=tz).date()
    for renta in rentas_estudiante:
        if renta.fecha_entrega is None:
            continue
        elif renta.fecha_entrega.date() < date_now:
            return JsonResponse(
                {"message": "El estudiante cuenta con una renta vencida", "data": []},
                safe=False,
                status=status.HTTP_410_GONE,
            )

    # Si pasa toda las validaciones, se crea la renta
    data_serializer.save()
    return JsonResponse(
        {"message": "OK", "data": data_serializer.data},
        safe=False,
        status=status.HTTP_201_CREATED,
    )


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def finish_renta(request, pk=None):
    data = Renta.objects.all().filter(pk=pk)

    if data.exists():
        data.update(fecha_entregado=datetime.datetime.now(tz=tz), entregado=True)
        data_serializer = RentaFinishSerializer(data[0], many=False)

        return JsonResponse(
            {"message": "OK", "data": data_serializer.data},
            safe=False,
            status=status.HTTP_200_OK,
        )
    else:
        return JsonResponse(
            {"message": "Renta no encontrada", "data": []},
            safe=False,
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_renta(request):
    qfilter = request.GET.get("filter", False)
    qfilter_field = request.GET.get("filterField", False)

    data = Renta.objects.all().order_by("-fecha_renta")
    if qfilter and qfilter_field == "estudiante":
        data = data.filter(estudiante__documento_identidad__icontains=qfilter)
    elif qfilter and qfilter_field == "libro":
        data = data.filter(libro__isbn__icontains=qfilter)

    data_serializer = RentaSerializer(data, many=True)
    return JsonResponse(
        {"message": "OK", "data": data_serializer.data},
        safe=False,
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_one_renta(request, pk: int):
    data = Renta.objects.all().filter(pk=pk)

    if data.exists():
        data_serializer = RentaSerializer(data[0], many=False)
        return JsonResponse(
            {"message": "OK", "data": data_serializer.data},
            safe=False,
            status=status.HTTP_200_OK,
        )
    else:
        return JsonResponse(
            {"message": "Renta no encontrado", "data": []},
            safe=False,
            status=status.HTTP_404_NOT_FOUND,
        )


# Inicia el loop que ejecuta los cron job
@api_view(["GET"])
def start_croonloop(request):
    last_process_pid = get_last_process_pid()
    start_cronloop(last_process_pid)
    print("proccess already started")

    return JsonResponse(
        {"message": "OK", "data": ""},
        safe=False,
        status=status.HTTP_200_OK,
    )
