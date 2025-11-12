from django.db import models
from .maquinas import Maquina
from .customuser import Funcionario

class Manutencao(models.Model):
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE, related_name='historico_manutencao')
    data_manutencao = models.DateTimeField(auto_now_add=True)
    responsavel = models.ForeignKey(
        Funcionario,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to=models.Q(cargo='MANUTENCAO') | models.Q(cargo='ENGENHARIA')
    )
    descricao = models.TextField()
    
    def __str__(self):
        return f"Manutenção na {self.maquina.nome} em {self.data_manutencao.strftime('%Y-%m-%d')}"
    
    # Sobrescrevendo o save para garantir que a Maquina.ultima_data_manutencao seja atualizada
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Atualiza a data da máquina
        self.maquina.ultima_data_manutencao = self.data_manutencao
        self.maquina.responsavel_manutencao = self.responsavel
        self.maquina.save(update_fields=['ultima_data_manutencao', 'responsavel_manutencao'])