# IA ajudou, na validação e nas queries
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from ..permissions import IsLeaderUser # Importe sua nova permissão
from ..models import Item, STATUS # Importe Item e STATUS

class DashboardLeaderView(APIView):
    """
    Mostra contagem de peças aprovadas/reprovadas.
    Filtra por data (do item) e funcionário (inspetor do lote).
    """
    permission_classes = [permissions.IsAuthenticated, IsLeaderUser]

    def get(self, request, *args, **kwargs):
        # 1. Define o queryset base (todas as peças)
        base_queryset = Item.objects.all()

        # 2. Pega os parâmetros de filtro da URL (query params)
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        # Filtra pelo ID do funcionário (inspetor)
        inspector_id = request.query_params.get('inspector_id', None) 

        # 3. Aplica os filtros, se eles existirem
        if start_date and end_date:
            # Filtra pela data de produção da PEÇA (Item.date)
            base_queryset = base_queryset.filter(date__range=[start_date, end_date])

        if inspector_id:
            # Filtra pelo inspetor do LOTE (Lot.inspector_FK)
            base_queryset = base_queryset.filter(lot_FK__inspector_FK_id=inspector_id)

        # 4. Calcula os agregados
        # Conta itens cujo lote foi APROVADO
        approved_count = base_queryset.filter(
            lot_FK__status=STATUS.APPROVED
        ).count()
        
        # Conta itens cujo lote foi REPROVADO
        reproved_count = base_queryset.filter(
            lot_FK__status=STATUS.REPROVED
        ).count()

        # 5. Retorna os dados
        data = {
            'total_approved': approved_count,
            'total_reproved': reproved_count
        }
        return Response(data)