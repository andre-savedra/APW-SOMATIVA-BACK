from django.db import models

class STATUS(models.TextChoices):
    APPROVED = 'APPROVED'
    REPROVED = 'REPROVED'

class Lot(models.Model):
    code = models.CharField(max_length=50)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    inspection_date = models.DateTimeField(null=True)
    inspector_FK = models.ForeignKey('CustomUser', 
                                related_name='Lot_inspector_FK',
                                on_delete=models.DO_NOTHING,
                                null=True) # "DO_NOTHING", caso o usuário seja excluído, manter registro que ele foi o responsável
    status = models.CharField(max_length= 50, choices=STATUS, default=None) # Define escolha do status restrita entre as opções da classe STATUS
    product_FK = models.ForeignKey('Product', related_name='Lot_product_FK', on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.code