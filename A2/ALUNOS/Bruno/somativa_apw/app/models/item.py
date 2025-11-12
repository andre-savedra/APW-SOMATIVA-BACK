from django.db import models
from django.core.exceptions import ValidationError

class Item(models.Model):
    date = models.DateTimeField(max_length=150)
    machine_FK = models.ForeignKey('Machine', 
                                related_name='Item_machine_FK',
                                on_delete=models.SET_NULL,
                                null=True)
    lot_FK = models.ForeignKey('Lot', related_name='Item_lot_FK', on_delete=models.DO_NOTHING, null=True)
    
    # CHATGPT helped :D
    def clean(self):
        """Valida se a data do item está dentro do intervalo do lote."""
        lot = self.lot_FK

        # Só valida se o lote e as datas existirem
        if lot and lot.start_date and lot.end_date:
            if not (lot.start_date <= self.date <= lot.end_date):
                raise ValidationError({
                    'date': 'A data de produção do item deve estar entre '
                            'a data de início e a data de fim do lote.'
                })


    def __str__(self):
        return f"Item do lote {self.lot_FK}"