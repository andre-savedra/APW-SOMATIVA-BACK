from rest_framework.viewsets import ModelViewSet
from ..models import *
from ..serializers import *
from app.utils import is_Admin, is_Producao, is_Engenharia, is_Inspecao, is_Manutencao, is_LiderProducao
from rest_framework.response import Response
 

class LoteView(ReadWriteSerializer, ModelViewSet):
    queryset = Lote.objects.all()
    read_serializer_class = LoteReadSerializer
    write_serializer_class = LoteSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Lote.objects.none()

        if is_Inspecao(user) and not is_Admin(user):
            param = self.request.query_params.get("inspecionados_por_mim")
            if param == "1":
                return Lote.objects.filter(responsavel_inspecao=user)
            return Lote.objects.filter(data_inspecao__isnull=True)
        return super().get_queryset()

    def create(self, request, *args, **kwargs):
        if not (is_Producao(request.user) or is_Admin(request.user)):
            return Response(status=403, data="Apenas Produção ou Admin podem criar lotes.")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not (is_Producao(request.user) or is_Admin(request.user)):
            return Response(status=403, data="Apenas Produção ou Admin podem editar lotes.")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not is_Admin(request.user):
            return Response(status=403, data="Apenas Admin pode excluir lotes.")
        return super().destroy(request, *args, **kwargs)
