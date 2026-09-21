API backend desenvolvida em Python utilizando FastAPI para a gestão completa de um sistema de delivery, contemplando autenticação JWT segura, gestão de utilizadores, criação e controlo de pedidos, bem como itens e migrações de base de dados.

🛠️ Tecnologias Utilizadas
Python
FastAPI
SQLAlchemy (ORM para mapeamento objeto-relacional)
Alembic 
SQLite (Base de dados local)
Pydantic (Validação de dados)
python-jose & Passlib (Autenticação JWT e hash de passwords com bcrypt)

📂 Estrutura do Projeto

'''Delivery/
├── server/
│   ├── alembic/                # Migrações da base de dados
│   ├── app/                    # Código-fonte principal da aplicação
│   │   ├── router/             # Rotas da API
│   │   │   ├── auth.py         # Rotas de autenticação e registo
│   │   │   └── order.py        # Rotas de gestão de pedidos e itens
│   │   ├── banco.db            # Base de dados SQLite local
│   │   ├── dependencies.py     # Dependências e injeção de sessão/token
│   │   ├── main.py             # Ponto de entrada da aplicação FastAPI
│   │   ├── models.py           # Modelos SQLAlchemy (User, Order, OrderItem)
│   │   └── schemas.py          # Schemas Pydantic para validação de entrada
│   ├── alembic.ini             # Configuração do Alembic
│   └── .env                    # Variáveis de ambiente (não versionado)
├── .gitignore                  # Ficheiros ignorados pelo Git
└── requirements.txt            # Dependências do projeto'''

Endpoints Principais da API
🔐 Autenticação (/auth)
POST /auth/create — Registo de novos utilizadores (validação de email e telefone únicos).
POST /auth/login — Autenticação e retorno de access_token e refresh_token.
GET /auth/refresh — Atualização do token de acesso utilizando o refresh token.

📦 Pedidos (/orders) (Requer Autenticação)
POST /orders/order — Criação de um novo pedido.
POST /orders/order/add/{id_order} — Adiciona um item (com quantidade, sabor, tamanho e preço) ao pedido.
POST /orders/order/remove/{id_item_order} — Remove um item específico do pedido.
POST /orders/order/cancel/{id_order} — Cancela um pedido existente.
POST /orders/order/finished/{id_order} — Finaliza/conclui um pedido.
GET /orders/list — Lista todos os pedidos (restrito a administradores).
