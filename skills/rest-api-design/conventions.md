# Convenções REST API — Referência

## URIs e Nomenclatura

- Recursos são **substantivos, plural, lowercase**: `/users`, `/orders`, `/payment-methods`
- Sem verbos nas URIs: nunca `/getUser`, `/createOrder`, `/deleteAccount`
- kebab-case para múltiplas palavras: `/payment-methods`
- Sub-recursos representam posse/contenção: `/users/{userId}/orders`
- **Máximo dois níveis de aninhamento**. Além disso, achate com query params.

### Query Parameters

Parâmetros controladores usam prefixo `_`:
- Filtros de atributo: `GET /orders?status=pending&customer_id=usr_123`
- Ordenação: `GET /products?_sort=price&_order=asc`
- Paginação: `GET /users?_page=1&_limit=20` ou `?_after=01ARZ3...&_limit=20`
- Nunca use query params para identificadores obrigatórios — esses pertencem ao path.

---

## Métodos HTTP

| Método | Semântica | Idempotente | Body | Resposta sucesso |
|--------|----------|-----------|------|-----------------|
| GET | Recuperar recurso(s) | Sim | Não | `200` |
| POST | Criar novo recurso | Não | Sim | `201` + `Location` header |
| PUT | Substituição completa | Sim | Sim | `200` |
| PATCH | Atualização parcial | Não | Sim | `200` |
| DELETE | Remover recurso | Sim | Não | `204` (sem body) |

- GET nunca modifica estado
- PUT substitui inteiro; para parcial use PATCH
- Operações em lote: `POST /orders/bulk-cancel`

---

## Status Codes

Nunca retorne `200 OK` com body de erro.

### Sucesso

| Código | Quando usar |
|------|-------------|
| 200 | GET, PUT, PATCH com sucesso |
| 201 | POST que cria recurso |
| 202 | Operação assíncrona aceita |
| 204 | DELETE ou ação sem body |

### Erros do Cliente (4xx)

| Código | Quando usar |
|------|-------------|
| 400 | Sintaxe malformada, JSON inválido |
| 401 | Não autenticado |
| 403 | Autenticado mas não autorizado |
| 404 | Recurso não encontrado |
| 409 | Conflito (duplicidade, inconsistência) |
| 422 | Input semanticamente inválido (JSON válido, falha na validação de negócio) |
| 429 | Rate limit excedido |

### Erros do Servidor (5xx)

| Código | Quando usar |
|------|-------------|
| 500 | Erro inesperado |
| 503 | Serviço temporariamente indisponível |

**Distinção crítica:** 400 = "não consigo fazer o parse". 422 = "fiz o parse mas está semanticamente errado".

---

## Envelope de Erro Padronizado

Definir como componente reutilizável (`ErrorResponse`) no spec:

```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "One or more fields are invalid.",
    "details": [
      { "field": "email", "issue": "Invalid email format" }
    ],
    "traceId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
  }
}
```

- `code`: UPPER_SNAKE_CASE, legível por máquina. Documentar todos.
- `message`: Legível por humanos. Seguro para exibir. Sem detalhes internos.
- `details`: Opcional para erros simples, obrigatório para validação.
- `traceId`: Sempre incluir.
- Nunca expor stack traces, classes internas ou erros de banco.

---

## Versionamento

- **Versione desde o dia 1** via URI: `/v1/users`
- Breaking changes exigem versão major nova:
  - Remover/renomear campo ou recurso
  - Mudar tipo de campo
  - Mudar esquema de auth
- Não-breaking (sem nova versão): novos campos opcionais, novos endpoints, novos query params com default.

**Deprecação:**
- Headers: `Deprecation: true`, `Sunset: <data>`, `Link: </v2/...>; rel="successor-version"`
- Mínimo 6 meses de carência para APIs públicas.

---

## Identificadores (IDs)

- **Nunca IDs sequenciais inteiros** em APIs públicas (enumeration attacks).
- **Padrão: ULID** — único, distribuído, ordenável, URL-safe, 26 chars.
- UUIDv7 é alternativa aceitável.
- ID interno (banco) vs ID público (API) são coisas diferentes.
- Prefixos de tipo opcionais (estilo Stripe): `usr_01ARZ3...`, `ord_01ARZ3...`
- IDs são **sempre strings** no JSON, nunca números.

| Formato | Ordenável | Distribuído | Seguro para API | Uso |
|---|---|---|---|---|
| Integer | Sim | Não | **Não** | Apenas interno |
| UUIDv4 | Não | Sim | Sim | Legados |
| UUIDv7 | Sim | Sim | Sim | Alternativa |
| ULID | Sim | Sim | Sim | **Padrão** |

---

## Segurança (baseline)

- **Autenticação**: definir `securitySchemes`. OAuth2/Bearer JWT para APIs não-públicas.
- **Rate limiting**: headers `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `Retry-After` (obrigatório em 429).
- **HTTPS only**: URLs `https://` no bloco `servers`.

---

## Anti-patterns a Sinalizar

| Anti-pattern | Problema | Correção |
|---|---|---|
| `/api/v1/getUser` | Verbo na URI | `GET /v1/users/{id}` |
| `200` com `{"success": false}` | Quebra semântica HTTP | `4xx` com envelope de erro |
| Sem versionamento | Impossível evoluir | Sempre `/v1/` |
| Auth na URI | Security smell | Headers + `securitySchemes` |
| `/api/data` genérico | Não RESTful | Recursos explícitos |
| Aninhamento > 2 níveis | Difícil manter/cachear | Achatar com query params |
| Array como root | Impossível adicionar metadados | `{"records": [...], "meta": {...}}` |
| ID integer | Segurança + precisão JS | String ULID |
| Enum sem extensibilidade | Clientes quebram | Documentar novos valores possíveis |
