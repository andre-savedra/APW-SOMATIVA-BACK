from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile


from .models import Category, Product, Machine, Lote, Maintence, StatusDashboard
from django.contrib.auth import get_user_model
from .serializers import (
    UserSerializer, CategorySerializer, ProductSerializer,
        MachineSerializer, LoteSerializer, MaintenceSerializer,
    DashboardLoteSerializer, DashboardStatusSerializer
)
from .permissions import IsInspector, IsProduction, IsMaintenance, IsProductionLeader

User = get_user_model()

class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsProductionLeader]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsProductionLeader()]
        return [permissions.IsAuthenticated()]

class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

class MachineView(ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsMaintenance() | IsProductionLeader()]
        return [permissions.IsAuthenticated()]

class LoteView(ModelViewSet):
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsProduction() | IsInspector()]
        return [permissions.IsAuthenticated()]

class MaintenceView(ModelViewSet):
    queryset = Maintence.objects.all()
    serializer_class = MaintenceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsMaintenance() | IsProductionLeader()]
        return [permissions.IsAuthenticated()]

class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            data = serializer.data
            data['access'] = str(refresh.access_token)
            data['refresh'] = str(refresh)
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)
        if user is None:
            return Response({'detail': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        user_data = UserSerializer(user).data
        return Response({
            'user': user_data,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_200_OK)

class DashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsProductionLeader]

    def get(self, request):

        total_products = Product.objects.count()
        total_machines = Machine.objects.count()
        total_lotes = Lote.objects.count()
        total_maintenance = Maintence.objects.count()

        recent_lotes = Lote.objects.select_related(
            'product', 'responsible'
        ).order_by('-start_date')[:5]

        two_months_ago = timezone.now() - timedelta(days=60)
        machines_needing_maintenance = Machine.objects.filter(
            Q(maintence__isnull=True) |
            Q(maintence__end_date__lt=two_months_ago)
        ).distinct()

        inspected_lotes = Lote.objects.exclude(inspect_date__isnull=True).count()
        pending_inspection = Lote.objects.filter(inspect_date__isnull=True).count()

        response_data = {
            'overview': {
                'total_products': total_products,
                'total_machines': total_machines,
                'total_lotes': total_lotes,
                'total_maintenance': total_maintenance,
                'inspected_lotes': inspected_lotes,
                'pending_inspection': pending_inspection
            },
            'recent_lotes': [
                {
                    'id': lote.id,
                    'name': lote.name,
                    'product_name': lote.product.name,
                    'responsible_name': lote.responsible.name,
                    'start_date': lote.start_date,
                    'end_date': lote.end_date,
                    'inspect_date': lote.inspect_date
                } for lote in recent_lotes
            ],
            'maintenance_needed': [
                {
                    'id': machine.id,
                    'name': machine.name,
                    'description': machine.description
                } for machine in machines_needing_maintenance
            ]
        }

        return Response(response_data)
    
def criar_produto_com_qrcode(request):
    produto = Product.objects.create(name="PC")
    
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(f"produto-{produto.id}")
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    
    produto.qr_code.save(f"produto_{produto.id}_qrcode.png", ContentFile(buffer.getvalue()))
    produto.save()
    
    return Response(f"Produto {produto.name} criado com QR Code.")