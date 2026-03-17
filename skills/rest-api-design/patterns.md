# Padrões de API — Referência

## Paginação

Definir a estratégia antes de implementar. Trocar depois é breaking change.

### Offset/Page

Usar quando: dataset pequeno/estático (< 10k), navegação numérica, admin.

```
GET /users?_page=2&_limit=20
```

Envelope:
```json
{
  "records": [...],
  "meta": {
    "page": 2,
    "limit": 20,
    "total": 1543,
    "total_pages": 78
  }
}
```

### Cursor-based

Usar quando: dataset grande/crescente, dados mutáveis, scroll infinito.

```
GET /users?_after=01ARZ3NDEKTSV4RRFFQ69G5FAV&_limit=20
```

Envelope:
```json
{
  "records": [...],
  "meta": {
    "limit": 20,
    "total": 1543,
    "next_cursor": "01ARZ3NDEKTSV4RRFFQ69G5FAX",
    "has_more": true
  }
}
```

Cursor deve ser **opaco** (base64 ou ID direto).

### Regras

- Resposta de listagem **sempre** objeto, nunca array nu.
- `limit` padrão: 20, máximo: 100. Rejeitar com `400` se exceder.
- Sempre incluir `has_more` ou `total_pages`.
- `total` apenas se computacionalmente barato (omitir é aceitável em cursor-based).

---

## Filtros

Query params com nomes dos campos do recurso:

```
GET /orders?status=pending&customer_id=usr_123
GET /products?category=electronics&price_gte=100&price_lte=500
GET /users?created_at_gte=2024-01-01T00:00:00Z
```

- Datas em ISO 8601 com timezone: `2024-01-15T10:30:00Z`
- Ranges com sufixos de operador: `_gte` (>=), `_gt` (>), `_lte` (<=), `_lt` (<)
- Múltiplos valores: `?status=pending,processing`
- Documentar todos os filtros disponíveis no spec.

---

## Busca Full-text

Separar busca de filtro. Parâmetro universal: `_q`

```
GET /products?_q=wireless+headphones
GET /users?_q=john&role=admin
```

- `_q` busca em campos relevantes (definidos e documentados no spec)
- Nunca usar `_q` para filtros exatos — para isso usar nome do campo

---

## Ordenação

```
GET /products?_sort=price&_order=asc
GET /orders?_sort=status,created_at&_order=asc,desc
```

- `_sort` (campo) e `_order` (`asc` | `desc`, padrão `asc`)
- Listar campos que suportam ordenação. `400` para não suportados.
- Sort padrão obrigatório: `created_at desc`
- Cursor-based requer sort estável: incluir `id` internamente.

---

## Expansão (`_expand`)

Por padrão, retornar apenas IDs de recursos relacionados. Expandir sob demanda:

```
GET /orders/ord_123
→ { "id": "ord_123", "customer_id": "usr_456" }

GET /orders/ord_123?_expand=customer,product
→ { "id": "ord_123", "customer": { "id": "usr_456", "name": "João" }, ... }
```

- Listar campos expansíveis no spec (não permitir expansão arbitrária)
- Dot-notation para aninhamento: `?_expand=order.customer`
- Profundidade máxima: 2 níveis
- Expansões não listadas retornam `400`

---

## Sparse Fieldsets (`_fields`)

```
GET /users?_fields=id,name,email
```

- Campos inexistentes retornam `400`
- `id` sempre retornado, mesmo que não solicitado
- Documentar campos obrigatórios vs opcionais

---

## Extensibilidade e Compatibilidade

### Breaking changes (requerem nova versão)

- Remover ou renomear campo/recurso
- Mudar tipo de campo (`string` → `integer`)
- Tornar campo opcional em obrigatório
- Mudar semântica de status code
- Remover valor de enum

### Não-breaking (sem nova versão)

- Adicionar campos opcionais na resposta
- Adicionar endpoints
- Adicionar query params opcionais (com default que preserva comportamento)
- Adicionar valores em enums de resposta

### Regras de extensibilidade

1. **Resposta sempre objeto**, nunca array nu
2. **Tolerância na leitura** (Lei de Postel): clientes ignoram campos desconhecidos
3. **Enums extensíveis**: documentar que novos valores podem surgir
4. **Timestamps obrigatórios**: `created_at` e `updated_at` (ISO 8601) em todo recurso

### Checklist

- [ ] Toda listagem é objeto com `records` e `meta`
- [ ] Nenhum endpoint retorna array como root
- [ ] Enums marcados como extensíveis
- [ ] Todos os recursos têm `created_at` e `updated_at`
- [ ] IDs são strings
- [ ] Query params novos têm defaults retrocompatíveis
- [ ] Campos novos são opcionais

### Parâmetros no OpenAPI

```yaml
parameters:
  - name: _expand
    in: query
    schema:
      type: string
    description: "Campos relacionados para expandir. Valores possíveis: customer, product."
  - name: _fields
    in: query
    schema:
      type: string
    description: "Subset de campos a retornar. 'id' sempre incluído."
  - name: _sort
    in: query
    schema:
      type: string
    description: "Campo para ordenação."
  - name: _order
    in: query
    schema:
      type: string
      enum: [asc, desc]
      default: asc
    description: "Direção da ordenação."
  - name: _q
    in: query
    schema:
      type: string
    description: "Busca textual em campos relevantes do recurso."
```
