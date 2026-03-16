---
name: dev-design-patterns
description: >
  Skill completa sobre padrões de projeto, princípios de design e arquitetura
  de software para código bem estruturado. Cobre Clean Code (Uncle Bob), SOLID,
  DRY/KISS/YAGNI, GoF Design Patterns, Clean Architecture, Hexagonal, DDD,
  Repository/Service Layer, CQRS, TDD, Twelve-Factor App, anti-padrões e
  padrões de resiliência. Baseada em Robert C. Martin, Martin Fowler, Kent Beck,
  Eric Evans, Gang of Four e práticas reconhecidas pela comunidade. Use esta
  skill SEMPRE que o usuário estiver projetando arquitetura, refatorando código,
  discutindo organização de projeto, revisando código, ou pedindo ajuda com
  estrutura. Acione também quando mencionar: design patterns, padrões de projeto,
  SOLID, Clean Code, Clean Architecture, DDD, hexagonal, repository pattern,
  service layer, CQRS, TDD, anti-padrões, code smells, refatoração, acoplamento,
  coesão, inversão de dependência, composição vs herança, ou qualquer discussão
  sobre como organizar e estruturar código de forma profissional.
---

# Dev Design Patterns — Padrões de Projeto e Arquitetura de Software

## Filosofia Central

> "A melhor arquitetura é a mais simples que resolve o problema atual e permite evolução futura."

Quatro regras de Kent Beck, em ordem de prioridade:
1. **Passa nos testes** — funciona como esperado
2. **Revela intenção** — fácil de entender
3. **Sem duplicação** — cada conceito em um lugar
4. **Mínimo de elementos** — menor número de abstrações necessárias

Antes de adicionar qualquer padrão ou abstração, pergunte: *o problema é real ou hipotético?*

## Quando Consultar as Referências

| Preciso de...                                         | Consultar                                |
|-------------------------------------------------------|------------------------------------------|
| Clean Code, SOLID, DRY/KISS/YAGNI, Kent Beck          | `references/design-principles.md`        |
| GoF patterns, composição vs herança, DI, refatoração   | `references/design-patterns.md`          |
| Clean/Hexagonal Architecture, DDD, CQRS, 12-Factor    | `references/architecture-patterns.md`    |
| Testes, resiliência, cache, observabilidade, APIs      | `references/testing-resilience.md`       |

Leia a referência relevante quando precisar de detalhes ou exemplos.

---

## Princípios Invioláveis

### 1. Clean Code — Código que Humanos Entendem

Código é lido 10x mais do que escrito. O objetivo é clareza, não esperteza.

- **Nomes descritivos** — `calculateTotalPrice`, não `calc` ou `x`
- **Funções pequenas** — máx 20-25 linhas, uma responsabilidade
- **Poucos argumentos** — 0-2 ideal, máx 3. Muitos = extraia objeto
- **Sem efeitos colaterais** — função faz o que o nome diz, nada mais
- **Sem números mágicos** — `MAX_RETRIES = 3`, não `3` solto no código
- **Regra do Escoteiro** — deixe o código mais limpo do que encontrou

### 2. SOLID — A Base de Código Extensível

| Princípio | Regra Prática | Sinal de Violação |
|-----------|---------------|-------------------|
| **SRP** | Uma classe, um motivo para mudar | Classe com "And" no nome |
| **OCP** | Estenda via novos tipos, não if/else | Cadeia de if/elif que cresce |
| **LSP** | Subtipo substituível pelo tipo base | Subclasse lança exceção em método herdado |
| **ISP** | Interfaces pequenas e focadas | Implementador deixa métodos vazios |
| **DIP** | Dependa de abstrações, não implementações | `new ConcreteClass()` dentro de lógica de negócio |

### 3. DRY, KISS, YAGNI — O Trio da Simplicidade

- **DRY** — Cada conhecimento tem representação única no sistema. Mas: duplicação *acidental* (código parecido com razões de mudança diferentes) não precisa ser eliminada — forçar DRY entre contextos cria acoplamento.
- **KISS** — A solução mais simples que funciona é a melhor. Código "inteligente" é código difícil de debugar.
- **YAGNI** — Implemente apenas o necessário agora. 80% das features "futuras" nunca são usadas. Exceção: decisões arquiteturais caras de reverter (escolha de banco, protocolo).

### 4. Composição sobre Herança

Herança cria acoplamento forte, hierarquias frágeis e explosão de classes. Reserve herança para relações genuínas IS-A com hierarquias estáveis (máx 2-3 níveis).

Use composição (HAS-A) quando:
- Comportamento precisa mudar em runtime
- Reutilização entre classes não relacionadas
- Testabilidade é prioridade

**Regra:** Na dúvida entre herança e composição, escolha composição.

---

## Padrões GoF Mais Relevantes (2025-2026)

