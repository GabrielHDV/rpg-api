# ⚔️ RPG de Mesa API

API REST para gerenciamento de campanhas e personagens de RPG de Mesa, desenvolvida com Python + FastAPI.

---

# 📖 Tema escolhido

Uma plataforma onde **mestres (admins)** criam e gerenciam campanhas de RPG, enquanto **jogadores (players)** criam personagens e participam dessas campanhas.

O tema foi escolhido por ser criativo, possuir regras de negócio claras e permitir implementar naturalmente autenticação, permissões, CRUD completo, upload de arquivos e testes automatizados.

---

# 🛠️ Tecnologias utilizadas

| Tecnologia | Versão | Motivo |
|---|---|---|
| FastAPI | 0.111.0 | Framework moderno, rápido e com documentação automática |
| PostgreSQL | 15 | Banco relacional robusto e gratuito |
| SQLAlchemy | 2.0.30 | ORM padrão do Python |
| Pydantic | 2.7.1 | Validação de dados |
| python-jose | 3.3.0 | Geração e validação de JWT |
| passlib + bcrypt | 1.7.4 | Hash seguro de senhas |
| Docker + Docker Compose | - | Containerização da aplicação |
| python-dotenv | 1.0.1 | Variáveis de ambiente |
| fastapi-mail | 1.4.1 | Envio de emails |
| cloudinary | 1.36.0 | Upload de imagens |
| pytest | 8.2.0 | Testes automatizados |

---

# 🗄️ Entidades e relacionamentos

```text
+---------+        1:N        +-------------+      N:0..1      +------------+
|  users  |------------------>| characters  |----------------->| campaigns |
+---------+                   +-------------+                  +------------+
```

- Um **user** pode possuir vários **characters**
- Uma **campaign** pode conter vários **characters**
- Um **character** pertence obrigatoriamente a um **user**
- Um **character** pode pertencer opcionalmente a uma **campaign**

---

# 🔐 Autenticação

O sistema utiliza **JWT (JSON Web Token)** para autenticação.

## Fluxo de autenticação

1. Usuário se registra em:

```http
POST /auth/register
```

2. Usuário realiza login em:

```http
POST /auth/login
```

3. A API retorna um token JWT

4. O token deve ser enviado no header:

```http
Authorization: Bearer <token>
```

---

## 👥 Níveis de acesso

| Role | Permissões |
|---|---|
| **admin** | Gerencia campanhas, usuários e todos os personagens |
| **player** | Cria e gerencia apenas seus personagens |

---

# 📡 Endpoints

## 🔑 Autenticação

| Método | Rota | Descrição | Acesso |
|---|---|---|---|
| POST | `/auth/register` | Registra novo usuário | Público |
| POST | `/auth/login` | Realiza login e retorna JWT | Público |

---

## 👤 Usuários

| Método | Rota | Descrição | Acesso |
|---|---|---|---|
| GET | `/users/` | Lista todos os usuários | Admin |
| GET | `/users/me` | Retorna usuário autenticado | Autenticado |
| GET | `/users/{id}` | Busca usuário por ID | Admin |
| PUT | `/users/me` | Atualiza perfil próprio | Autenticado |
| DELETE | `/users/{id}` | Remove usuário | Admin |

---

## 🏰 Campanhas

| Método | Rota | Descrição | Acesso |
|---|---|---|---|
| POST | `/campaigns/` | Cria campanha | Admin |
| GET | `/campaigns/` | Lista campanhas | Autenticado |
| GET | `/campaigns/{id}` | Busca campanha por ID | Autenticado |
| PUT | `/campaigns/{id}` | Atualiza campanha | Admin (criador) |
| DELETE | `/campaigns/{id}` | Remove campanha | Admin (criador) |

---

## 🧙 Personagens

| Método | Rota | Descrição | Acesso |
|---|---|---|---|
| POST | `/characters/` | Cria personagem | Autenticado |
| GET | `/characters/` | Lista personagens do usuário | Autenticado |
| GET | `/characters/all` | Lista todos os personagens | Admin |
| GET | `/characters/{id}` | Busca personagem por ID | Autenticado |
| PUT | `/characters/{id}` | Atualiza personagem | Dono/Admin |
| DELETE | `/characters/{id}` | Remove personagem | Dono/Admin |
| POST | `/characters/{id}/upload-imagem` | Upload da imagem do personagem | Dono/Admin |

