from rest_framework.routers import DefaultRouter
from .views import HospedeViewSet, AcomodacaoViewSet, ReservaViewSet, ManutencaoViewSet

router = DefaultRouter()
router.register(r'hospedes', HospedeViewSet)
router.register(r'acomodacoes', AcomodacaoViewSet)
router.register(r'reservas', ReservaViewSet)
router.register(r'manutencoes', ManutencaoViewSet)

urlpatterns = router.urls
