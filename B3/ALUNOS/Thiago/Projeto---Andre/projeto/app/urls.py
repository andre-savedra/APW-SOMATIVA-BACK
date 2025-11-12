# app/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'reservas', ReservasViewSet)
router.register(r'hospede', HospedeViewSet)
router.register(r'acomodacao', AcomodacaoViewSet)
router.register(r'empregado', EmpregadoViewSet)
router.register(r'limpeza', LimpezaViewSet)
router.register(r'manutencoes', ManutencoesViewSet)
urlpatterns = router.urls