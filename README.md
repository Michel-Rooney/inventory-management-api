# 📦 Inventory Management API

API REST para gerenciamento de estoque, desenvolvida com **Django** e **Django REST Framework**. Permite que empresas cadastrem produtos, registrem vendas, monitorem alertas de estoque e visualizem dados de desempenho em um dashboard analítico.

---

## 🚀 Tecnologias

| Tecnologia | Versão |
|---|---|
| Python | 3.x |
| Django | 4.2.7 |
| Django REST Framework | 3.14.0 |
| SimpleJWT | 5.3.0 |
| PostgreSQL | via psycopg2 |
| Gunicorn | 21.2.0 |
| WhiteNoise | 6.6.0 |
| django-cors-headers | 4.3.1 |
| pytest / pytest-django | 7.4.4 / 4.7.0 |

---

## 🗂️ Estrutura do Projeto

```
inventory-management-api/
├── core/                   # Configurações principais (settings, urls, wsgi/asgi)
├── apps/
│   ├── user/               # Autenticação e gerenciamento de usuários
│   ├── product/            # Produtos, logs e alertas de estoque
│   ├── purchase/           # Registro de vendas e dashboard
│   └── utils/              # Permissões, queries e utilitários compartilhados
├── manage.py
├── requirements.txt
├── build.sh                # Script de build para deploy
└── .env-example            # Exemplo de variáveis de ambiente
```

---

## ⚙️ Configuração do Ambiente

### 1. Clone o repositório

```bash
git clone https://github.com/Michel-Rooney/inventory-management-api.git
cd inventory-management-api
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Copie o arquivo `.env-example` para `.env` e preencha os valores:

```bash
cp .env-example .env
```

```env
SECRET_KEY=sua-chave-secreta-django
SECRET_KEY_JWT=sua-chave-secreta-jwt
DEBUG=1

ALLOWED_HOSTS=127.0.0.1
CSRF_TRUSTED_ORIGINS=http://127.0.0.1:8000
CORS_ALLOWED_ORIGINS=http://127.0.0.1:3000

# Banco de dados
ALLOWED_DATABASE=postgresql
ENGINE_DB=django.db.backends.postgresql
NAME=nome_do_banco
USER=usuario
PASSWORD=senha
HOST=localhost
PORT=5432
```

### 5. Execute as migrações

```bash
python manage.py migrate
```

### 6. Inicie o servidor

```bash
python manage.py runserver
```

---

## 🔑 Autenticação

A API utiliza **JWT (JSON Web Token)** via `djangorestframework-simplejwt`. Todas as rotas protegidas exigem o token no header `Authorization: Bearer <token>`.

| Endpoint | Método | Descrição |
|---|---|---|
| `/api/token/` | POST | Obter access + refresh token |
| `/api/token/refresh/` | POST | Renovar o access token |
| `/api/token/verify/` | POST | Verificar validade do token |

---

## 📡 Endpoints

### 👤 Usuário — `/api/user/`

| Método | URL | Descrição | Auth |
|---|---|---|---|
| POST | `/api/user/` | Criar novo usuário | ❌ |
| GET | `/api/user/` | Retorna os dados do usuário autenticado | ✅ |
| PATCH | `/api/user/{id}/` | Atualizar dados do usuário | ✅ |
| DELETE | `/api/user/{id}/` | Deletar conta | ✅ |

---

### 📦 Produtos — `/api/products/`

| Método | URL | Descrição | Auth |
|---|---|---|---|
| GET | `/api/products/` | Listar produtos da empresa | ✅ |
| POST | `/api/products/` | Criar produto | ✅ |
| GET | `/api/products/{id}/` | Detalhar produto | ✅ |
| PATCH | `/api/products/{id}/` | Atualizar produto | ✅ |
| DELETE | `/api/products/{id}/` | Deletar produto | ✅ |
| GET | `/api/products/alert_products/` | Alertas de estoque e validade | ✅ |

**Filtros disponíveis:**

- Busca por nome, descrição ou marca: `?search=termo`

**Campos do produto:**

| Campo | Tipo | Descrição |
|---|---|---|
| `name` | string | Nome único do produto |
| `description` | string | Descrição |
| `brand` | string | Marca |
| `quantity` | int | Quantidade em estoque (≥ 0) |
| `purchase_price` | float | Preço de compra |
| `sale_price` | float | Preço de venda |
| `expiration` | date | Data de validade (opcional) |

---

### 🚨 Alertas de Estoque (`/api/products/alert_products/`)

Retorna produtos categorizados por nível de urgência:

| Status | Critério |
|---|---|
| `quantity_red` | Quantidade entre 0 e 2 unidades |
| `quantity_yellow` | Quantidade entre 3 e 5 unidades |
| `date_red` | Validade vencida ou em menos de 3 dias |
| `date_yellow` | Validade entre 3 e 10 dias |

---

### 🛒 Compras — `/api/purchase/`

| Método | URL | Descrição | Auth |
|---|---|---|---|
| POST | `/api/purchase/` | Registrar nova venda | ✅ |
| GET | `/api/purchase/dashboard_data/` | Dados para dashboard analítico | ✅ |

**Dashboard (`?type=week|month|year`):**

Retorna dados de vendas agrupados por período:

```json
{
  "labels": ["Segunda", "Terça", "..."],
  "values": [150.0, 200.0, "..."],
  "total_price": 1500.0,
  "gain": 300.0,
  "data": [{ "date": "10/03/2024", "total_price": 150.0, "gain": 30.0 }],
  "biggest_sale": { "data": "2024-03-15", "value": 500.0 },
  "most_sold_product": { "name": "Produto X", "total_sale": 750.0 }
}
```

---

### 📋 Log de Produtos — `/api/product-log/`

Histórico de produtos associados às vendas realizadas.

| Método | URL | Descrição | Auth |
|---|---|---|---|
| GET | `/api/product-log/` | Listar logs | ✅ |
| GET | `/api/product-log/{id}/` | Detalhar log | ✅ |

---

## 🧪 Testes

O projeto utiliza **pytest** com **pytest-django** e possui cobertura de testes para autenticação, CRUD de produtos, criação de compras e validações.

```bash
# Rodar todos os testes
pytest

# Com cobertura de código
coverage run -m pytest
coverage report
```

---

## 🚢 Deploy

O projeto inclui um script `build.sh` para deploy em plataformas como Render:

```bash
./build.sh
```

Esse script executa automaticamente:
1. `pip install -r requirements.txt`
2. `python manage.py collectstatic --no-input`
3. `python manage.py migrate`

Para servir em produção, utilize o Gunicorn:

```bash
gunicorn core.wsgi:application
```

---

## 🔐 Permissões

- **`IsOwner`** — o usuário só pode acessar e modificar seus próprios dados.
- **`IsOwnerProduct`** — o usuário só pode visualizar e gerenciar produtos vinculados à sua empresa (conta).

---

## 📝 Licença

Este projeto é de uso pessoal. Sinta-se livre para usar e adaptar conforme sua necessidade.
