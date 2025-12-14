from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventoViewSet


# O DefaultRouter gera as rotas CRUD (GET, POST, PUT, DELETE) e as @actions.
router = DefaultRouter()
router.register(r'eventos', EventoViewSet, basename='evento')


urlpatterns = [
    path('', include(router.urls)),
]
