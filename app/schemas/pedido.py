from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class StatusPedido(str, Enum):
    CRIADO = "CRIADO"
    CONFIRMADO = "CONFIRMADO"
    CANCELADO = "CANCELADO"


class PedidoCreate(BaseModel):
    """Corpo esperado em POST /pedidos."""

    cliente: str = Field(..., min_length=1, description="Identificação textual do cliente")
    produto: str = Field(..., min_length=1, description="Identificação textual do produto")
    quantidade: int = Field(..., gt=0, description="Quantidade solicitada")
    valor_unitario: Decimal = Field(..., gt=0, description="Preço de uma unidade")


class PedidoStatusUpdate(BaseModel):
    """Corpo esperado em PATCH /pedidos/{id}/status."""

    status: StatusPedido


class PedidoResponse(BaseModel):
    """Representação de um pedido retornada pela API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    cliente: str
    produto: str
    quantidade: int
    valor_unitario: Decimal
    valor_total: Decimal
    status: StatusPedido
    data_criacao: datetime
