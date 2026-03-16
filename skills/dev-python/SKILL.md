---
name: dev-python
description: >
  Skill completa para desenvolvimento Python com boas práticas, estilo Pythônico
  e padrões reconhecidos pelo mercado. Baseada em Fluent Python (Ramalho),
  Effective Python (Slatkin), Raymond Hettinger, PEPs oficiais e ferramentas
  modernas (ruff, mypy, pytest, uv). Use esta skill SEMPRE que o usuário estiver
  trabalhando com código Python — seja criando novos projetos, refatorando,
  debugando, escrevendo testes, ou pedindo revisão de código. Acione também
  quando o usuário mencionar: Python, .py, pip, venv, pytest, FastAPI, Django,
  Flask, SQLAlchemy, Pydantic, type hints, async/await em Python, ou qualquer
  framework/biblioteca Python. Se houver um pyproject.toml, setup.py, ou
  requirements.txt no projeto, esta skill é relevante.
---

# Dev Python — Desenvolvimento Pythônico com Boas Práticas

## Filosofia Central

O Zen of Python (PEP 20) guia todas as decisões. Os princípios mais impactantes no dia a dia:

- **Explícito é melhor que implícito** — type hints, argumentos nomeados, erros claros
- **Simples é melhor que complexo** — a solução mais simples que funciona é a melhor
- **Legibilidade conta** — código é lido muito mais vezes do que escrito
- **Deve haver uma — e preferencialmente só uma — maneira óbvia de fazer**
- **Erros nunca devem passar silenciosamente** — trate exceções explicitamente

> "Não escreva código difícil de entender para parecer inteligente. Escreva código tão claro que pareça óbvio." — Raymond Hettinger

## Quando Consultar as Referências

Este arquivo contém as regras e princípios essenciais. Para exemplos detalhados com código:

| Preciso de...                                    | Consultar                              |
|--------------------------------------------------|----------------------------------------|
| Idiomas Pythônicos, padrões e anti-padrões       | `references/pythonic-patterns.md`      |
| Python moderno (3.10+), type hints, async        | `references/modern-python.md`          |
| Estrutura de projeto, ferramentas, pyproject.toml| `references/project-setup.md`          |

Leia a referência relevante quando precisar de exemplos de código ou detalhes específicos.

---

## Regras de Ouro

### 1. Estilo Pythônico (PEP 8 + Beyond PEP 8)

PEP 8 é o ponto de partida, mas como Raymond Hettinger ensina em "Beyond PEP 8", o verdadeiro objetivo é **clareza e legibilidade**, não conformidade cega com regras.

**Nomeação — a decisão de design mais importante:**
- `snake_case` para funções, variáveis e módulos
- `PascalCase` para classes
- `UPPER_SNAKE_CASE` para constantes de módulo
- `_prefixo` para indicar uso interno (convenção, não proteção)
- Nomes descritivos que revelam intenção — `calculate_total_price`, não `calc`

**Funções:**
- Pequenas e focadas (máximo 25-30 linhas)
- Um nível de abstração por função
- Use `*` para forçar argumentos nomeados quando há risco de confusão
- Prefira retornos explícitos a efeitos colaterais

**Imports:**
- Agrupe: stdlib → terceiros → locais (com linha em branco entre grupos)
- Use ruff para ordenação automática (regra `I` substitui isort)
- Prefira imports absolutos; imports relativos só dentro do mesmo pacote

### 2. Type Hints São Obrigatórios

Type hints não são decoração — são documentação executável que previne bugs antes do runtime.

```python
# Assinaturas de função SEMPRE tipadas
def buscar_usuario(user_id: int, *, incluir_inativos: bool = False) -> User | None:
    ...

# Variáveis com tipo não óbvio
resultados: list[dict[str, Any]] = []

# Genéricos modernos (Python 3.12+)
type Matrix[T] = list[list[T]]
```

**Regras:**
- Toda função pública tem type hints nos parâmetros E no retorno
- Use `Protocol` para duck typing tipado (não ABC quando possível)
- Use `TypedDict` para dicts com estrutura conhecida (ex: JSON de API)
- Use `| None` em vez de `Optional[X]` (Python 3.10+)
- Execute `mypy --strict` ou `pyright` regularmente

### 3. Tratamento de Erros

Python segue a filosofia EAFP (Easier to Ask Forgiveness than Permission) — tente fazer e trate a exceção se falhar, em vez de verificar condições antes.

**Regras invioláveis:**
- NUNCA use `except:` ou `except Exception:` sem re-raise — isso engole erros silenciosamente
- Crie hierarquia de exceções customizadas para o domínio da aplicação
- Use `from e` ao encadear exceções para preservar o traceback
- Use `from None` apenas para ocultar detalhes sensíveis (ex: segurança)
- Blocos `try` devem ser pequenos — apenas o código que pode falhar

```python
# Hierarquia de exceções do domínio
class AppError(Exception):
    """Exceção base da aplicação."""

class NotFoundError(AppError):
    """Recurso não encontrado."""

class ValidationError(AppError):
    """Dados de entrada inválidos."""

# Encadeamento correto
try:
    response = client.get(url)
except ConnectionError as e:
    raise ExternalServiceError(f"Falha ao conectar: {url}") from e
```

### 4. Estruturas de Dados — Use a Mais Simples

| Caso de Uso                     | Escolha        | Porquê                              |
|---------------------------------|----------------|--------------------------------------|
| Modelos internos                | `@dataclass`   | Leve, rápido, Pythônico              |
| Dados imutáveis simples         | `NamedTuple`   | Performance máxima, desempacotável   |
| Validação de input/API          | Pydantic        | Validação rica em runtime            |
| Dict tipado (JSON externo)      | `TypedDict`    | Checagem estática sem overhead       |

