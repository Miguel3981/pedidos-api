from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.pedido import PedidoCreate, PedidoResponse, PedidoStatusUpdate
from app.services.pedido_service import PedidoNaoEncontrado, PedidoService

router = APIRouter(prefix="/pedidos", tags=["pedidos"])


@router.post("", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
def criar_pedido(dados: PedidoCreate, db: Session = Depends(get_db)):
    """POST /pedidos — cria um pedido; a aplicação calcula valor_total e status inicial."""
    service = PedidoService(db)
    return service.criar_pedido(dados)


@router.get("/{pedido_id}", response_model=PedidoResponse)
def consultar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    """GET /pedidos/{id} — 200 OK se existir, 404 Not Found caso contrário."""
    service = PedidoService(db)
    try:
        return service.buscar_pedido(pedido_id)
    except PedidoNaoEncontrado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado")


@router.get("", response_model=List[PedidoResponse])
def listar_pedidos(db: Session = Depends(get_db)):
    """GET /pedidos — retorna a coleção de pedidos existentes (sem paginação nesta versão)."""
    service = PedidoService(db)
    return service.listar_pedidos()


@router.patch("/{pedido_id}/status", response_model=PedidoResponse)
def alterar_status(pedido_id: int, dados: PedidoStatusUpdate, db: Session = Depends(get_db)):
    """PATCH /pedidos/{id}/status — atualiza apenas o estado do pedido."""
    service = PedidoService(db)
    try:
        return service.alterar_status(pedido_id, dados.status)
    except PedidoNaoEncontrado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado")
