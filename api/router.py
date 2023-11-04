from api.views import TipoDocumentoAPIViewSet, SexoAPIViewSet
from rest_framework.routers import DefaultRouter

tipos_documentos_router = DefaultRouter()
tipos_documentos_router.register(r'', TipoDocumentoAPIViewSet, basename='')

sexos_router = DefaultRouter()
sexos_router.register(r'', SexoAPIViewSet, basename='')