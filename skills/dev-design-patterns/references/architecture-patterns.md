# Padrões Arquiteturais — Referência Detalhada

Baseado em: Robert C. Martin, Alistair Cockburn, Eric Evans, Adam Wiggins

## Índice
1. [Clean Architecture](#clean-architecture)
2. [Hexagonal / Ports & Adapters](#hexagonal)
3. [MVC, MVVM e Variantes](#mvc-mvvm)
4. [Domain-Driven Design](#ddd)
5. [Repository e Service Layer](#repository-service-layer)
6. [CQRS e Event Sourcing](#cqrs-event-sourcing)
7. [Microsserviços](#microsserviços)
8. [Twelve-Factor App](#twelve-factor-app)

---

## Clean Architecture

### Camadas (de dentro para fora)

1. **Entities** — Regras de negócio da empresa. Sem dependências externas.
2. **Use Cases** — Regras da aplicação. Orquestram entidades. Não conhecem UI/banco/framework.
3. **Interface Adapters** — Controllers, Presenters, Gateways. Convertem formatos.
4. **Frameworks & Drivers** — Banco, web framework, UI. Detalhes substituíveis.

### A Regra de Dependência
- Dependências de código SEMPRE apontam para dentro
- Camadas internas NUNCA conhecem externas
- Dados cruzam fronteiras como DTOs, nunca como entidades de framework

### Quando NÃO Usar
- CRUD simples sem lógica de negócio significativa
- Projetos pequenos com vida útil curta
- Protótipos/MVPs onde velocidade > arquitetura

**Violação comum:** Entidade com anotações ORM → crie modelo separado para persistência.

---

## Hexagonal

### Componentes
- **Core (Hexágono)** — Lógica de negócio pura
- **Portas de Entrada (Driving)** — Interfaces de acesso ao core (API, CLI, eventos)
- **Portas de Saída (Driven)** — Interfaces do core para infraestrutura (DB, APIs externas)
- **Adaptadores** — Implementações concretas das portas

### Quando Usar
- Múltiplas integrações externas
- Testabilidade é prioridade
- Previsão de trocar tecnologias

### Quando NÃO
- CRUDs simples ou protótipos
- Prazo curto com escopo pequeno

### Clean vs Hexagonal vs Onion
São variações do mesmo princípio (DIP). Não são fundamentalmente diferentes.

| Aspecto | Hexagonal | Onion | Clean |
|---------|-----------|-------|-------|
| Foco | Flexibilidade com sistemas externos | Domínio como centro | Use cases + separação |
| Melhor para | Muitas integrações | DDD com domínio rico | Lógica complexa e testável |

Escolha a terminologia que sua equipe conhece.

---

## MVC, MVVM

### MVC
- **Quando:** APIs REST, backends tradicionais
- **Forte:** Alinha com HTTP request/response
- **Fraco:** Controllers tendem a crescer (Fat Controller)

### MVVM
- **Quando:** SPAs com data binding (React, Vue, Angular)
- **Forte:** Separação UI/lógica, ViewModel testável
- **Fraco:** Boilerplate para telas simples

---

## DDD

### Padrões Estratégicos
- **Bounded Context** — Fronteira onde modelo é válido
- **Ubiquitous Language** — Linguagem compartilhada devs + negócio
- **Context Map** — Como bounded contexts se relacionam

### Padrões Táticos
| Padrão | O que é |
|--------|---------|
| **Entity** | Objeto com identidade única (Usuário, Pedido) |
| **Value Object** | Imutável, definido por atributos (Dinheiro, Email, CPF) |
| **Aggregate** | Cluster de entidades como unidade transacional |
| **Repository** | Acesso a dados para aggregates |
| **Domain Service** | Lógica entre múltiplos aggregates |
| **Domain Event** | Algo significativo que aconteceu no domínio |
| **Factory** | Criação complexa com lógica de negócio |

### Quando NÃO Usar DDD
- Domínios CRUD simples
- Sem acesso a especialistas de domínio
- Lógica trivial

**Regra:** DDD rigoroso apenas no Core Domain. CRUD para subdomínios de suporte.

---

## Repository e Service Layer

### Controller → Service → Repository
```
[Controller] → Recebe request, valida input básico
       ↓
[Service]    → Lógica de negócio, transações, orquestração
       ↓
[Repository] → Acesso a dados, queries, persistência
```

### Repository
- Interface tipo coleção para objetos de domínio
- Isola lógica de negócio do banco
- Facilita testes com mocks
- **Evite:** GenericRepository<T> para tudo — crie interfaces específicas

### Service Layer
- Ponto único de entrada para operações de negócio
- Reutilizável por diferentes interfaces (API, CLI, eventos)
- **Evite:** Services com lógica de acesso a dados

### Violações Comuns (Responsibility Bleed)
- Controller com lógica de negócio → mova para Service
- Repository com validação → mova para Service
- Service com `new Repository()` → injeção de dependência

---

## CQRS e Event Sourcing

### CQRS
Separa modelo de leitura (Query) do de escrita (Command).

**Quando usar:** Reads >> writes; modelos de leitura/escrita muito diferentes; escala independente.
**Quando NÃO:** CRUD simples; equipes inexperientes; consistência forte em tempo real.

### Event Sourcing
Armazena estado como sequência de eventos imutáveis.

**Quando usar:** Auditoria legal; "viagem no tempo"; domínios naturalmente event-driven (financeiro).
**Quando NÃO:** Sem necessidade de histórico; lógica trivial; equipes inexperientes.

**Armadilha:** CQRS + Event Sourcing juntos = complexidade significativa. Use CQRS sozinho primeiro.

---

## Microsserviços

### Padrões Essenciais
| Padrão | Resolve |
|--------|---------|
| API Gateway | Ponto único de entrada |
| Service Discovery | Serviços se encontram dinamicamente |
| Database per Service | Desacopla persistência |
| Saga | Transações distribuídas com compensação |
| Strangler Fig | Migração incremental de monolito |

### Quando Usar
- Equipes grandes com deploy independente
- Bounded contexts claros
- Escala independente de partes do sistema

### Quando NÃO
- Equipes pequenas (< 5 devs)
- MVP ou startup em fase inicial
- Sem expertise em sistemas distribuídos

**Regra:** Comece com monolito modular. Extraia microsserviços quando a dor justificar.

---

## Twelve-Factor App

| # | Fator | Regra |
|---|-------|-------|
| 1 | **Codebase** | Um repo, muitos deploys |
| 2 | **Dependencies** | Declaradas explicitamente |
| 3 | **Config** | No ambiente (env vars) |
| 4 | **Backing Services** | Recursos substituíveis via config |
| 5 | **Build/Release/Run** | Estágios separados, releases imutáveis |
| 6 | **Processes** | Stateless |
| 7 | **Port Binding** | App auto-contida |
| 8 | **Concurrency** | Escale com processos |
| 9 | **Disposability** | Startup rápido, shutdown gracioso |
| 10 | **Dev/Prod Parity** | Ambientes similares |
| 11 | **Logs** | Stream para stdout |
| 12 | **Admin Processes** | Mesmo código e ambiente |
