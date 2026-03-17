---
name: dev-architecture-principles
description: >
  Skill sobre princípios de arquitetura de sistemas modernos — segurança by
  design (OWASP, Zero Trust), escalabilidade, resiliência, observabilidade,
  API-First design, multi-tenancy SaaS, cloud native (12-Factor App),
  Infrastructure as Code (IaC/GitOps), compliance (GDPR/LGPD) e Well-Architected
  Framework (AWS/Azure/GCP consolidado). Baseada em NIST, OWASP, AWS, Azure,
  Google Cloud, Netflix, Sam Newman, HashiCorp e CNCF. Use esta skill SEMPRE
  que o usuário estiver tomando decisões arquiteturais, projetando infraestrutura,
  discutindo escalabilidade, segurança, resiliência, multi-tenancy, compliance
  ou qualquer aspecto de arquitetura de sistemas. Acione quando mencionar:
  arquitetura, security by design, zero trust, escalabilidade, multi-tenant,
  SaaS, resiliência, circuit breaker, observabilidade, SLI/SLO, API design,
  12-factor, cloud native, IaC, terraform, GitOps, LGPD, GDPR, privacy by
  design, well-architected, pilares de arquitetura, ou qualquer decisão sobre
  como um sistema deve ser construído, escalado e operado em produção.
---

# Dev Architecture Principles — Princípios de Arquitetura de Sistemas

## Filosofia

> "Arquitetura é o conjunto de decisões que você gostaria de ter acertado no início do projeto." — Ralph Johnson

Princípios de arquitetura não são sobre tecnologia específica — são sobre **decisões de design de sistema** que afetam segurança, escalabilidade, resiliência, operação e compliance. Decisões caras de reverter que merecem reflexão antecipada.

## Quando Consultar as Referências

| Preciso de...                                      | Consultar                               |
|----------------------------------------------------|-----------------------------------------|
| Segurança by Design, OWASP, Zero Trust             | `references/security.md`                |
| Escalabilidade e Resiliência                       | `references/scalability-resilience.md`  |
| Well-Architected, 12-Factor, IaC, GitOps           | `references/cloud-native.md`            |
| API-First Design e Observabilidade                 | `references/api-observability.md`       |
| Multi-Tenancy SaaS e Compliance (GDPR/LGPD)       | `references/saas-compliance.md`         |

---

## Os 6 Pilares da Arquitetura Moderna

Consolidação dos frameworks AWS, Azure e Google Cloud:

| Pilar | Pergunta-chave | Princípio Central |
|-------|---------------|-------------------|
| **Segurança** | Como protegemos dados e sistemas? | Defense in depth, least privilege, zero trust |
| **Confiabilidade** | Como garantimos que funciona sob falha? | Design for failure, circuit breaker, graceful degradation |
| **Performance** | Como mantemos velocidade sob carga? | Cache, async, horizontal scaling, CDN |
| **Operação** | Como monitoramos e evoluímos? | Observabilidade, IaC, GitOps, automação |
| **Custo** | Como otimizamos gastos? | Right-sizing, auto-scaling, reserved instances |
| **Sustentabilidade** | Como minimizamos impacto ambiental? | Maximizar utilização, reduzir recursos ociosos |

---

## Segurança — Princípios Invioláveis

| Princípio | Regra Prática |
|-----------|---------------|
| **Least Privilege** | Mínimo acesso necessário, pelo menor tempo |
| **Defense in Depth** | Múltiplas camadas — nunca dependa de uma só |
| **Fail Securely** | Erro = estado seguro, não estado aberto |
| **Zero Trust** | Nunca confie, sempre verifique — localização de rede não é confiança |
| **Input Validation** | Valide TUDO no servidor — frontend é cortesia |
| **Security by Default** | Seguro por padrão, sem configuração manual |

---

## Escalabilidade — Decisões Fundamentais

```
Preciso escalar?
├── Mais capacidade no mesmo servidor    → Vertical (Scale Up)
├── Mais servidores distribuindo carga   → Horizontal (Scale Out)  ← preferível
├── Leitura pesada                       → Read Replicas + Cache
├── Escrita pesada                       → Sharding + Write-Behind Cache
└── Conteúdo estático                    → CDN
```

**Regra:** Projete para horizontal scaling desde o início — é mais barato e resiliente a longo prazo.

---

## Resiliência — Assuma que Tudo Falha

