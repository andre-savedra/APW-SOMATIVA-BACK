from rest_framework import serializers
from .models import Guest, Accommodation, Reservation, Employee, CleaningRecord, MaintenanceRecord

class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = '__all__'


class CleaningRecordSerializer(serializers.ModelSerializer):
    funcionario = serializers.StringRelatedField()  # mostra nome do funcionário
    class Meta:
        model = CleaningRecord
        fields = '__all__'


class MaintenanceRecordSerializer(serializers.ModelSerializer):
    funcionario = serializers.StringRelatedField()
    class Meta:
        model = MaintenanceRecord
        fields = '__all__'


class AccommodationSerializer(serializers.ModelSerializer):
    # incluir a última limpeza detalhada e o funcionário responsável
    ultima_limpeza = serializers.SerializerMethodField()

    class Meta:
        model = Accommodation
        fields = ['id','numero','tipo','capacidade','valor_diaria','status','data_ultima_limpeza','ultima_limpeza']

    def get_ultima_limpeza(self, obj):
        last = obj.limpezas.order_by('-data_limpeza').first()
        if not last:
            return None
        return CleaningRecordSerializer(last).data


class ReservationSerializer(serializers.ModelSerializer):
    # retornar nome do hóspede e número da acomodação conforme requisito
    hospede_nome = serializers.CharField(source='hospede.nome_completo', read_only=True)
    acomodacao_numero = serializers.CharField(source='acomodacao.numero', read_only=True)

    class Meta:
        model = Reservation
        fields = ['id','codigo','hospede','hospede_nome','acomodacao','acomodacao_numero','data_checkin','data_checkout','valor_total','status']


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
