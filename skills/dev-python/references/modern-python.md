# Python Moderno — Type Hints, Async e Features 3.10+

## Índice
1. [Type Hints Modernos](#type-hints-modernos)
2. [Structural Pattern Matching](#structural-pattern-matching)
3. [Dataclasses Avançadas](#dataclasses-avançadas)
4. [Async/Await Moderno](#asyncawait-moderno)
5. [Pathlib](#pathlib)
6. [F-strings Avançadas](#f-strings-avançadas)
7. [Walrus Operator](#walrus-operator)

---

## Type Hints Modernos

### Sintaxe Moderna (Python 3.10+)
```python
# Union com | (PEP 604)
def buscar(id: int) -> User | None:
    ...

# Tipos built-in como genéricos (PEP 585)
def processar(items: list[str], config: dict[str, int]) -> tuple[bool, str]:
    ...

# TypeAlias (Python 3.12+)
type Vector = list[float]
type Matrix[T] = list[list[T]]
type Handler = Callable[[Request], Response]
```

### Protocol — Duck Typing Tipado (PEP 544)
```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Serializable(Protocol):
    """Qualquer objeto que pode ser serializado."""
    def to_dict(self) -> dict: ...
    def to_json(self) -> str: ...

# Qualquer classe que implemente to_dict() e to_json() satisfaz o protocolo
# Sem herança necessária — verdadeiro duck typing com segurança de tipos

class User:
    def to_dict(self) -> dict:
        return {"name": self.name}

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

# ✅ Funciona — User satisfaz Serializable
def save(entity: Serializable) -> None:
    data = entity.to_dict()
    ...
```

### Self Type (PEP 673, Python 3.11+)
```python
from typing import Self

class Builder:
    def with_name(self, name: str) -> Self:
        self.name = name
        return self  # Retorna o tipo correto em subclasses

    def with_age(self, age: int) -> Self:
        self.age = age
        return self
```

### ParamSpec (PEP 612) — Decorators Tipados
```python
from typing import ParamSpec, TypeVar, Callable
import functools

P = ParamSpec("P")
R = TypeVar("R")

def log_calls(func: Callable[P, R]) -> Callable[P, R]:
    """Decorator que preserva tipos perfeitamente."""
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Chamando {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_calls
def add(a: int, b: int) -> int:
    return a + b

# mypy sabe que add(a: int, b: int) -> int
```

### TypeGuard (PEP 647) — Narrowing de Tipos
```python
from typing import TypeGuard

def is_string_list(val: list[object]) -> TypeGuard[list[str]]:
    """Type guard que verifica se todos os elementos são strings."""
    return all(isinstance(x, str) for x in val)

def process(data: list[object]) -> None:
    if is_string_list(data):
        # mypy sabe que data é list[str] aqui
        print(" ".join(data))
```

### TypedDict para JSON
```python
from typing import TypedDict, NotRequired, Required

class APIResponse(TypedDict):
    status: str
    data: list[dict]
    error: NotRequired[str]      # Campo opcional
    timestamp: Required[str]      # Explicitamente obrigatório

# Para herança
class PaginatedResponse(APIResponse):
    page: int
    total_pages: int
    has_next: bool
```

---

## Structural Pattern Matching (Python 3.10+)

```python
# Match básico com guards
def processar_comando(comando: dict) -> str:
    match comando:
        case {"action": "create", "data": data} if data:
            return criar_recurso(data)
        case {"action": "delete", "id": int(id_val)}:
            return deletar_recurso(id_val)
        case {"action": "list", "filters": dict(filtros)}:
            return listar_recursos(filtros)
        case {"action": action}:
            return f"Ação desconhecida: {action}"
        case _:
            return "Comando inválido"

# Match com classes
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

@dataclass
class Circle:
    center: Point
    radius: float

@dataclass
class Rectangle:
    top_left: Point
    bottom_right: Point

def area(shape) -> float:
    match shape:
        case Circle(center=_, radius=r):
            return 3.14159 * r ** 2
        case Rectangle(top_left=Point(x1, y1), bottom_right=Point(x2, y2)):
            return abs(x2 - x1) * abs(y2 - y1)
        case _:
            raise ValueError(f"Forma desconhecida: {type(shape)}")

# Match com OR patterns e captura
def classificar_status(code: int) -> str:
    match code:
        case 200 | 201 | 204:
            return "sucesso"
        case 301 | 302:
            return "redirecionamento"
        case 400:
            return "requisição inválida"
        case 401 | 403:
            return "não autorizado"
        case 404:
            return "não encontrado"
        case code if 500 <= code < 600:
            return "erro do servidor"
        case _:
            return f"código desconhecido: {code}"
```

---

## Dataclasses Avançadas

```python
from dataclasses import dataclass, field, asdict, replace
from typing import Self

@dataclass(slots=True, frozen=True, order=True)
class Version:
    """Versão semântica com comparação natural."""
    major: int
    minor: int
    patch: int

    @classmethod
    def from_string(cls, version: str) -> Self:
        parts = version.split(".")
        return cls(int(parts[0]), int(parts[1]), int(parts[2]))

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

# Comparação funciona automaticamente com order=True
assert Version(2, 0, 0) > Version(1, 9, 9)

@dataclass(slots=True)
class Config:
    """Configuração com valores padrão e validação."""
    host: str = "localhost"
    port: int = 8080
    debug: bool = False
    tags: list[str] = field(default_factory=list)
    _validated: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        """Validação pós-inicialização."""
        if self.port < 0 or self.port > 65535:
            raise ValueError(f"Porta inválida: {self.port}")
        self._validated = True

# Criar cópia modificada (frozen-friendly)
config = Config(host="prod.example.com", port=443)
dev_config = replace(config, host="localhost", debug=True)

# Converter para dict (útil para serialização)
config_dict = asdict(config)
```

---

## Async/Await Moderno

### TaskGroup (Python 3.11+) — Substitui gather()
```python
import asyncio

async def buscar_dados_usuario(user_id: int) -> dict:
    """Busca todos os dados do usuário concorrentemente."""
    async with asyncio.TaskGroup() as tg:
        perfil_task = tg.create_task(buscar_perfil(user_id))
        pedidos_task = tg.create_task(buscar_pedidos(user_id))
        notificacoes_task = tg.create_task(buscar_notificacoes(user_id))

    # Se qualquer task falhar, TODAS são canceladas automaticamente
    return {
        "perfil": perfil_task.result(),
        "pedidos": pedidos_task.result(),
        "notificacoes": notificacoes_task.result(),
    }
```

### Exception Groups (Python 3.11+)
```python
async def processar_lote(items: list[str]) -> list[str]:
    """Processa lote com tratamento granular de erros."""
    try:
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(processar(item)) for item in items]
    except* ConnectionError as eg:
        logger.error(f"{len(eg.exceptions)} erros de conexão")
        # Pode tratar cada exceção individualmente
        for exc in eg.exceptions:
            logger.error(f"  Detalhe: {exc}")
    except* ValueError as eg:
        logger.error(f"{len(eg.exceptions)} erros de validação")

    return [t.result() for t in tasks if not t.cancelled()]
```

### Semáforo para Rate Limiting
```python
async def buscar_urls(urls: list[str], max_concurrent: int = 10) -> list[str]:
    """Busca URLs com limite de concorrência."""
    semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch_one(url: str) -> str:
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                    return await resp.text()

    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(fetch_one(url)) for url in urls]

    return [t.result() for t in tasks]
```

### Timeouts
```python
# Timeout em operação individual
async def buscar_com_timeout(url: str) -> str:
    async with asyncio.timeout(10):  # Python 3.11+
        return await fetch(url)

# Timeout com fallback
async def buscar_ou_cache(url: str) -> str:
    try:
        async with asyncio.timeout(5):
            return await fetch(url)
    except TimeoutError:
        logger.warning(f"Timeout ao buscar {url}, usando cache")
        return await get_from_cache(url)
```

---

## Pathlib

```python
from pathlib import Path

# Construção de paths
base = Path(__file__).parent
config_path = base / "config" / "settings.json"
data_dir = Path.home() / ".myapp" / "data"

# Criar diretórios
data_dir.mkdir(parents=True, exist_ok=True)

# Leitura e escrita
content = config_path.read_text(encoding="utf-8")
config_path.write_text(json.dumps(config), encoding="utf-8")

# Listar arquivos
python_files = list(Path("src").rglob("*.py"))
csv_files = list(Path("data").glob("*.csv"))

# Informações do arquivo
if config_path.exists():
    size = config_path.stat().st_size
    name = config_path.stem        # "settings"
    ext = config_path.suffix       # ".json"
    parent = config_path.parent    # Path("config")

# Manipulação
new_path = config_path.with_suffix(".yaml")
new_path = config_path.with_stem("production")

# Temporários com pathlib
import tempfile
with tempfile.TemporaryDirectory() as tmpdir:
    tmp_path = Path(tmpdir) / "output.csv"
    tmp_path.write_text("data")
```

---

## F-strings Avançadas

```python
# Formatação numérica
valor = 1234567.89
print(f"R$ {valor:,.2f}")        # R$ 1,234,567.89
print(f"{valor:.2e}")             # 1.23e+06
print(f"{0.85:.0%}")              # 85%

# Alinhamento e padding
name = "Python"
print(f"{name:>20}")              # "              Python"
print(f"{name:^20}")              # "       Python       "
print(f"{name:-<20}")             # "Python--------------"

# Debug (Python 3.8+)
x = 42
print(f"{x = }")                  # "x = 42"
print(f"{x * 2 = }")             # "x * 2 = 84"

# Datetime
from datetime import datetime
now = datetime.now()
print(f"{now:%Y-%m-%d %H:%M}")   # "2025-03-16 14:30"

# Representação
obj = [1, 2, 3]
print(f"{obj!r}")                 # "[1, 2, 3]" (repr)
print(f"{obj!s}")                 # "[1, 2, 3]" (str)

# Expressões complexas
users = [{"name": "Ana"}, {"name": "Bob"}]
print(f"Total: {len(users)} usuários")
print(f"Nomes: {', '.join(u['name'] for u in users)}")

# Nested f-strings (Python 3.12+)
width = 10
print(f"{'resultado':>{width}}")
```

---

## Walrus Operator (:=)

```python
# Evitar chamada de função duplicada
if (n := len(data)) > 10:
    print(f"Processando {n} itens em lotes")

# Em loops de leitura
while chunk := file.read(8192):
    process(chunk)

# Em list comprehensions com filtro
results = [
    transformed
    for item in items
    if (transformed := expensive_transform(item)) is not None
]

# Em expressões condicionais
if (match := pattern.search(text)) is not None:
    print(f"Encontrado: {match.group()}")

# ⚠ Não abuse — use apenas quando claramente reduz repetição
# ❌ Ruim: obscurece o código
total = sum(x := int(s) for s in strings if x > 0)  # Confuso!
```
