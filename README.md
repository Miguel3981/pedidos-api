# API de Pedidos

Projeto incremental da disciplina **Desenvolvimento de Sistemas Distribuídos** — Trabalho 1.

## Integrantes

| Nome completo | Turma | RA |
|---|---|---|
| _Miguel_Cardoso_de_Jesus_| _(preencher)_ | _(preencher)_ |
| _(preencher)_ | _(preencher)_ | _(preencher)_ |
| _(preencher)_ | _(preencher)_ | _(preencher)_ |
| _(preencher)_ | _(preencher)_ | _(preencher)_ |

## Arquitetura

- **Cliente → API de Pedidos → PostgreSQL**
- A aplicação (FastAPI) e o banco (PostgreSQL) executam em containers separados, comunicando-se por uma rede interna do Docker.
- Camadas internas da aplicação:
  - `app/api` — Controller: recebe requisições HTTP e produz respostas.
  - `app/services` — Service: lógica de negócio (cálculo de `valor_total`, definição de status inicial, regras de transição de estado).
  - `app/repositories` — Repository: abstrai o acesso ao banco de dados.
  - `app/models` — modelo persistente (SQLAlchemy).
  - `app/schemas` — modelos de entrada/saída da API (Pydantic).
  - `app/database.py` — configuração da conexão, lida via variável de ambiente `DATABASE_URL`.

## Modelo de Pedido

| Campo | Descrição |
|---|---|
| `id` | Identificador do pedido |
| `cliente` | Identificação textual do cliente |
| `produto` | Identificação textual do produto |
| `quantidade` | Quantidade solicitada |
| `valor_unitario` | Preço de uma unidade |
| `valor_total` | Calculado pela aplicação (`quantidade * valor_unitario`) |
| `status` | `CRIADO`, `CONFIRMADO` ou `CANCELADO` |
| `data_criacao` | Instante em que o pedido foi registrado |

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/pedidos` | Cria um pedido. Entrada: `cliente`, `produto`, `quantidade`, `valor_unitario`. Retorna `201 Created`. |
| `GET` | `/pedidos/{id}` | Consulta um pedido. Retorna `200 OK` ou `404 Not Found`. |
| `GET` | `/pedidos` | Lista todos os pedidos existentes (sem paginação nesta versão). |
| `PATCH` | `/pedidos/{id}/status` | Altera o status de um pedido existente. |
| `GET` | `/health` | Verificação de disponibilidade. Retorna `{"status": "ok"}`. |

Documentação interativa (Swagger) disponível em `http://localhost:8000/docs` após subir a aplicação.

## Como executar

Pré-requisitos: [Docker](https://www.docker.com/) e Docker Compose instalados.

```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_REPOSITORIO>
git checkout APIPedidos-1-final
docker compose up -d --build
```

A API ficará disponível em `http://localhost:8000`.

Serviços definidos no `docker-compose.yml`:
- `pedidos` — aplicação FastAPI (porta `8000`).
- `postgres` — banco de dados PostgreSQL (dados persistidos em volume Docker).

Variáveis de ambiente utilizadas pela aplicação estão documentadas em `.env.example`. Ao usar `docker compose up`, elas já são definidas automaticamente pelo próprio `docker-compose.yml` — não é necessário nenhum passo manual adicional.

## Persistência

Os dados dos pedidos são armazenados em um volume Docker (`pedidos_data`), portanto sobrevivem a reinícios do container da aplicação. Apenas `docker compose down -v` remove os dados definitivamente.

## Estados do pedido

- `CRIADO` — pedido registrado (estado inicial).
- `CONFIRMADO` — pedido confirmado pela aplicação.
- `CANCELADO` — pedido cancelado.

Novos estados poderão surgir em versões futuras, quando Estoque e Pagamento forem distribuídos como serviços independentes.