| Padrão | Quando Usar |
|--------|-------------|
| **Circuit Breaker** | Chamadas entre serviços — previne cascata |
| **Retry + Backoff** | Falhas transientes (rede, timeout) |
| **Bulkhead** | Isolar recursos — falha não contamina |
| **Timeout** | Toda chamada externa — nunca espere infinito |
| **Graceful Degradation** | Parte falha, resto funciona |
| **Health Check** | Detecção proativa de problemas |
| **Idempotency** | Retries seguros — mesma operação, mesmo resultado |

---

## Observabilidade — Os 3 Pilares

| Pilar | Captura | Serve Para |
|-------|---------|------------|
| **Logs** | Eventos discretos | Debug, auditoria |
| **Métricas** | Valores numéricos ao longo do tempo | Alertas, tendências |
| **Traces** | Fluxo de request entre serviços | Gargalos, latência |

**SLI/SLO/SLA:**
- **SLI** = métrica que mede o serviço (ex: latência p99 < 200ms)
- **SLO** = objetivo interno (99.9% das requests < 200ms)
- **SLA** = compromisso com cliente (se violar, há penalidade)

---

## API-First — Contrato Antes de Código

1. Defina o contrato (OpenAPI/Swagger) **antes** de implementar
2. URLs = recursos (substantivos), verbos HTTP = ações
3. Versionamento obrigatório (v1, v2)
4. Rate limiting, paginação e autenticação desde o dia 1
5. Erros padronizados (RFC 9457 — Problem Details)
6. API Gateway como ponto único de entrada

---

## Multi-Tenancy — Modelos SaaS

| Modelo | Isolamento | Custo | Quando Usar |
|--------|-----------|-------|-------------|
| **Silo** (dedicado) | Máximo | Alto | Compliance rigoroso, dados sensíveis |
| **Bridge** (schema/banco) | Alto | Médio | Equilíbrio isolamento/custo |
| **Pool** (tenant_id) | Médio | Baixo | Scale, muitos tenants |

**Problemas críticos:** Noisy Neighbor (um tenant monopoliza recursos) e Data Sovereignty (dados na jurisdição correta).

---

## Cloud Native — 12-Factor App (Resumo)

| Fator | Regra |
|-------|-------|
| Config | No ambiente (env vars), nunca no código |
| Dependencies | Declaradas explicitamente |
| Processes | Stateless — estado em backing services |
| Backing Services | Substituíveis via config (banco, cache, fila) |
| Logs | Stream para stdout |
| Build/Release/Run | Separados, releases imutáveis |
| Disposability | Startup rápido, shutdown gracioso |

---

## Infrastructure as Code — Princípios

- **Declarativo** — defina estado desejado, ferramenta converge
- **Versionado** — tudo em Git, cada mudança rastreável
- **Idempotente** — aplicar N vezes = mesmo resultado
- **Imutável** — substitua servidores, não modifique
- **Secrets** — nunca em plaintext, use Vault/AWS Secrets Manager
- **GitOps** — Git como single source of truth, deploy via PR

---

## Compliance (GDPR/LGPD) — Privacy by Design

| Princípio | Impacto Técnico |
|-----------|----------------|
| **Data Minimization** | Colete apenas o estritamente necessário |
| **Purpose Limitation** | Dados usados apenas para o fim declarado |
| **Privacy by Default** | Config padrão = mais privada possível |
| **Right to Erasure** | Capacidade técnica de deletar tudo de um usuário |
| **Data Portability** | Exportar dados em formato legível por máquina |
| **Audit Trail** | Log completo de operações sobre dados pessoais |
| **Consent Management** | Consentimento granular, armazenado e gerenciável |

---

## Guia de Decisão

```
Novo sistema?
├── Precisa de segurança rigorosa     → Security by Design + Zero Trust
├── Múltiplos clientes (SaaS)        → Multi-Tenancy (escolha modelo)
├── Dados pessoais (BR/EU)           → Privacy by Design (LGPD/GDPR)
├── Vai para cloud                   → 12-Factor + IaC + Well-Architected
├── Alta disponibilidade             → Resiliência (Circuit Breaker, Retry)
├── APIs para terceiros              → API-First + Contract-First
└── Precisa diagnosticar problemas   → Observabilidade (Logs, Metrics, Traces)

Sistema existente com problemas?
├── Cai quando um serviço falha      → Circuit Breaker + Bulkhead
├── Lento sob carga                  → Cache + Horizontal Scaling
├── Difícil de debugar               → Observabilidade + Correlation IDs
├── Infra manual, propenso a erro    → IaC + GitOps
├── Dados sem controle               → Compliance + Data Governance
└── Vulnerabilidades recorrentes     → Security by Design + Input Validation
```
