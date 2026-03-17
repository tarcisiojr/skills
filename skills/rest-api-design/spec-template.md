# Padrões FastAPI / Pydantic — Referência

O OpenAPI 3.1 é gerado automaticamente pelo FastAPI a partir dos schemas Pydantic e decorators de rota. Este arquivo documenta os padrões que garantem um OpenAPI correto e consistente.

---

## Schemas Base Compartilhados

### Envelope de Erro

```python
class ErrorDetail(BaseModel):
    field: str
    message: str
    code: str

class ErrorBody(BaseModel):
    code: str  # UPPER_SNAKE_CASE, legível por máquina
    message: str  # Legível por humanos
    details: list[ErrorDetail] | None = None  # Obrigatório em 422
    trace_id: str  # UUID para correlação de logs

class ErrorResponse(BaseModel):
    error: ErrorBody
```

### Paginação Offset-based

```python
class PaginationMeta(BaseModel):
    page: int
    limit: int
    total_records: int
    total_pages: int

class PaginatedResponse(BaseModel, Generic[T]):
    records: list[T]
    meta: PaginationMeta
```

### Identificador ULID

```python
# ID público na API — string ULID de 26 caracteres
id: str = Field(
    description="Identificador único do recurso (ULID)",
    examples=["01ARZ3NDEKTSV4RRFFQ69G5FAV"],
    min_length=26,
    max_length=26,
)
```

### Timestamps

```python
created_at: datetime = Field(
    description="Data de criação (ISO 8601 UTC)",
    examples=["2024-01-15T10:30:00Z"],
)
updated_at: datetime = Field(
    description="Data da última atualização (ISO 8601 UTC)",
    examples=["2024-01-15T14:22:00Z"],
)
```

---

## Padrão de Schema por Recurso

Cada recurso tem 3 schemas separados:

```python
class PatientCreate(BaseModel):
    """Campos obrigatórios para criação (POST body)."""
    name: str
    email: EmailStr
    phone: str | None = None
    date_of_birth: date
    gender: str

class PatientUpdate(BaseModel):
    """Campos opcionais para atualização (PATCH body)."""
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None

class PatientResponse(BaseModel):
    """Representação completa do recurso (response)."""
    id: str  # ULID
    name: str
    email: str
    phone: str | None
    date_of_birth: date
    gender: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

---

## Padrão de Rota FastAPI

```python
@router.post(
    "",
    response_model=PatientResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar paciente",
    description="Cria um novo paciente vinculado ao profissional autenticado.",
    responses={
        409: {"model": ErrorResponse, "description": "Email já cadastrado"},
        422: {"model": ErrorResponse, "description": "Dados inválidos"},
    },
)
async def create_patient(
    data: PatientCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> PatientResponse:
    ...
```

### Listagem com Paginação

```python
@router.get(
    "",
    response_model=PaginatedResponse[PatientResponse],
    summary="Listar pacientes",
    description="Retorna lista paginada. Sort padrão: name asc.",
)
async def list_patients(
    _page: int = Query(1, ge=1, description="Número da página"),
    _limit: int = Query(20, ge=1, le=100, description="Itens por página"),
    _sort: str = Query("name", description="Campo para ordenação"),
    _order: Literal["asc", "desc"] = Query("asc", description="Direção"),
    _q: str | None = Query(None, description="Busca textual"),
    gender: str | None = Query(None, description="Filtro por gênero"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[PatientResponse]:
    ...
```

### Endpoint Público (sem auth)

```python
@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login",
    # Sem Depends(get_current_user) = endpoint público
)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    ...
```

---

## Query Parameters de Controle

Todos com prefixo `_` para distinguir de filtros de atributo:

| Parâmetro | Tipo | Default | Descrição |
|-----------|------|---------|-----------|
| `_page` | int | 1 | Número da página |
| `_limit` | int | 20 | Itens por página (máx 100) |
| `_sort` | str | varia | Campo para ordenação |
| `_order` | str | "asc" | Direção (asc/desc) |
| `_q` | str | None | Busca textual |
| `_expand` | str | None | Relacionamentos para expandir |
| `_fields` | str | None | Subset de campos |

---

## Checklist de Implementação por Endpoint

- [ ] `summary` e `description` no decorator
- [ ] `response_model` com tipo correto
- [ ] `status_code` explícito (201 para POST, 204 para DELETE)
- [ ] `responses={}` com todos os status codes de erro
- [ ] `tags` para agrupamento no OpenAPI
- [ ] Type hints em todos os parâmetros
- [ ] Query parameters com `Query()` e descrição
- [ ] Path parameters com `Path()` e descrição
- [ ] Auth via `Depends(get_current_user)` ou ausente para públicos
