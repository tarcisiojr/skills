# Escalabilidade e Resiliência — Referência Detalhada

Baseado em: AWS, Azure, Netflix, Microsoft Patterns

## Índice
1. [Padrões de Escalabilidade](#escalabilidade)
2. [Padrões de Resiliência](#resiliência)
3. [Tabela de Decisão](#decisão)

---

## Escalabilidade

### Horizontal vs Vertical

| Aspecto | Vertical (Scale Up) | Horizontal (Scale Out) |
|---------|--------------------|-----------------------|
| O que faz | Mais CPU/RAM no mesmo servidor | Mais servidores |
| Limite | Hardware máximo da máquina | Virtualmente ilimitado |
| Downtime | Geralmente requer restart | Zero downtime |
| Custo | Exponencial após certo ponto | Linear |
| Complexidade | Baixa | Alta (estado distribuído) |

**Regra:** Horizontal é preferível para produção. Vertical é aceitável para banco de dados ou componentes difíceis de distribuir.

### Padrões de Escalabilidade

**Sharding (Particionamento Horizontal):**
- Divide dados em múltiplos bancos/tabelas baseado em shard key
- Shard key deve distribuir uniformemente (evitar hot spots)
- Bom: tenant_id, user_id com hash. Ruim: data de criação (skew temporal)

**Read Replicas:**
- Cópias read-only do banco principal
- Redirecione leituras para réplicas, escritas para primário
- Aceite eventual consistency para leituras

**Caching:**
- Cache-Aside (Lazy Loading) como padrão — leia cache, se miss leia banco e popule
- Sempre defina TTL — dados stale indefinidamente é bug
- TTLs randomizados para evitar cache stampede
- Monitore hit rate — abaixo de 80% indica problema

**Load Balancing:**
- Distribui tráfego entre instâncias
- Algoritmos: Round Robin, Least Connections, IP Hash
- Health checks para remover instâncias com problemas

**CDN:**
- Conteúdo estático próximo do usuário
- Reduz latência e carga no origin server
- Cache-Control headers para controlar TTL

**Auto-Scaling:**
- Ajuste automático baseado em métricas (CPU, memória, request count)
- Defina min/max instances para controlar custos
- Cooldown period para evitar thrashing (escalar e desescalar repetidamente)

**Connection Pooling:**
- Reutilize conexões de banco/HTTP em vez de criar por request
- Dimensione pool baseado em carga esperada
- Monitore pool exhaustion como métrica de saturação

---

## Resiliência

### Circuit Breaker
```
CLOSED ──(falhas > threshold)──> OPEN ──(timeout)──> HALF-OPEN
   ↑                                                      │
   └──────────(sucesso)────────────────────────────────────┘
```

- **Closed:** Normal, falhas contadas. Se threshold excedido → abre
- **Open:** Fail-fast imediato. Após timeout → half-open
- **Half-Open:** Permite poucos requests de teste. Sucesso → fecha. Falha → abre

**Configuração típica:**
- Threshold: 5 falhas em 10 segundos
- Open timeout: 30-60 segundos
- Half-open requests: 3-5

### Retry com Exponential Backoff

```
Tentativa 1: imediato
Tentativa 2: 1s + jitter
Tentativa 3: 2s + jitter
Tentativa 4: 4s + jitter
Tentativa 5: desistir
```

- Jitter = delay aleatório para evitar thundering herd
- Máximo 3-5 tentativas
- Apenas para operações **idempotentes** (GET, PUT, DELETE com ID)
- Nunca retry em 4xx (erro do cliente) — só em 5xx e timeouts

### Bulkhead
- Isola pools de recursos (threads, conexões) por serviço/funcionalidade
- Se pool A esgota, pool B continua funcionando
- Exemplo: pool separado para pagamentos vs notificações

### Timeout
- Toda chamada externa tem timeout explícito
- Sem timeout = thread presa indefinidamente = resource starvation
- Timeout hierárquico: timeout da operação > soma dos timeouts internos

### Graceful Degradation
- Sistema funciona com capacidade reduzida quando componentes falham
- Exemplo: Netflix mostra catálogo genérico se motor de recomendação cai
- Priorize funcionalidades core sobre features secundárias

### Health Check
- Endpoint `/health` que verifica dependências críticas
- Liveness: "processo está rodando?" (restart se falhar)
- Readiness: "pronto para receber tráfego?" (remove do load balancer se falhar)

### Dead Letter Queue (DLQ)
- Mensagens que falham após N retries vão para fila separada
- Permite análise posterior sem bloquear processamento
- Alerte quando DLQ acumula mensagens

### Saga Pattern
- Transações distribuídas como sequência de transações locais
- Cada step tem compensação (rollback) se step posterior falhar
- Choreography (eventos) vs Orchestration (coordenador central)

---

## Tabela de Decisão

| Problema | Padrão | Implementação |
|----------|--------|---------------|
| Serviço externo instável | Circuit Breaker | Resilience4j, Polly, tenacity |
| Falhas de rede transientes | Retry + Backoff | Exponential com jitter |
| Um serviço derruba todos | Bulkhead | Thread pools separados |
| Request presa infinitamente | Timeout | Em toda chamada externa |
| Componente opcional falhou | Graceful Degradation | Fallback com dados cached |
| Preciso saber se serviço está ok | Health Check | /health, /ready endpoints |
| Mensagem não processável | Dead Letter Queue | DLQ com alerting |
| Transação entre N serviços | Saga | Choreography ou Orchestration |
| Leitura pesada | Cache + Read Replicas | Redis + replicas de banco |
| Tráfego imprevisível | Auto-Scaling | Metrics-based com cooldown |
