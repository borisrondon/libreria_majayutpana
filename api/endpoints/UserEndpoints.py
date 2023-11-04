from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from django.http.response import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q
from api.serializers import UserSerializer, UserGetSerializer, ChangePasswordSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password(request):
    current_user = User.objects.filter(pk=request.user.pk)

    if current_user.exists():
        current_user = current_user[0]
        data_serializer = ChangePasswordSerializer(data=request.data)
        data_serializer.is_valid(raise_exception=True)

        if not current_user.check_password(data_serializer.data.get("old_password")):
            return JsonResponse(
                {"message": "Contraseña actual incorrecta", "data": []},
                safe=False,
                status=status.HTTP_400_BAD_REQUEST,
            )

        current_user.set_password(data_serializer.data.get("new_password"))
        current_user.save()
        return JsonResponse(
            {"message": "OK", "data": data_serializer.data},
            safe=False,
            status=status.HTTP_200_OK,
        )
    else:
        return JsonResponse(
            {"message": "Usuario no encontrado", "data": []},
            safe=False,
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["POST"])
@permission_classes([IsAdminUser])
def create_user(request):
    data_serializer = UserSerializer(data=request.data)
    data_serializer.is_valid(raise_exception=True)

    username = request.data["username"]
    password = request.data["password"]
    email = request.data["email"]

    if "password_confirm" not in request.data:
        return JsonResponse(
            {
                "message": "Falta el campo password_confirm",
                "data": [],
            },
            safe=False,
            status=status.HTTP_400_BAD_REQUEST,
        )

    password_confirm = request.data["password_confirm"]
    if password != password_confirm:
        return JsonResponse(
            {
                "message": "Las contraseñas no coinciden",
                "data": [],
            },
            safe=False,
            status=status.HTTP_400_BAD_REQUEST,
        )

    email_exists = User.objects.all().filter(email=email)
    if email_exists.exists():
        return JsonResponse(
            {"message": "El correo ya está en uso", "data": []},
            safe=False,
            status=status.HTTP_400_BAD_REQUEST,
        )

    User.objects.create_user(username, email, password)
    return JsonResponse(
        {"message": "OK", "data": []}, safe=False, status=status.HTTP_201_CREATED
    )


@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def delete_user(request, username=None):
    if username == request.user.username:
        return JsonResponse(
            {"message": "No se puede auto eliminar", "data": ""},
            safe=False,
            status=status.HTTP_400_BAD_REQUEST,
        )

    data = User.objects.all().filter(username=username, is_staff=False)
    if data.exists():
        data[0].delete()

        return JsonResponse(
            {"message": "OK", "data": ""},
            safe=False,
            status=status.HTTP_204_NO_CONTENT,
        )
    else:
        return JsonResponse(
            {"message": "Usuario no encontrado", "data": []},
            safe=False,
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    qfilter = request.GET.get("filter", False)

    data = User.objects.all()
    data = data.filter(~Q(pk=request.user.pk))  # Para que no liste al usuario actual
    if qfilter:
        data = data.filter(Q(username__icontains=qfilter) | Q(email__icontains=qfilter))

    data_serializer = UserGetSerializer(data, many=True)
    return JsonResponse(
        {"message": "OK", "data": data_serializer.data},
        safe=False,
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    data = User.objects.filter(pk=request.user.pk)
    data_serializer = UserGetSerializer(data[0], many=False)
    return JsonResponse(
        {"message": "OK", "data": data_serializer.data},
        safe=False,
        status=status.HTTP_200_OK,
    )