from .categoria import CategoriaSerializer
from .custom_user import CustomUserSerializer
from .lote import LoteSerializer, LoteReadSerializer, LoteWriteSerializer
from .maquina import MaquinaSerializer
from .producao import ProducaoSerializer
from .produto import ProdutoSerializer
from .custom_S import ReadWriteSerializer
__all__ = [
    'CategoriaSerializer',
    'CustomUserSerializer',
    'LoteSerializer',
    'LoteReadSerializer',
    'LoteWriteSerializer',
    'MaquinaSerializer',
    'ProducaoSerializer',
    'ProdutoSerializer',
    'ReadWriteSerializer'
]