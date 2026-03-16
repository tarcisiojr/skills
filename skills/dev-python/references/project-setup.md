# Estrutura de Projeto Python Moderno

## Índice
1. [Layout src/](#layout-src)
2. [pyproject.toml Completo](#pyprojecttoml-completo)
3. [Ferramentas de Qualidade](#ferramentas-de-qualidade)
4. [Pre-commit Hooks](#pre-commit-hooks)
5. [Logging Estruturado](#logging-estruturado)
6. [Configuração e Variáveis de Ambiente](#configuração)
7. [Comandos de Validação](#comandos-de-validação)

---

## Layout src/

A estrutura `src/` é o padrão recomendado pelo Python Packaging Guide. Ela evita problemas de importação acidental do código-fonte durante testes.

```
meu-projeto/
├── src/
│   └── meu_projeto/
│       ├── __init__.py
│       ├── __main__.py          # Entry point: python -m meu_projeto
│       ├── cli.py               # Interface de linha de comando
│       ├── config.py            # Configuração centralizada
│       ├── exceptions.py        # Exceções customizadas do domínio
│       ├── models/              # Modelos de dados (dataclasses, Pydantic)
│       │   ├── __init__.py
│       │   ├── user.py
│       │   └── order.py
│       ├── services/            # Lógica de negócio
│       │   ├── __init__.py
│       │   ├── user_service.py
│       │   └── order_service.py
│       ├── repositories/        # Acesso a dados
│       │   ├── __init__.py
│       │   ├── base.py          # Protocol/ABC base
│       │   └── postgres.py
│       └── utils/               # Utilitários genéricos
│           ├── __init__.py
│           └── retry.py
├── tests/
│   ├── conftest.py              # Fixtures compartilhadas
│   ├── unit/
│   │   ├── test_user_service.py
│   │   └── test_order_service.py
│   └── integration/
│       └── test_api.py
├── pyproject.toml               # Configuração central do projeto
├── README.md
├── .pre-commit-config.yaml
├── .gitignore
└── .env.example                 # Template de variáveis de ambiente
```

**Por que src/ layout?**
- Impede que `import meu_projeto` funcione sem instalar o pacote
- Garante que os testes rodam contra o pacote instalado, não o código-fonte
- Compatível com `pip install -e .` (editable install) para desenvolvimento

---

## pyproject.toml Completo

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "meu-projeto"
version = "1.0.0"
description = "Descrição clara do projeto"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.11"
authors = [
    {name = "Seu Nome", email = "email@example.com"},
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Typing :: Typed",
]
dependencies = [
    "pydantic>=2.0",
    "httpx>=0.24",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=5.0",
    "pytest-asyncio>=0.23",
    "mypy>=1.8",
    "ruff>=0.4",
    "pre-commit>=3.6",
]

[project.scripts]
meu-cli = "meu_projeto.cli:main"

# ═══════════════════════════════════════════════════════════
# RUFF — Substitui flake8 + isort + black + pyupgrade
# ═══════════════════════════════════════════════════════════
[tool.ruff]
target-version = "py311"
line-length = 88
src = ["src", "tests"]

[tool.ruff.lint]
select = [
    "E",     # erros de estilo (pycodestyle)
    "W",     # avisos de estilo (pycodestyle)
    "F",     # erros lógicos (pyflakes)
    "I",     # ordenação de imports
    "B",     # detecção de bugs comuns
    "C4",    # otimização de comprehensions
    "UP",    # modernização automática de sintaxe
    "SIM",   # simplificação de código
    "TCH",   # otimiza imports para TYPE_CHECKING
    "RUF",   # regras específicas do ruff
    "PT",    # boas práticas pytest
    "RET",   # consistência de return statements
    "ARG",   # argumentos não utilizados
    "ERA",   # código comentado (dead code)
    "PERF",  # sugestões de performance
    "FURB",  # modernização de código (refurb)
]
ignore = [
    "E501",  # Line too long (ruff format cuida disso)
]

[tool.ruff.lint.isort]
known-first-party = ["meu_projeto"]

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["ARG"]  # Fixtures podem ter args não usados diretamente

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

# ═══════════════════════════════════════════════════════════
# MYPY — Type checking estático
# ═══════════════════════════════════════════════════════════
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

# ═══════════════════════════════════════════════════════════
# PYTEST — Testes
# ═══════════════════════════════════════════════════════════
[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
markers = [
    "slow: testes demorados (rodar separadamente)",
    "integration: testes de integração (requerem serviços externos)",
]
addopts = [
    "-ra",                       # Mostra resumo de falhas
    "-q",                        # Output conciso
    "--strict-markers",          # Erro se marker não registrado
    "--cov=src",                 # Cobertura do código fonte
    "--cov-report=term-missing", # Mostra linhas não cobertas
    "--cov-fail-under=90",       # Mínimo 90% de cobertura
]

# ═══════════════════════════════════════════════════════════
# COVERAGE — Cobertura de testes
# ═══════════════════════════════════════════════════════════
[tool.coverage.run]
source = ["src"]
omit = ["tests/*", "**/__main__.py"]

[tool.coverage.report]
fail_under = 90
show_missing = true
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.",
    "@overload",
]
```

---

## Ferramentas de Qualidade

### Ruff — O Canivete Suíço

Ruff unifica lint e formatação num único binário Rust — 10-100x mais rápido que a stack anterior (flake8 + isort + black + pyupgrade).

```bash
# Lint (verificar + corrigir automaticamente)
ruff check . --fix

# Formatação
ruff format .

# Verificar sem corrigir
ruff check .

# Mostrar regras disponíveis
ruff rule E501
```

### Mypy — Type Checking

```bash
# Verificação estrita
mypy . --strict

# Verificar arquivo específico
mypy src/meu_projeto/services/user_service.py

# Gerar relatório HTML
mypy . --html-report reports/mypy
```

### uv — Gerenciamento de Dependências

uv é o substituto moderno para pip, poetry e venv. Escrito em Rust, extremamente rápido.

```bash
# Criar projeto novo
uv init meu-projeto

# Criar e ativar virtual environment
uv venv
source .venv/bin/activate

# Instalar dependências
uv pip install -e ".[dev]"

# Adicionar dependência
uv add httpx
uv add --dev pytest

# Sincronizar dependências (equivalente ao poetry install)
uv sync

# Rodar script sem instalar
uv run python script.py

# Lock de dependências
uv lock
```

---

## Pre-commit Hooks

`.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies:
          - pydantic>=2.0

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-yaml
      - id: check-toml
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: check-added-large-files
        args: [--maxkb=500]
      - id: detect-private-key
```

```bash
# Instalar hooks
pre-commit install

# Rodar em todos os arquivos
pre-commit run --all-files
```

---

## Logging Estruturado

Para aplicações modernas, prefira structlog sobre o módulo logging padrão. Produz logs estruturados (JSON) que são pesquisáveis em ferramentas como Datadog, ELK, CloudWatch.

```python
# ═══════════════════════════════════════════════════════════
# RECOMENDADO: structlog — logging estruturado moderno
# ═══════════════════════════════════════════════════════════
import structlog

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.ConsoleRenderer()          # Dev: output colorido
        # structlog.processors.JSONRenderer()    # Prod: JSON para ferramentas
    ],
)

# Em cada módulo
log = structlog.get_logger()

# Uso — dados estruturados, não strings formatadas
log.info("pedido_processado", order_id=123, total=99.90, moeda="BRL")
# 2026-03-16T14:30:00Z [info] pedido_processado  order_id=123 total=99.9 moeda=BRL

log.error("falha_conexao", servico="api-pagamento", tentativa=3, exc_info=True)

# ═══════════════════════════════════════════════════════════
# ALTERNATIVA: logging stdlib (quando não pode adicionar dependências)
# ═══════════════════════════════════════════════════════════
import logging

logger = logging.getLogger(__name__)

# Use f-strings ou mensagens diretas — NÃO use %s/%d (estilo legado)
logger.info(f"Processando pedido {order_id}")
logger.error(f"Falha ao conectar com {service}: {error}", exc_info=True)
```

---

## Configuração

```python
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """Configuração da aplicação via variáveis de ambiente."""
    # Banco de dados
    database_url: str = Field(
        default="postgresql://localhost/mydb",
        description="URL de conexão com o banco de dados",
    )

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8080
    debug: bool = False

    # Segurança
    secret_key: str = Field(..., description="Chave secreta para JWT")
    allowed_origins: list[str] = ["http://localhost:3000"]

    # Caminhos
    log_dir: Path = Path("logs")
    upload_dir: Path = Path("uploads")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }

# Singleton
_settings: Settings | None = None

def get_settings() -> Settings:
    """Retorna instância única de configuração."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
```

`.env.example`:
```bash
# Banco de dados
DATABASE_URL=postgresql://user:pass@localhost:5432/mydb

# API
API_HOST=0.0.0.0
API_PORT=8080
DEBUG=false

# Segurança
SECRET_KEY=trocar-em-producao
ALLOWED_ORIGINS=["http://localhost:3000"]
```

---

## Comandos de Validação

Pipeline completa que deve ser executada antes de finalizar qualquer tarefa:

```bash
# Pipeline padrão
ruff check . --fix && ruff format . && mypy . --strict && pytest --cov

# Com uv (sem ativar venv)
uv run ruff check . --fix && uv run ruff format . && uv run mypy . --strict && uv run pytest --cov
```

**Critério de conclusão:**
1. Zero erros de lint (ruff check)
2. Formatação aplicada (ruff format)
3. Zero erros de tipo (mypy --strict)
4. Todos os testes passando
5. Cobertura >= 90%
6. Arquivos temporários removidos
7. `git status` mostra apenas mudanças intencionais
