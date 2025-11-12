from django.db import models
from .lote import Lote
from .maquinas import Maquina
from .produtos import Produto


class ItemProducao(models.Model):
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE, related_name='itens_produzidos')
    data_hora_item = models.DateTimeField(auto_now_add=True)

    maquina = models.ForeignKey(Maquina, on_delete=models.PROTECT)
 
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT) 

    def __str__(self):
        return f"Item {self.id} do Lote {self.lote.codigo}"