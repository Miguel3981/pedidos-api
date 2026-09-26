import enum
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum, Integer, Numeric, String

from app.database import Base


class StatusPedido(str, enum.Enum):
    CRIADO = "CRIADO"
    CONFIRMADO = "CONFIRMADO"
    CANCELADO = "CANCELADO"


class Pedido(Base):
    """Modelo de Pedido persistido no PostgreSQL."""

    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    cliente = Column(String, nullable=False)
    produto = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)
    valor_unitario = Column(Numeric(10, 2), nullable=False)
    valor_total = Column(Numeric(10, 2), nullable=False)
    status = Column(
        Enum(StatusPedido, name="status_pedido"),
        nullable=False,
        default=StatusPedido.CRIADO,
    )
    data_criacao = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
