# Design Patterns — Referência Detalhada

Baseado em: Gang of Four, Martin Fowler (Refactoring)

## Índice
1. [Padrões Criacionais](#criacionais)
2. [Padrões Estruturais](#estruturais)
3. [Padrões Comportamentais](#comportamentais)
4. [Composição sobre Herança](#composição-sobre-herança)
5. [Injeção de Dependência](#injeção-de-dependência)
6. [Refatorações Essenciais](#refatorações)

---

## Criacionais

### Factory Method
**Problema:** Criação de objetos com lógica condicional complexa; código cliente não deveria saber qual classe concreta criar.
**Quando usar:** Frameworks que precisam instanciar objetos definidos pelo usuário; criação baseada em configuração/tipo.
**Quando NÃO:** Objetos simples com `new` direto.

### Builder
**Problema:** Objeto com muitos parâmetros opcionais; construtor telescópico.
**Quando usar:** Configurações complexas (queries SQL, HTTP requests, documentos).
**Quando NÃO:** Objetos com 1-3 campos obrigatórios.

### Singleton
**Relevância:** BAIXA — quase sempre prefira injeção de dependência.
**Únicos usos legítimos:** Pool de conexões, configuração global read-only, logger.
**Problemas:** Estado global oculto, difícil de testar, acoplamento invisível.

---

## Estruturais

### Adapter
**Problema:** Interface incompatível com o que o cliente espera.
**Quando usar:** Integrar API de terceiros; adaptar código legado a nova interface.
**Quando NÃO:** Quando você controla ambas as interfaces.

### Decorator
**Problema:** Adicionar responsabilidades a objetos dinamicamente sem herança.
**Quando usar:** Middleware (logging, auth, cache), streams com transformações empilháveis.
**Quando NÃO:** Quando composição simples resolve.

### Facade
**Problema:** Sistema complexo com muitas interfaces interdependentes.
**Quando usar:** Simplificar acesso a subsistemas (SDK wrapping, API gateway).
**Quando NÃO:** Quando já existe interface simples.

### Proxy
**Problema:** Controlar acesso ou adicionar funcionalidade ao acessar um objeto.
**Quando usar:** Cache (caching proxy), lazy loading (virtual proxy), controle de acesso (protection proxy).
**Quando NÃO:** Overhead desnecessário em objetos leves.

---

## Comportamentais

### Strategy
**Problema:** Família de algoritmos intercambiáveis.
**Quando usar:** Validação com regras variáveis, métodos de pagamento, algoritmos de ordenação, estratégias de pricing.
**Quando NÃO:** Quando há apenas 1 algoritmo e não há previsão de mudança.
**Dica moderna:** Em linguagens com funções de primeira classe, funções/lambdas substituem classes Strategy.

### Observer
**Problema:** Notificar múltiplos objetos quando estado muda.
**Quando usar:** Sistemas de eventos, UI reativa, webhooks, pub/sub.
**Quando NÃO:** Fluxo síncrono simples; cuidado com cascatas de notificação.

### Command
**Problema:** Encapsular operação como objeto para desacoplar invocação de execução.
**Quando usar:** Undo/redo, filas de tarefas, logging de ações, transações.
**Quando NÃO:** Operações simples sem necessidade de reversão ou enfileiramento.

### State
**Problema:** Objeto muda comportamento baseado em estado interno.
**Quando usar:** Máquinas de estado (pedido, workflow, jogo, UI).
**Quando NÃO:** Estados simples com 2-3 transições (if/else basta).

### Template Method
**Problema:** Algoritmo com estrutura fixa mas passos variáveis.
**Quando usar:** Frameworks com hook methods.
**Quando NÃO:** Prefira Strategy/Composition na maioria dos casos modernos.

---

## Composição sobre Herança

### Quando Usar Herança (IS-A)
- Relação genuína "é um" que é estável
- Máximo 2-3 níveis de profundidade
- A hierarquia é improvável de mudar
- Framework exige (ex: Android Activity)

### Quando Usar Composição (HAS-A)
- Relação "tem um" ou "usa um"
- Comportamento muda em runtime
- Reutilização entre classes não relacionadas
- Testabilidade é prioridade (mocks são triviais)

### Problemas da Herança
- **Explosão de classes:** N dimensões = N^x subclasses
- **Fragilidade:** Mudança no pai quebra filhos inesperadamente
- **Acoplamento forte:** Filhos dependem da implementação interna do pai
- **Rigidez:** Não muda comportamento em runtime

### Regra Prática
Na dúvida entre herança e composição → composição. Reserve herança para frameworks e hierarquias genuinamente estáveis.

---

## Injeção de Dependência

### Tipos (em ordem de preferência)

| Tipo | Como | Quando |
|------|------|--------|
| **Constructor Injection** | Via construtor | Sempre — garante objeto completo |
| **Setter Injection** | Via método set | Dependências opcionais |
| **Interface Injection** | Contrato de injeção | Raro, evitar |

### Boas Práticas
- Constructor injection como padrão
- Muitas dependências no construtor = violação de SRP → divida a classe
- Evite Service Locator (anti-pattern) — esconde dependências
- Não instancie dependências internamente (`new`) — injete de fora
- Use o container DI do framework quando disponível

### Quando NÃO Usar
- Scripts simples sem necessidade de testabilidade
- Funções puras sem dependências externas
- Quando introduz complexidade desproporcional ao benefício

---

## Refatorações Essenciais (Martin Fowler)

Refatoração é melhorar design sem mudar comportamento. Pequenas transformações seguras que acumulam grandes melhorias.

| Refatoração | Quando Aplicar |
|---|---|
| **Extract Method** | Método faz múltiplas coisas; código muito longo |
| **Extract Class** | Classe com responsabilidades demais |
| **Inline Method** | Corpo tão claro quanto o nome |
| **Rename** | Nome não revela intenção |
| **Introduce Parameter Object** | Muitos parâmetros relacionados |
| **Replace Conditional with Polymorphism** | if/else que escolhe por tipo |
| **Move Method** | Método usa mais dados de outra classe |
| **Replace Magic Number with Constant** | Número literal sem significado |
| **Replace Temp with Query** | Variável temporária cacheia expressão |
| **Extract Interface** | Múltiplas classes com métodos comuns |

**Regra chave:** Cada refatoração é "pequena demais para valer a pena" individualmente. O valor está na composição de muitas transformações pequenas e seguras, sempre com testes passando.
