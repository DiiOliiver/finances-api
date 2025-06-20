# Finances API

API para gerenciamento financeiro desenvolvida em **Python** com **FastAPI** e arquitetura **Clean Architecture**, utilizando **MongoDB** e **Redis**. O projeto adota boas práticas de organização, validação e automação de processos de desenvolvimento.

---

## Estrutura do Projeto

A estrutura do projeto foi organizada para respeitar o Clean Architecture, com separação clara de responsabilidades, além de recursos auxiliares para padronização e automação:

```
finances-api/
├── .hooks/
│   └── check_branch_name.py           # Script para validar nome de branch
├── src/
│   ├── application/                   # Casos de uso e serviços da aplicação
│   ├── domain/                        # Entidades e contratos do domínio
│   ├── infra/                         # Implementações externas (ex: bancos, API)
│   └── __init__.py
├── tests/                             # Testes automatizados
├── .coverage
├── .env
├── .env-example
├── .gitignore
├── .importlinter                      # Configuração do Import Linter para garantir Clean Arch
├── .pre-commit-config.yaml            # Hooks automatizados de pré-commit
├── .python-version
├── docker-compose.yml                 # Orquestração de MongoDB e Redis
├── main.py                            # Ponto de entrada da aplicação
├── poetry.lock
├── pyproject.toml                     # Configuração e dependências do projeto
└── README.md
```

## Principais Funcionalidades

- **API RESTful** com FastAPI para gerenciamento de receitas, despesas, categorias e usuários.
- **Validação de dados** com Pydantic.
- **Injeção de dependências** com Dependency Injector.
- **Paginação** de resultados.
- **Envio de e-mails** (via aiosmtplib).
- **Cache** com Redis.
- **Testes automatizados** com pytest e pytest-cov.
- **Padronização de imports** e arquitetura com Import Linter.
- **Automação de boas práticas** com pre-commit (lint, testes, validação de branch, importlinter).

## Instalação e Configuração

### Requisitos

- Python >= 3.13
- [Poetry](https://python-poetry.org/)
- Docker e Docker Compose

### Passos

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/finances-api.git
   cd finances-api
   ```

2. **Copie e configure variáveis de ambiente**
   ```bash
   cp .env-example .env
   # Edite o arquivo .env conforme necessário
   ```

3. **Suba os serviços do banco e cache**
   ```bash
   docker-compose up -d
   ```

4. **Habilitar o ambiente virtual, para que o python consiga enxergar dependências instaladas**
   ```bash
   poetry shell
   ```

5. **Instale as dependências do Python**
   ```bash
   poetry install
   ```

6. **Execute a aplicação**
   ```bash
   task run
   ```

7. **Acesse a API**
   - Padrão: http://localhost:8000

8. **Execute os testes**
   ```bash
   poetry run pytest
   ```

### Automatizações e Boas Práticas

- **Pre-commit**: Antes de cada commit, são executados:
  - `ruff` (lint/fix de código)
  - `pytest` (testes automatizados)
  - `check-arch` (validação da arquitetura via importlinter)
  - `check-branch-name` (validação de nome de branch via regex)
- **Import Linter**: Garante que não haja violações na arquitetura do projeto.
- **Taskipy**: Atalhos para comandos comuns, como lint, teste e execução do app.

## Dependências Principais (pyproject.toml)

- `fastapi[standard]` - API web
- `pydantic-settings` - Configuração e validação
- `aiosmtplib` e `email-validator` - E-mails
- `redis` - Cache
- `dependency-injector` - Injeção de dependências
- `jwt` / `pyjwt` - Autenticação
- `fastapi-pagination` - Paginação
- **Dev:** `pytest`, `pytest-cov`, `taskipy`, `ruff`, `import-linter`, `pre-commit`

---