---

# 🚀 Como executar o projeto

## 📋 Pré-requisitos

- Docker instalado
- Docker Compose instalado

---

## 1. Clone o repositório

```bash
git clone https://github.com/GabrielHDV/rpg-api.git
cd rpg-api
```

---

## 2. Crie o arquivo `.env`

```bash
cp .env.example .env
```

---

## 3. Configure as variáveis de ambiente

```env
DATABASE_URL=postgresql://rpg_user:rpg_password@db:5432/rpg_db

SECRET_KEY=sua-chave-secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

MAIL_HOST=sandbox.smtp.mailtrap.io
MAIL_PORT=587
MAIL_USERNAME=seu-usuario-mailtrap
MAIL_PASSWORD=sua-senha-mailtrap
MAIL_FROM=noreply@rpgapi.com

CLOUDINARY_CLOUD_NAME=seu-cloud-name
CLOUDINARY_API_KEY=sua-api-key
CLOUDINARY_API_SECRET=seu-api-secret
```

---

## 4. Suba os containers

```bash
docker compose up --build
```

---

## 5. Acesse a documentação Swagger

```text
http://localhost:8000/docs
```

---

## 6. Execute os testes

```bash
docker compose exec api pytest tests/ -v
```

---

# 📋 Regras de negócio

- Apenas admins podem criar campanhas
- Personagens só podem entrar em campanhas com status `recruiting`
- Campanhas cheias não aceitam novos personagens
- Usuários comuns só podem editar seus próprios personagens
- Apenas o admin criador pode editar/remover campanhas
- Senhas são armazenadas usando hash bcrypt
- Email de boas-vindas é enviado no registro
- Upload de imagens integrado ao Cloudinary

---

# 🧪 Testes automatizados

O projeto possui **20 testes automatizados** cobrindo:

- Registro de usuários
- Login/autenticação JWT
- Permissões por role
- CRUD de campanhas
- CRUD de personagens
- Regras de negócio
- Upload de imagens

---

# 📂 Estrutura do projeto

```text
rpg-api/
├── app/
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── dependencies.py    # Dependências de autenticação e usuário logado
│   │   └── security.py        # JWT, hash de senha e regras de segurança
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py            # Model da entidade User
│   │   ├── campaign.py        # Model da entidade Campaign
│   │   └── character.py       # Model da entidade Character
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py            # Rotas de registro e login
│   │   ├── users.py           # Rotas de usuários
│   │   ├── campaigns.py       # Rotas de campanhas
│   │   └── characters.py      # Rotas de personagens e upload de imagem
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py            # Schemas Pydantic de usuários
│   │   ├── campaign.py        # Schemas Pydantic de campanhas
│   │   └── character.py       # Schemas Pydantic de personagens
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── cloudinary.py      # Serviço de upload de imagens no Cloudinary
│   │   └── email.py           # Serviço de envio de email
│   │
│   ├── __init__.py
│   ├── database.py            # Configuração do banco e sessão SQLAlchemy
│   └── main.py                # Arquivo principal da aplicação FastAPI
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Configurações e fixtures dos testes
│   ├── test_auth.py           # Testes de autenticação
│   ├── test_campaigns.py      # Testes de campanhas
│   └── test_characters.py     # Testes de personagens
│
├── Dockerfile                 # Imagem Docker da API
├── docker-compose.yml         # Configuração dos containers
├── requirements.txt           # Dependências do projeto
├── .env                       # Variáveis de ambiente locais
├── .gitignore
└── test.db                    # Banco SQLite usado em testes/local
```

---

# 🔮 Melhorias futuras

- Sistema de convites para campanhas
- Paginação
- Refresh Token
- Chat em tempo real com WebSocket
- Sistema de inventário
- Logs administrativos
- Filtros por raça, classe e status
- Sistema de experiência e níveis

---

