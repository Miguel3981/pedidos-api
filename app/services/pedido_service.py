from typing import List

from sqlalchemy.orm import Session

from app.models.pedido import Pedido, StatusPedido
from app.repositories.pedido_repository import PedidoRepository
from app.schemas.pedido import PedidoCreate


class PedidoNaoEncontrado(Exception):
    """Levantada quando um pedido solicitado não existe."""


class PedidoService:
    """Concentra a lógica da aplicação: calcula valores e coordena o repositório."""

    def __init__(self, db: Session):
        self.repository = PedidoRepository(db)

    def criar_pedido(self, dados: PedidoCreate) -> Pedido:
        valor_total = dados.quantidade * dados.valor_unitario
        pedido = Pedido(
            cliente=dados.cliente,
            produto=dados.produto,
            quantidade=dados.quantidade,
            valor_unitario=dados.valor_unitario,
            valor_total=valor_total,
            status=StatusPedido.CRIADO,
        )
        return self.repository.criar(pedido)

    def buscar_pedido(self, pedido_id: int) -> Pedido:
        pedido = self.repository.buscar_por_id(pedido_id)
        if pedido is None:
            raise PedidoNaoEncontrado(f"Pedido {pedido_id} não encontrado")
        return pedido

    def listar_pedidos(self) -> List[Pedido]:
        return self.repository.listar()

    def alterar_status(self, pedido_id: int, novo_status: StatusPedido) -> Pedido:
        pedido = self.buscar_pedido(pedido_id)
        pedido.status = novo_status
        return self.repository.salvar(pedido)
