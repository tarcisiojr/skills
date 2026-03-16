# Testes, Resiliência, APIs e Observabilidade — Referência Detalhada

Baseado em: AWS, Microsoft, Atlassian, Martin Fowler, Cucumber

## Índice
1. [Pirâmide de Testes](#pirâmide-de-testes)
2. [TDD e BDD](#tdd-e-bdd)
3. [Design de APIs](#design-de-apis)
4. [Tratamento de Erros](#tratamento-de-erros)
5. [Circuit Breaker e Retry](#circuit-breaker-e-retry)
6. [Padrões de Cache](#cache)
7. [Observabilidade](#observabilidade)
8. [Feature Flags e Trunk-Based](#feature-flags)
9. [Checklist de Code Review](#code-review)

---

## Pirâmide de Testes

```
      /   E2E    \       ~10% — Fluxos completos (lentos, caros)
     /------------\
    / Integração   \     ~20% — Interação entre componentes
   /----------------\
  /   Unitários      \   ~70% — Lógica isolada (rápidos, baratos)
 /--------------------\
```

**Ajustes por contexto:**
- Microsserviços: mais integração (comunicação entre serviços)
- UI-heavy: mais E2E para interações complexas
- Bibliotecas/SDKs: quase 100% unitários

**Anti-padrão "Ice Cream Cone":** Muitos E2E, poucos unitários → suite lenta, frágil e cara.

**Regras:**
- Teste comportamento, não implementação
- Testes frágeis = testando detalhe interno
- E2E em todo commit? Não — use smoke tests + nightly full suite

---

## TDD e BDD

### TDD — Test-Driven Development
**Ciclo Red-Green-Refactor:**
1. **Red:** Escreva teste que falha (define comportamento desejado)
2. **Green:** Mínimo de código para passar
3. **Refactor:** Limpe código mantendo testes verdes

**Quando usar:** Lógica de negócio complexa, APIs, edge cases, alta confiabilidade.
**Quando NÃO:** Protótipos, UI experimental, scripts descartáveis.

**Erros comuns:**
- Testes grandes (teste uma coisa por vez)
- Pular refactor
- Testar implementação em vez de comportamento

### BDD — Behavior-Driven Development
**Formato Gherkin:**
```
Dado que [contexto inicial]
Quando [ação executada]
Então [resultado esperado]
```

**Quando usar:** Requisitos complexos com stakeholders; regras que mudam frequentemente.
**Quando NÃO:** Equipe 100% técnica; requisitos simples e claros.

---

## Design de APIs

### REST
- URLs baseadas em recursos (substantivos, não verbos)
- Verbos HTTP semânticos (GET, POST, PUT, PATCH, DELETE)
- Paginação, filtros e rate limiting obrigatórios
- Erros padronizados — RFC 9457 (Problem Details):
```json
{
  "type": "https://api.example.com/errors/validation",
  "title": "Erro de validação",
  "status": 422,
  "detail": "O campo email é obrigatório"
}
```
- Versionamento na URL (v1, v2) ou header
- OpenAPI/Swagger para documentação

### GraphQL
- Quando: frontends complexos, mobile (minimizar requests)
- Limitar profundidade e complexidade de queries
- DataLoader para evitar N+1
- Query complexity analysis obrigatório

### gRPC
- Quando: comunicação interna entre serviços, alta performance, streaming

### Erros Comuns (todos)
- Sem rate limiting
- Expor erros internos ao cliente
- APIs sem documentação ou contrato
- Sem autenticação (OAuth 2.0 / JWT)

---

## Tratamento de Erros

### Padrões
- **Try-Catch Centralizado** — Handler global + cada camada trata o que pode
- **Graceful Degradation** — Parte falha, resto funciona (ex: YouTube sem comentários)
- **Error Boundaries** — Frontend: captura erros de renderização, mostra fallback

### Regras
- NUNCA catch vazio (swallowing exceptions)
- Validação server-side obrigatória (frontend é cortesia)
- Mensagens úteis, não genéricas ("Ocorreu um erro")
- Nunca expor stack traces ao usuário
- Logar com contexto suficiente para debug

---

## Circuit Breaker e Retry

### Circuit Breaker
```
CLOSED ──(falhas > threshold)──> OPEN ──(timeout)──> HALF-OPEN
   ↑                                                      │
   └──────────(sucesso)────────────────────────────────────┘
```
- **Closed:** Requests passam, falhas contadas
- **Open:** Fail-fast, requests rejeitadas
- **Half-Open:** Poucos requests para testar recuperação

### Retry Pattern
- Exponential backoff (1s, 2s, 4s, 8s...)
- Jitter para evitar thundering herd
- Máximo 3-5 tentativas
- Apenas para operações idempotentes

### Combinação
Retry para falhas transientes → Circuit Breaker para persistentes.

**Erros comuns:**
- Retry sem backoff (DDoS no próprio serviço)
- Threshold muito alto/baixo
- Sem fallback quando circuito abre
- Retry em operações não-idempotentes

---

## Cache

| Padrão | Como | Melhor para |
|--------|------|-------------|
| **Cache-Aside** | App lê cache; miss → lê banco → popula cache | Leitura pesada |
| **Write-Through** | Escrita atualiza cache + banco simultaneamente | Dados sempre atualizados |
| **Write-Behind** | Escrita no cache, banco atualizado async | Alta taxa de escrita |
| **Prefetching** | Dados replicados proativamente | Workloads previsíveis |

**Regras:**
- Sempre definir TTL
- TTLs randomizados para evitar cache stampede
- Monitorar hit rate (< 80% = problema)
- Comece pelo mais acessado, não cache tudo

---

## Observabilidade

### Três Pilares
| Pilar | Captura | Exemplo |
|-------|---------|---------|
| **Logs** | Eventos discretos com contexto | ELK, Loki |
| **Métricas** | Valores numéricos ao longo do tempo | Prometheus, Grafana |
| **Traces** | Fluxo de request entre serviços | Jaeger, OpenTelemetry |

**Boas práticas:**
- Logging estruturado (JSON)
- Correlation IDs entre serviços
- Níveis de log: ERROR (ação), WARN (atenção), INFO (fluxo), DEBUG (dev)
- OpenTelemetry como padrão (vendor-neutral)
- Observabilidade como design concern, não afterthought

**Erros comuns:**
- Logar dados sensíveis (PII, senhas, tokens)
- Coletar 100% dos dados (~70% são desnecessários)
- Alert fatigue (alertas demais)

---

## Feature Flags

### Trunk-Based Development
- Commits pequenos e frequentes (diários)
- Branches de vida curta (máx 1 dia)
- Feature flags controlam visibilidade
- Deploy != Release (desacoplamento)

### Tipos de Flags
| Tipo | Duração | Uso |
|------|---------|-----|
| Release | Temporário | Esconder feature incompleta |
| Experiment | Temporário | A/B testing |
| Ops | Permanente | Circuit breaker, kill switch |
| Permission | Permanente | Acesso por role/plano |

**Regra crítica:** Limpe flags obsoletas — cada flag não removida é dívida técnica.

---

## Code Review

### Checklist

**Funcionalidade:**
- Implementa o solicitado
- Edge cases tratados
- Erros tratados adequadamente

**Qualidade:**
- Legível e organizado
- Segue convenções do projeto
- DRY — sem duplicação desnecessária
- Funções pequenas com SRP
- Nomes descritivos

**Design:**
- Alinhado com arquitetura do projeto
- Sem acoplamento desnecessário
- Abstrações apropriadas
- SOLID respeitado

**Segurança:**
- Sem SQL injection, XSS, CSRF
- Input validation server-side
- Sem dados sensíveis expostos
- Auth/authz verificados

**Testes:**
- Testes unitários para lógica nova
- Cobrem edge cases
- Testam comportamento, não implementação

**Performance:**
- Sem queries N+1
- Sem memory leaks
- Cache onde apropriado

**Processo:**
- PR < 400 linhas (ideal < 200)
- CI verde
- Descrição clara do que e porquê
