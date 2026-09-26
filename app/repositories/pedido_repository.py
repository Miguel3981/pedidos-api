from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.pedido import Pedido


class PedidoRepository:
    """Encapsula o acesso ao banco para a entidade Pedido."""

    def __init__(self, db: Session):
        self.db = db

    def criar(self, pedido: Pedido) -> Pedido:
        self.db.add(pedido)
        self.db.commit()
        self.db.refresh(pedido)
        return pedido

    def buscar_por_id(self, pedido_id: int) -> Optional[Pedido]:
        return self.db.query(Pedido).filter(Pedido.id == pedido_id).first()

    def listar(self) -> List[Pedido]:
        return self.db.query(Pedido).order_by(Pedido.id).all()

    def salvar(self, pedido: Pedido) -> Pedido:
        """Persiste alterações feitas em um pedido já existente."""
        self.db.commit()
        self.db.refresh(pedido)
        return pedido
