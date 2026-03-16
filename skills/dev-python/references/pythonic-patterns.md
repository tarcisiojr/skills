# Padrões Pythônicos — Referência Detalhada

Baseado em: Raymond Hettinger, Fluent Python (Ramalho), Effective Python (Slatkin)

## Índice
1. [Iteração Idiomática](#iteração-idiomática)
2. [Dicionários e Collections](#dicionários-e-collections)
3. [Comprehensions e Generators](#comprehensions-e-generators)
4. [Context Managers](#context-managers)
5. [Decorators](#decorators)
6. [Dunder Methods](#dunder-methods)
7. [Funções como Objetos de Primeira Classe](#funções-como-objetos)
8. [SOLID em Python com Exemplos](#solid-em-python)
9. [Tratamento de Erros Completo](#tratamento-de-erros)
10. [Anti-Padrões com Correções](#anti-padrões)

---

## Iteração Idiomática

Raymond Hettinger ensina: "Se você está usando `range(len(...))`, provavelmente está fazendo errado."

```python
# ❌ Ruim: loop por índice
for i in range(len(colors)):
    print(colors[i])

# ✅ Bom: iteração direta
for color in colors:
    print(color)

# ✅ enumerate quando precisa do índice
for i, color in enumerate(colors):
    print(i, '-->', color)

# ✅ enumerate com start customizado
for rank, name in enumerate(winners, start=1):
    print(f"{rank}º lugar: {name}")

# ✅ reversed para iteração reversa
for color in reversed(colors):
    print(color)

# ✅ zip para iterar sobre múltiplas sequências
for name, color in zip(names, colors):
    print(name, '-->', color)

# ✅ zip com strict (Python 3.10+) — erro se tamanhos diferentes
for name, score in zip(names, scores, strict=True):
    print(f"{name}: {score}")

# ✅ sorted com key function
for student in sorted(students, key=lambda s: s.grade, reverse=True):
    print(student.name)
```

**Unpacking com starred expressions (Slatkin):**
```python
first, *middle, last = [1, 2, 3, 4, 5]
# first=1, middle=[2, 3, 4], last=5

_, *body, _ = "header,data1,data2,footer".split(",")
# body=['data1', 'data2']

# Swap Pythônico
a, b = b, a

# Atualização simultânea de estado
x, y = x + dx * t, y + dy * t
```

---

## Dicionários e Collections

```python
from collections import Counter, defaultdict, deque

# Construir dict a partir de pares
d = dict(zip(names, colors))

# Contagem — SEMPRE use Counter
word_counts = Counter(words)
top_3 = word_counts.most_common(3)

# Agrupamento — defaultdict
groups = defaultdict(list)
for name in names:
    groups[len(name)].append(name)

# dict.get para valores padrão
value = config.get("timeout", 30)

# setdefault para inicializar e acessar
graph.setdefault(node, []).append(neighbor)

# Merge de dicts (Python 3.9+)
merged = defaults | user_config | overrides

# deque para filas (O(1) em ambas as pontas)
queue: deque[str] = deque(maxlen=100)
queue.append("item")
item = queue.popleft()
```

---

## Comprehensions e Generators

```python
# List comprehension — transformações simples em uma linha
squares = [x**2 for x in range(10)]
even_squares = [x**2 for x in range(10) if x % 2 == 0]

# Dict comprehension
name_lengths = {name: len(name) for name in names}

# Set comprehension
unique_lengths = {len(name) for name in names}

# ⚠ Se a comprehension não cabe em uma linha, use um loop normal
# ❌ Ruim: comprehension complexa demais
result = [
    transform(item)
    for group in groups
    for item in group.items
    if item.is_valid()
    and item.category in allowed_categories
]

# ✅ Bom: loop explícito quando é complexo
result = []
for group in groups:
    for item in group.items:
        if item.is_valid() and item.category in allowed_categories:
            result.append(transform(item))

# Generator expression — processamento lazy (não consome memória)
total = sum(x**2 for x in range(10_000_000))

# Generator function — para lógica complexa
def ler_arquivo_grande(path: str):
    """Lê arquivo grande linha por linha sem carregar na memória."""
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                yield line

# itertools para operações avançadas
from itertools import chain, islice, groupby

# Achatar listas
flat = list(chain.from_iterable(nested_lists))

# Pegar os primeiros N de um iterador
first_10 = list(islice(infinite_generator(), 10))
```

---

## Context Managers

Qualquer recurso que precisa de setup/cleanup deve usar context manager.

```python
from contextlib import contextmanager, suppress, asynccontextmanager

# Context manager com classe (quando precisa de estado)
class DatabaseConnection:
    """Gerencia conexão com banco de dados."""
    def __init__(self, url: str) -> None:
        self.url = url
        self.conn = None

    def __enter__(self):
        self.conn = create_connection(self.url)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
        return False  # Não suprime exceções

# Context manager com generator (mais conciso)
@contextmanager
def temporary_directory():
    """Cria diretório temporário e limpa ao sair."""
    path = Path(tempfile.mkdtemp())
    try:
        yield path
    finally:
        shutil.rmtree(path)

# suppress — ignorar exceções específicas de forma limpa
with suppress(FileNotFoundError):
    Path("temp.txt").unlink()

# Empilhar context managers
from contextlib import ExitStack

with ExitStack() as stack:
    files = [stack.enter_context(open(f)) for f in file_paths]
    # Todos os arquivos são fechados ao sair do bloco

# Context manager async
@asynccontextmanager
async def managed_session():
    """Gerencia sessão HTTP assíncrona."""
    session = aiohttp.ClientSession()
    try:
        yield session
    finally:
        await session.close()
```

---

## Decorators

Decorators separam preocupações transversais (logging, cache, retry) da lógica de negócio.

```python
import functools
import time
import logging

logger = logging.getLogger(__name__)

# Decorator simples com functools.wraps (SEMPRE use wraps)
def log_calls(func):
    """Loga chamadas de função com argumentos e resultado."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Chamando {func.__name__}({args}, {kwargs})")
        result = func(*args, **kwargs)
        logger.info(f"{func.__name__} retornou {result}")
        return result
    return wrapper

# Decorator com parâmetros
def retry(max_attempts: int = 3, delay: float = 1.0):
    """Reexecuta a função em caso de falha."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < max_attempts - 1:
                        time.sleep(delay * (2 ** attempt))
            raise last_error
        return wrapper
    return decorator

# Decorator para medir tempo de execução
def timer(func):
    """Mede e loga o tempo de execução."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.info(f"{func.__name__} executou em {elapsed:.4f}s")
        return result
    return wrapper

# Cache built-in (memoização)
@functools.lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Cache para funções com argumentos não-hashable
@functools.cache  # Python 3.9+ — cache ilimitado
def factorial(n: int) -> int:
    return n * factorial(n - 1) if n else 1
```

---

## Dunder Methods

Luciano Ramalho (Fluent Python): "O modelo de dados do Python é o que torna Python, Python."

```python
from dataclasses import dataclass
from typing import Iterator, Self

@dataclass(slots=True)
class Money:
    """Representa valor monetário com operações seguras."""
    amount: int  # Em centavos para evitar float
    currency: str = "BRL"

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("Valor não pode ser negativo")

    def __add__(self, other: Self) -> Self:
        if self.currency != other.currency:
            raise ValueError(f"Moedas diferentes: {self.currency} vs {other.currency}")
        return Money(self.amount + other.amount, self.currency)

    def __mul__(self, factor: int) -> Self:
        return Money(self.amount * factor, self.currency)

    def __bool__(self) -> bool:
        return self.amount > 0

    def __format__(self, spec: str) -> str:
        reais = self.amount / 100
        if spec == ".2f":
            return f"R$ {reais:,.2f}"
        return f"R$ {reais:,.2f}"

    def __repr__(self) -> str:
        return f"Money({self.amount}, '{self.currency}')"

    def __str__(self) -> str:
        return f"R$ {self.amount / 100:,.2f}"


# Container customizado com protocolo de iteração
@dataclass
class Playlist:
    """Playlist com suporte a iteração e acesso por índice."""
    name: str
    _tracks: list[str] = field(default_factory=list)

    def __len__(self) -> int:
        return len(self._tracks)

    def __getitem__(self, index: int) -> str:
        return self._tracks[index]

    def __iter__(self) -> Iterator[str]:
        return iter(self._tracks)

    def __contains__(self, track: str) -> bool:
        return track in self._tracks

    def add(self, track: str) -> None:
        self._tracks.append(track)
```

---

## Funções como Objetos

Em Python, funções são objetos de primeira classe — isso elimina a necessidade de muitos design patterns.

```python
from typing import Callable

# Strategy pattern com funções (Ramalho - Fluent Python)
type DiscountStrategy = Callable[[float, int], float]

def desconto_fidelidade(total: float, anos_cliente: int) -> float:
    """5% para clientes com mais de 2 anos."""
    return total * 0.05 if anos_cliente > 2 else 0

def desconto_volume(total: float, _: int) -> float:
    """10% para compras acima de R$ 500."""
    return total * 0.10 if total > 500 else 0

def melhor_desconto(
    total: float,
    anos_cliente: int,
    estrategias: list[DiscountStrategy],
) -> float:
    """Aplica a melhor estratégia de desconto."""
    return max(
        estrategia(total, anos_cliente)
        for estrategia in estrategias
    )

# Registro de handlers com dict de funções
handlers: dict[str, Callable] = {
    "create": handle_create,
    "update": handle_update,
    "delete": handle_delete,
}

def dispatch(action: str, data: dict) -> None:
    handler = handlers.get(action)
    if handler is None:
        raise ValueError(f"Ação desconhecida: {action}")
    handler(data)
```

---

## SOLID em Python

### SRP — Responsabilidade Única
```python
# ❌ Classe faz tudo
class UserManager:
    def create_user(self, data): ...
    def send_welcome_email(self, user): ...
    def generate_report(self, user): ...
    def save_to_database(self, user): ...

# ✅ Responsabilidades separadas
class UserService:
    def __init__(self, repo: UserRepository, email: EmailService) -> None:
        self._repo = repo
        self._email = email

    def create_user(self, data: CreateUserRequest) -> User:
        user = User.from_request(data)
        self._repo.save(user)
        self._email.send_welcome(user)
        return user
```

### OCP — Aberto/Fechado com Protocol
```python
from typing import Protocol

class Exporter(Protocol):
    def export(self, data: list[dict]) -> bytes: ...

class CSVExporter:
    def export(self, data: list[dict]) -> bytes: ...

class JSONExporter:
    def export(self, data: list[dict]) -> bytes: ...

# Novo formato? Crie nova classe. Nenhum código existente muda.
class ParquetExporter:
    def export(self, data: list[dict]) -> bytes: ...
```

### ISP — Segregação de Interface com Protocol
```python
class Readable(Protocol):
    def read(self) -> bytes: ...

class Writable(Protocol):
    def write(self, data: bytes) -> None: ...

# Componentes dependem apenas do que usam
def process_input(source: Readable) -> dict: ...
def save_output(target: Writable, data: bytes) -> None: ...
```

### DIP — Inversão de Dependência
```python
class NotificationSender(Protocol):
    def send(self, to: str, message: str) -> None: ...

class OrderService:
    def __init__(self, notifier: NotificationSender) -> None:
        self._notifier = notifier  # Depende da abstração

    def complete_order(self, order: Order) -> None:
        # ... lógica
        self._notifier.send(order.customer_email, "Pedido confirmado!")

# Fácil trocar: EmailSender, SMSSender, SlackSender...
```

---

## Tratamento de Erros

### Hierarquia de Exceções
```python
class AppError(Exception):
    """Base para exceções da aplicação."""
    def __init__(self, message: str, code: str | None = None) -> None:
        self.message = message
        self.code = code
        super().__init__(message)

class NotFoundError(AppError):
    def __init__(self, resource: str, id: str | int) -> None:
        super().__init__(f"{resource} '{id}' não encontrado", "NOT_FOUND")

class ValidationError(AppError):
    def __init__(self, field: str, detail: str) -> None:
        self.field = field
        super().__init__(f"Validação falhou em '{field}': {detail}", "VALIDATION")

class ExternalServiceError(AppError):
    def __init__(self, service: str, cause: Exception) -> None:
        self.service = service
        super().__init__(f"Falha em {service}: {cause}", "EXTERNAL")
```

### Padrões de Uso
```python
# Encadeamento com from (preserva causa original)
try:
    data = api_client.fetch(url)
except ConnectionError as e:
    raise ExternalServiceError("API Users", e) from e

# Suppress para segurança (oculta detalhes internos)
try:
    return validate_jwt(token)
except JWTError:
    raise AuthenticationError("Token inválido") from None

# Bloco try mínimo
try:
    f = open(path)
except FileNotFoundError:
    logger.error(f"Arquivo não encontrado: {path}")
    raise

with f:
    return f.read()  # Erros aqui propagam normalmente
```

---

## Anti-Padrões

### 1. Argumento Default Mutável
```python
# ❌ FATAL: lista compartilhada entre chamadas
def add_item(item, items=[]):
    items.append(item)
    return items

# ✅ Correto
def add_item(item: str, items: list[str] | None = None) -> list[str]:
    if items is None:
        items = []
    items.append(item)
    return items

# ✅ Com dataclass
@dataclass
class Config:
    tags: list[str] = field(default_factory=list)
```

### 2. Bare Except
```python
# ❌ Engole TODOS os erros (inclusive KeyboardInterrupt!)
try:
    process()
except:
    pass

# ❌ Quase tão ruim
try:
    process()
except Exception:
    pass

# ✅ Capture exceções específicas
try:
    process()
except (ConnectionError, TimeoutError) as e:
    logger.warning(f"Erro de rede: {e}")
    raise
```

### 3. God Class
```python
# ❌ Classe com 20+ métodos e múltiplas responsabilidades
class ApplicationManager:
    def create_user(self): ...
    def send_email(self): ...
    def generate_pdf(self): ...
    def connect_database(self): ...
    def parse_csv(self): ...

# ✅ Classes coesas com responsabilidade única
class UserService: ...
class EmailService: ...
class ReportGenerator: ...
```

### 4. Uso Incorreto de os.path
```python
# ❌ Antiquado e verboso
import os
path = os.path.join(os.path.dirname(__file__), "data", "config.json")
if os.path.exists(path):
    with open(path) as f:
        data = f.read()

# ✅ pathlib — moderno, legível, orientado a objetos
from pathlib import Path
path = Path(__file__).parent / "data" / "config.json"
if path.exists():
    data = path.read_text()
```

### 5. Retorno de Tipos Mistos sem Type Hint
```python
# ❌ Quem chama não sabe o que esperar
def find_user(user_id):
    user = db.get(user_id)
    if user:
        return user
    return None  # ou return False, ou return -1...

# ✅ Tipo explícito + pattern consistente
def find_user(user_id: int) -> User | None:
    """Busca usuário por ID. Retorna None se não encontrado."""
    return db.query(User).filter_by(id=user_id).first()
```
