FastAPI Application

Este é um projeto FastAPI com PostgreSQL, Redis cache e logging.

Estrutura do Projeto

```
├── app/

│ ├── api/

│ │ ├── endpoints/

│ │ │ └── base.py

│ │ └── router.py

│ ├── models/

│ │ └── base.py

│ ├── schemas/

│ │ └── base.py

│ ├── utils/

│ │ ├── cache.py

│ │ └── logger.py

│ ├── database.py

│ ├── main.py

│ └── cache.py

├── alembic/

│ ├── versions/

│ └── env.py

├── tests/

├── .env

├── alembic.ini

├── requirements.txt

└── README.md
```

Configuração
Clone o repositório
Crie um ambiente virtual: `python3 -m venv venv`
Ative o ambiente virtual:
Windows: `venv\Scripts\activate`
Unix ou MacOS: `source venv/bin/activate`
Instale as dependências: `pip install -r requirements.txt`
Configure as variáveis de ambiente no arquivo .env

Migrações com Alembic

Para gerenciar as migrações do banco de dados, usamos Alembic.

Inicializar Alembic (apenas na primeira vez)

alembic init alembic

Criar uma nova migração

`alembic revision --autogenerate -m "Descrição da migração"`

Aplicar migrações

`alembic upgrade head`

Reverter migrações

`alembic downgrade -1`

Logging

O logging é configurado em app/utils/logger.py. Para usar o logger em qualquer parte do código:

Python
Copiar

```
from app.utils.logger import log_info, log_error

log_info("Esta é uma mensagem de informação")
log_error("Esta é uma mensagem de erro")
```

Para logs assíncronos:

Python
Copiar

```
from app.utils.logger import async_info, async_error

await async_info("Esta é uma mensagem de informação assíncrona")
await async_error("Esta é uma mensagem de erro assíncrona")
```

Cache

O cache Redis é configurado em app/utils/cache.py. Para usar o cache em endpoints:

Python
Copiar

```
from app.utils.cache import custom_cache

@router.get("/items")
@custom_cache(expire=30)
async def read_items(): # Sua lógica aqui
```

Adicionando Novas Pastas

Se você precisar adicionar novas pastas ao projeto:

Crie a nova pasta dentro do diretório app/
Se a pasta contiver módulos Python, adicione um arquivo **init**.py vazio
Importe os módulos relevantes em app/**init**.py ou onde forem necessários

Exemplo para adicionar uma nova pasta services:

```
mkdir app/services

touch app/services/init.py
```

Então, você pode adicionar módulos Python dentro de app/services/ conforme necessário.

Executando o Projeto

Para executar o projeto:

```
uvicorn app.main:app --reload
```

A API estará disponível em http://localhost:8000.

A documentação Swagger UI estará disponível em http://localhost:8000/docs.

Testes

Para executar os testes:

```
pytest
```