| Padrão | Relevância | Resolve |
|--------|-----------|---------|
| **Strategy** | Muito alta | Algoritmos intercambiáveis (validação, auth, pricing) |
| **Observer** | Muito alta | Eventos, pub/sub, UI reativa, webhooks |
| **Factory Method** | Alta | Criação com lógica condicional complexa |
| **Builder** | Alta | Objetos com muitos parâmetros opcionais |
| **Adapter** | Alta | Integração com APIs de terceiros / legado |
| **Decorator** | Alta | Adicionar comportamento dinamicamente (middleware) |
| **Facade** | Alta | Simplificar API complexa |
| **Command** | Alta | Undo/redo, filas, logging de ações |
| **Proxy** | Alta | Cache, lazy loading, controle de acesso |

Padrões que **perderam relevância**: Visitor, Memento, Mediator, Flyweight — substituídos por abordagens mais modernas (event sourcing, state management, eventos desacoplados).

---

## Arquiteturas — Quando Usar Qual

| Cenário | Arquitetura | Porquê |
|---------|-------------|--------|
| CRUD simples | MVC + Repository | Suficiente, sem overhead |
| Domínio complexo | Clean/Hexagonal + DDD | Isola negócio de infraestrutura |
| Múltiplas integrações | Hexagonal (Ports & Adapters) | Adaptadores substituíveis |
| Alta escala reads >> writes | CQRS | Modelos otimizados para cada operação |
| Auditoria/compliance | Event Sourcing | Histórico completo e imutável |
| Equipes grandes | Microsserviços + Bounded Contexts | Deploy independente |
| SPA com dados complexos | MVVM + GraphQL | Data binding + queries flexíveis |

**Regra de ouro:** Clean, Hexagonal e Onion são variações do mesmo princípio — inversão de dependência. Não são padrões fundamentalmente diferentes. Escolha a terminologia que sua equipe conhece.

---

## Camadas Padrão (Controller → Service → Repository)

```
[Controller/Handler] → Recebe request, valida input básico
        ↓
[Service Layer]      → Lógica de negócio, transações, orquestração
        ↓
[Repository]         → Acesso a dados, queries, persistência
```

**Violações comuns:**
- Controller com lógica de negócio → mova para Service
- Repository com validação de negócio → mova para Service
- Service instanciando dependência com `new` → use injeção de dependência

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

- Teste **comportamento**, não implementação
- Padrão AAA: Arrange → Act → Assert
- Testes frágeis que quebram com refatoração = testando implementação
- TDD para lógica de negócio complexa; BDD quando stakeholders participam

---

## Anti-Padrões Fatais

| Anti-Padrão | Sinal | Correção |
|-------------|-------|----------|
| **God Class** | Classe com 500+ linhas que faz tudo | SRP + Extract Class |
| **Fat Controller** | Controller com lógica de negócio | Service Layer |
| **Anemic Domain** | Entidades só com getters/setters | Mova lógica para entidades |
| **Distributed Monolith** | Microsserviços acoplados | Bounded contexts independentes |
| **Primitive Obsession** | Email como string, dinheiro como float | Value Objects |
| **Shotgun Surgery** | Uma mudança = N arquivos | Consolide lógica (SRP) |
| **Golden Hammer** | Mesmo padrão para tudo | Avalie cada problema |
| **Premature Optimization** | Otimizar antes de medir | "Meça primeiro, otimize depois" |

---

## Twelve-Factor App (Resumo)

Para aplicações SaaS modernas e cloud-native:

| # | Fator | Regra Prática |
|---|-------|---------------|
| 1 | Codebase | Um repo por app, config diferencia ambientes |
| 2 | Dependencies | Declaradas explicitamente, nunca implícitas |
| 3 | Config | No ambiente (env vars), nunca no código |
| 4 | Backing Services | Banco/cache/fila = recursos substituíveis via config |
| 5 | Build/Release/Run | Estágios separados, releases imutáveis |
| 6 | Processes | Stateless — persista em backing services |
| 7 | Port Binding | App auto-contida, exporta via porta |
| 8 | Concurrency | Escale horizontalmente (processos) |
| 9 | Disposability | Startup rápido, shutdown gracioso |
| 10 | Dev/Prod Parity | Minimize diferenças entre ambientes |
| 11 | Logs | Stream para stdout, colete externamente |
| 12 | Admin Processes | Migrations/scripts = mesmo código e ambiente |

---

## Guia de Decisão Rápida

```
Código existente com problemas?
├── Classes enormes           → SRP + Extract Class
├── Difícil de testar         → DI + Repository Pattern
├── Duplicação                → DRY + Extract Method
├── Herança profunda          → Composição sobre Herança
├── Lógica espalhada          → Service Layer + Domain Model
├── Acoplamento forte         → Interfaces + DIP + Eventos
├── Controller gordo          → Mova lógica para Service
└── if/elif crescente         → Strategy Pattern ou Polimorfismo
```

**Checklist antes de adicionar complexidade:**
- O problema é REAL (não hipotético)?
- A solução simples foi tentada primeiro?
- A equipe entende o padrão?
- O custo de manutenção vale o benefício?
- É possível adicionar depois se necessário?

Se qualquer resposta for "não", pare e reconsidere.
