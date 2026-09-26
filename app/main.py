from fastapi import FastAPI

from app.api import pedidos
from app.database import Base, engine

# Cria as tabelas no banco caso ainda não existam.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Pedidos",
    description="Projeto incremental — Desenvolvimento de Sistemas Distribuídos",
    version="1.0.0",
)

app.include_router(pedidos.router)


@app.get("/health", tags=["saude"])
def health():
    """Endpoint de saúde — não representa funcionalidade de negócio."""
    return {"status": "ok"}
