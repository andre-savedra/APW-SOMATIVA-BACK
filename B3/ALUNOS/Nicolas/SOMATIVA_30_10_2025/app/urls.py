from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'hospedes', HospedeViewSet, basename='hospede')
router.register(r'acomodacoes', AcomodacaoViewSet, basename='acomodacao')
router.register(r'reservas', ReservaViewSet, basename='reserva')
router.register(r'governanca/pendentes', GovernancaPendentesViewSet, basename='governanca-pendentes')

urlpatterns = router.urls

