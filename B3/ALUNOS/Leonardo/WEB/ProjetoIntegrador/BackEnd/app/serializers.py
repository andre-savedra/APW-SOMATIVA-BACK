from rest_framework import serializers
from .models import *

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('name', 'photo', 'email', 'creation_date')
        many = True

class AmbienteSerializer(serializers.ModelSerializer):
    class Meta:
       model = Ambiente
       fields = '__all__'
       many = True

# opção de pegar apenas o campo name da categoria
    category_FK = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )

class AtivoSerializer(serializers.ModelSerializer):
    class Meta:
       model = Ativo
       fields = '__all__'
       many = True

class AtivoWriteSerializer(serializers.ModelSerializer):      
    class Meta:
        model = Ativo   #model de conversão
        fields = '__all__' #todos os campos
        many = True        #permite serialização de vários
    

class TarefasSerializer(serializers.ModelSerializer):
    class Meta:
       model = Tarefas
       fields = '__all__'
       many = True
      

class HistoricoStatusSerializer(serializers.ModelSerializer):
    class Meta:
       model = HistoricoStatus
       fields = '__all__'
       many = True

class TarefaStatusImageSerializer(serializers.ModelSerializer):
    class Meta:
       model = TarefaStatusImage
       fields = '__all__'
       many = True

class NoificationSerializer(serializers.ModelSerializer):
    class Meta:
       model = Notification
       fields = '__all__'
       many = True

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category   #model de conversão
        fields = '__all__' #todos os campos
        many = True        #permite serialização de vários