Use `@dataclass(slots=True)` para performance e `frozen=True` para imutabilidade.

### 5. Testes São Parte do Código

Testes não são opcionais — são a especificação executável do comportamento.

**Framework:** pytest (sempre). Nunca unittest puro.

**Padrões:**
- Padrão AAA: Arrange → Act → Assert (separados por linha em branco)
- Use `@pytest.fixture` para setup reutilizável
- Use `@pytest.mark.parametrize` para múltiplos cenários
- Nomes descritivos: `test_rejeita_email_invalido`, não `test_email_1`
- Mínimo 90% de cobertura em lógica de negócio
- Testes rápidos rodam por padrão; marque lentos com `@pytest.mark.slow`

### 6. Ferramentas Modernas (2025-2026)

A stack recomendada é enxuta e rápida:

| Ferramenta | Substitui            | Para quê                          |
|------------|----------------------|-----------------------------------|
| **ruff**   | flake8, isort, black, pyupgrade | Lint + format unificado (10-100x mais rápido) |
| **mypy**   | —                    | Type checking estático             |
| **pytest** | unittest             | Testes                             |
| **uv**     | pip+poetry+venv      | Gerenciamento de deps e ambientes  |
| **pre-commit** | —              | Hooks automáticos antes de commit  |

### 7. Padrões Pythônicos Essenciais

Estes são os idiomas que distinguem código Python de "código Java escrito em Python":

- **Iteração direta** — `for item in collection`, nunca `for i in range(len(...))`
- **Comprehensions** — para transformações simples de coleções
- **Generators** — para datasets grandes (processamento lazy)
- **Context managers** — para qualquer recurso que precisa de cleanup
- **Decorators** — para preocupações transversais (logging, retry, cache)
- **Unpacking** — `first, *rest, last = sequence`
- **Walrus operator** — `if (n := len(data)) > 10:` para evitar repetição
- **f-strings** — sempre, nunca `format()` ou `%`
- **pathlib.Path** — sempre, nunca `os.path`

### 8. Anti-Padrões Fatais

Estes são bugs esperando para acontecer:

| Anti-Padrão                          | Problema                              | Correção                              |
|--------------------------------------|---------------------------------------|---------------------------------------|
| Argumento default mutável            | Compartilhado entre chamadas          | `field(default_factory=list)`         |
| `except:` ou `except Exception:`     | Engole erros silenciosamente          | Capture exceções específicas          |
| Variáveis globais mutáveis           | Estado compartilhado imprevisível     | Injeção de dependência                |
| God class (classe faz tudo)          | Impossível testar e manter            | SRP — uma responsabilidade por classe |
| Wildcard import `from x import *`    | Polui namespace, conflitos            | Imports explícitos                    |
| Hardcoded paths/secrets              | Quebra em ambientes diferentes        | Variáveis de ambiente / config        |
| Retornar tipos mistos                | `return None` ou `return User`        | Use `User | None` com type hint       |

---

## Fluxo de Trabalho

Ao implementar código Python, siga esta sequência:

1. **Entender** — Leia o código existente e entenda a arquitetura
2. **Planejar** — Identifique a abordagem mais simples que resolve o problema
3. **Implementar** — Código Pythônico com type hints e docstrings
4. **Testar** — Escreva testes com pytest antes de considerar "pronto"
5. **Validar** — Execute toda a pipeline de qualidade:

```bash
# Pipeline completa de validação
ruff check . --fix && ruff format .   # Lint + format
mypy . --strict                        # Type checking
pytest --cov=src --cov-fail-under=90   # Testes + cobertura
```

6. **Limpar** — Remova arquivos temporários, verifique git status

---

## Princípios SOLID em Python

Python favorece composição sobre herança e protocolos sobre classes abstratas:

- **SRP** — Uma classe, uma responsabilidade. Se a classe tem "And" no nome, divida.
- **OCP** — Extensível via novos tipos, não modificação de if/elif chains. Use `Protocol`.
- **LSP** — Subtipos substituíveis. Se `Square` não se comporta como `Rectangle`, não herde.
- **ISP** — Interfaces pequenas com `Protocol`. Não force implementação de métodos desnecessários.
- **DIP** — Dependa de `Protocol`, não de classes concretas. Injete dependências no construtor.

Consulte `references/pythonic-patterns.md` para exemplos completos de cada princípio.

---

## Docstrings (PEP 257, formato Google)

```python
def processar_pagamento(
    valor: float,
    *,
    moeda: str = "BRL",
    parcelas: int = 1,
) -> ResultadoPagamento:
    """Processa um pagamento e retorna o resultado da transação.

    Valida o valor e a moeda antes de enviar para o gateway.
    Em caso de falha no gateway, tenta novamente até 3 vezes.

    Args:
        valor: Valor do pagamento em centavos.
        moeda: Código ISO 4217 da moeda (default: BRL).
        parcelas: Número de parcelas (1 = à vista).

    Returns:
        ResultadoPagamento com status e id da transação.

    Raises:
        ValidationError: Se valor <= 0 ou moeda inválida.
        GatewayError: Se o gateway falhar após todas as tentativas.
    """
```

**Regras:**
- Toda função/classe pública tem docstring
- Primeira linha é um resumo imperativo ("Processa...", não "Esta função processa...")
- Formato Google (Args, Returns, Raises) — mais legível que Sphinx
- Docstrings em português brasileiro
