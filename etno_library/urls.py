"""
URL configuration for etno_library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include

from api.endpoints.AuthEndpoints import MyTokenObtainPairView
from api.endpoints.UserEndpoints import change_password, get_user_info, create_user, get_all_users, delete_user
from api.endpoints.EstudiantesEndpoints import (
    create_estudiante,
    update_estudiante,
    get_all_estudiante,
    get_one_estudiante,
)
from api.endpoints.LibrosEndpoints import (
    create_libro,
    update_libro,
    get_all_libro,
    get_one_libro,
)
from api.endpoints.RentasEndpoints import (
    start_croonloop,
    create_renta,
    finish_renta,
    get_all_renta,
    get_one_renta,
)
from api.router import tipos_documentos_router, sexos_router

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("start_croonloop/", start_croonloop, name="start_croonloop"),
    
    path("admin/", admin.site.urls),
    path("login/", MyTokenObtainPairView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("password_change/", change_password, name="change_password"),
    path(
        "password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
    # Endpoints para los usuarios
    path("usuario/create/", create_user, name="create_user"),
    path("usuario/delete/<str:username>", delete_user, name="delete_user"),
    path("usuario/get/all/", get_all_users, name="get_all_users"),
    path("usuario/get/info/", get_user_info, name="get_user_info"),
    # Endpoints para los tipos de documentos
    path("tipos_documentos/", include(tipos_documentos_router.urls)),
    # Endpoints para los tipos de documentos
    path("sexos/", include(sexos_router.urls)),
    # Endpoints para los estudiantes
    path("estudiante/create/", create_estudiante, name="create_estudiante"),
    path("estudiante/update/<int:pk>/", update_estudiante, name="update_estudiante"),
    path("estudiante/get/all/", get_all_estudiante, name="get_all_estudiante"),
    path("estudiante/get/<int:pk>/", get_one_estudiante, name="get_one_estudiante"),
    # Endpoints para los libros
    path("libro/create/", create_libro, name="create_libro"),
    path("libro/update/<int:pk>/", update_libro, name="update_libro"),
    path("libro/get/all/", get_all_libro, name="get_all_libro"),
    path("libro/get/<int:pk>/", get_one_libro, name="get_one_libro"),
    # Endpoints para las rentas
    path("renta/create/", create_renta, name="create_renta"),
    path("renta/finish/<int:pk>/", finish_renta, name="finish_renta"),
    path("renta/get/all/", get_all_renta, name="get_all_renta"),
    path("renta/get/<int:pk>/", get_one_renta, name="get_one_renta"),
]
