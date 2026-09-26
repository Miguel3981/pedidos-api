import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# A aplicação recebe sua configuração do ambiente (DATABASE_URL).
# Endereço, porta, usuário e senha do banco não ficam fixos no código.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://pedidos:pedidos@postgres:5432/pedidos",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Fornece uma sessão de banco por requisição (dependency do FastAPI)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
