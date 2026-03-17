# API-First Design e Observabilidade — Referência Detalhada

Baseado em: REST/OpenAPI, GraphQL, CNCF, Google SRE

## Índice
1. [API-First Design](#api-first)
2. [REST Best Practices](#rest)
3. [GraphQL Best Practices](#graphql)
4. [Observabilidade Completa](#observabilidade)
5. [SLIs, SLOs e SLAs](#sli-slo-sla)

---

## API-First Design

### Princípios
- **API como produto** — Projete a interface antes de escrever código
- **Contract-First** — OpenAPI/Swagger spec antes da implementação
- **Versionamento** — Nunca quebre clientes existentes (v1, v2 na URL)
- **Documentation as Code** — Documentação gerada do spec, sempre atualizada

### Erros Padronizados (RFC 9457)
```json
{
  "type": "https://api.example.com/errors/validation",
  "title": "Erro de validação",
  "status": 422,
  "detail": "O campo 'email' deve ser um endereço válido",
  "instance": "/users/123",
  "errors": [
    {"field": "email", "message": "Formato inválido"}
  ]
}
```

---

## REST

### Design de URLs
```
✅ Bom: substantivos no plural
GET    /users          → listar
GET    /users/123      → buscar por ID
POST   /users          → criar
PUT    /users/123      → substituir
PATCH  /users/123      → atualizar parcial
DELETE /users/123      → remover

✅ Relacionamentos
GET    /users/123/orders        → pedidos do usuário
POST   /users/123/orders        → criar pedido para usuário

❌ Ruim: verbos na URL
POST   /createUser
GET    /getUserById/123
POST   /deleteUser/123
```

### Obrigatórios desde o dia 1
- **Paginação:** `?page=1&per_page=20` com metadata (total, has_next)
- **Filtros:** `?status=active&created_after=2025-01-01`
- **Rate Limiting:** Headers `X-RateLimit-Limit`, `X-RateLimit-Remaining`
- **Auth:** OAuth 2.0 / JWT em toda API não-pública
- **CORS:** Configurado restritivamente (não `*`)
- **Compression:** gzip/brotli para responses

### Status Codes Corretos
| Código | Quando |
|--------|--------|
| 200 | Sucesso com body |
| 201 | Criado com sucesso |
| 204 | Sucesso sem body (DELETE) |
| 400 | Input inválido do cliente |
| 401 | Não autenticado |
| 403 | Autenticado mas sem permissão |
| 404 | Recurso não encontrado |
| 409 | Conflito (ex: email duplicado) |
| 422 | Validação falhou |
| 429 | Rate limit excedido |
| 500 | Erro interno do servidor |

---

## GraphQL

### Quando Usar (em vez de REST)
- Frontends com necessidades de dados variadas
- Mobile (minimizar requests e bandwidth)
- Múltiplos consumers com requisitos diferentes

### Boas Práticas
- Limitar profundidade de queries (max 5-7 níveis)
- Query complexity analysis obrigatório
- DataLoader para evitar N+1
- Timeouts em queries longas
- Não versionar — evoluir o schema (deprecate fields)
- Mutations separadas de queries (CQRS mindset)

### Quando NÃO Usar
- APIs simples/CRUD (REST é mais simples)
- File upload pesado (REST/gRPC melhor)
- Cache HTTP nativo é importante (REST cacheia melhor)

---

## Observabilidade

### Os 3 Pilares

**Logs — O que aconteceu?**
- Eventos discretos com timestamp e contexto
- Estruturados (JSON) para busca e análise
- Níveis: ERROR (precisa ação) → WARN (atenção) → INFO (fluxo normal) → DEBUG (dev)
- Nunca logue dados sensíveis (PII, tokens, senhas)

**Métricas — Qual o estado?**
- Valores numéricos ao longo do tempo
- USE method para infraestrutura: Utilization, Saturation, Errors
- RED method para serviços: Rate, Errors, Duration
- Dashboards para visualização em tempo real

**Traces — Como o request fluiu?**
- Rastreia request de ponta a ponta entre serviços
- Identifica gargalos e latência por componente
- Span = unidade de trabalho dentro de um trace
- Correlation ID propaga contexto entre serviços

### OpenTelemetry
- Standard aberto e vendor-neutral (CNCF)
- SDK para instrumentação (auto e manual)
- Collector para processamento e exportação
- Suporta logs, métricas e traces unificados

### Alerting Eficaz
- Alerte sobre **sintomas** (latência, error rate), não causas (CPU alta)
- Todo alerta deve ter runbook associado
- Evite alert fatigue — menos alertas, mais relevantes
- Severidades claras: P1 (drop everything) → P4 (next sprint)

---

## SLIs, SLOs e SLAs

### Definições
- **SLI (Service Level Indicator)** — Métrica que mede o serviço
  - Exemplo: "latência p99 de requests GET /users"
- **SLO (Service Level Objective)** — Objetivo interno
  - Exemplo: "99.9% das requests com latência < 200ms"
- **SLA (Service Level Agreement)** — Compromisso com cliente
  - Exemplo: "99.5% de uptime mensal; violação = crédito"

### SLOs Comuns
| Tipo de Serviço | SLO Típico |
|----------------|-----------|
| API crítica (pagamento) | 99.99% (4.3min downtime/mês) |
| API principal | 99.9% (43min/mês) |
| API interna | 99.5% (3.6h/mês) |
| Batch processing | 99% (7.3h/mês) |

### Error Budget
- Se SLO = 99.9%, error budget = 0.1% do período
- Enquanto tiver budget → pode fazer deploys, experimentos
- Budget esgotado → freeze de features, foco em estabilidade
- Ferramenta de negociação entre velocidade e confiabilidade
