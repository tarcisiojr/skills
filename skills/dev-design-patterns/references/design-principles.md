# Princípios de Design — Referência Detalhada

Baseado em: Robert C. Martin (Clean Code), Kent Beck, Martin Fowler

## Índice
1. [Clean Code Completo](#clean-code)
2. [SOLID com Exemplos](#solid)
3. [DRY, KISS, YAGNI](#dry-kiss-yagni)
4. [Regras de Kent Beck](#kent-beck)
5. [Lei de Demeter](#lei-de-demeter)
6. [Code Smells](#code-smells)

---

## Clean Code

### Regras de Nomenclatura
- Nomes descritivos e pronunciáveis — `userAccountStatus`, não `usrAccSt`
- Nomes pesquisáveis — evite `i`, `x`, `temp`
- Substitua números mágicos por constantes — `MAX_LOGIN_ATTEMPTS = 5`
- Sem codificação de tipo no nome — não use notação húngara (`strName`)
- Classes = substantivos (`UserService`), métodos = verbos (`calculateTotal`)
- Evite nomes genéricos — `data`, `info`, `manager` quase nunca são bons

### Regras de Funções
- **Pequenas** — máximo 20-25 linhas; se não cabe na tela, é grande demais
- **Uma responsabilidade** — se precisar de "e" para descrever, divida
- **Poucos argumentos** — 0-2 ideal, máx 3. Mais que isso → extraia objeto
- **Sem flag arguments** — `render(true)` é obscuro; crie `renderForSuite()` e `renderForSingle()`
- **Sem efeitos colaterais** — `checkPassword()` não deve resetar sessão
- **Command-Query Separation** — função retorna valor OU muda estado, nunca ambos

### Regras de Comentários
- **Bons:** explicam PORQUÊ, avisos, TODOs com tracking
- **Ruins:** explicam O QUÊ (o código deveria ser autoexplicativo)
- **Código comentado:** delete — git é seu backup
- Se precisa de comentário para explicar, reescreva o código

### Regras de Design
- Dados configuráveis em níveis altos (não hardcode)
- Prefira polimorfismo a if/else ou switch/case
- Use injeção de dependência
- Lei de Demeter: objeto conhece apenas vizinhos diretos
- Separe código de construção (setup) de código de uso

---

## SOLID

### SRP — Princípio da Responsabilidade Única

**Uma classe tem apenas UM motivo para mudar.**

```
❌ Ruim: classe UserManager
├── createUser()        → persistência
├── sendWelcomeEmail()  → notificação
├── generateReport()    → relatório
└── validateCPF()       → validação

✅ Bom: responsabilidades separadas
├── UserService         → orquestra criação
├── UserRepository      → persistência
├── EmailService        → notificação
├── ReportGenerator     → relatórios
└── CPFValidator        → validação
```

**Sinal de violação:** classe com "And" ou "Manager" no nome; arquivo com 500+ linhas.
**Quando relaxar:** módulos muito pequenos onde separação criaria indireção desnecessária.

### OCP — Princípio Aberto/Fechado

**Aberto para extensão, fechado para modificação.**

```
❌ Ruim: if/elif que cresce a cada novo tipo
if payment_type == "credit":
    process_credit()
elif payment_type == "debit":
    process_debit()
elif payment_type == "pix":  # Modificação!
    process_pix()

✅ Bom: novo tipo = nova classe
interface PaymentProcessor:
    process(amount)

class CreditProcessor(PaymentProcessor): ...
class DebitProcessor(PaymentProcessor): ...
class PixProcessor(PaymentProcessor): ...  # Extensão!
```

**Sinal de violação:** cadeia de if/elif que cresce; precisar modificar código existente para adicionar funcionalidade.
**Quando relaxar:** CRUD simples onde polimorfismo seria overengineering.

### LSP — Princípio de Substituição de Liskov

**Subtipos substituíveis por seus tipos base sem quebrar o programa.**

```
❌ Violação clássica:
class Rectangle:
    setWidth(w)
    setHeight(h)

class Square(Rectangle):  # Square herda Rectangle
    setWidth(w):
        self.width = w
        self.height = w  # Efeito colateral! Viola contrato

✅ Correto: hierarquia que respeita contratos
class Shape(ABC):
    area() -> float

class Rectangle(Shape): ...
class Square(Shape): ...
```

**Sinal de violação:** subclasse lança exceção em método herdado; subclasse ignora comportamento do pai.
**Raramente relaxe** — violações de LSP são quase sempre bugs de design.

### ISP — Princípio da Segregação de Interface

**Clientes não dependem de interfaces que não usam.**

```
❌ Interface "Deus":
interface Worker:
    work()
    eat()
    sleep()
    code()
    managePeople()
# Robôs não comem, estagiários não gerenciam

✅ Interfaces segregadas:
interface Workable: work()
interface Feedable: eat()
interface Manageable: managePeople()
```

**Sinal de violação:** implementador deixa métodos vazios ou lançando NotImplementedError.
**Quando relaxar:** interfaces com 2-3 métodos coesos não precisam ser divididas.

### DIP — Princípio da Inversão de Dependência

**Módulos de alto nível não dependem de baixo nível. Ambos dependem de abstrações.**

```
❌ Dependência direta:
class OrderService:
    def __init__(self):
        self.db = MySQLConnection()  # Acoplamento!

✅ Dependência invertida:
class OrderService:
    def __init__(self, repository: OrderRepository):  # Abstração!
        self.repository = repository
```

**Sinal de violação:** `new ConcreteClass()` ou `import concrete_module` dentro de lógica de negócio.
**Quando relaxar:** scripts simples sem necessidade de troca de implementação.

---

## DRY, KISS, YAGNI

### DRY — Don't Repeat Yourself
- Cada conhecimento: representação única e autoritativa
- **Duplicação real:** mesma lógica de validação em 3 controllers → extraia middleware
- **Duplicação acidental:** código parecido mas com razões de mudança diferentes → NÃO elimine, cria acoplamento
- **Regra dos 3:** tolerável em 2 lugares; no 3º, extraia

### KISS — Keep It Simple
- A solução mais simples que funciona é a melhor
- Código "inteligente" = código difícil de debugar
- "Qualquer tolo pode escrever código que um computador entende. Bons programadores escrevem código que humanos entendem." — Fowler
- **Violação:** Strategy + Factory + Observer para um CRUD de 3 campos

### YAGNI — You Ain't Gonna Need It
- Implemente apenas o necessário AGORA
- 80% das features "futuras" nunca são usadas
- Código especulativo = custo sem retorno
- **Exceção:** decisões arquiteturais caras de reverter (banco, protocolo, linguagem)

---

## Kent Beck — Regras de Design Simples

Em ordem de prioridade:

1. **Passa nos testes** — funciona como esperado. Prioridade máxima. Nunca sacrifique por elegância.
2. **Revela intenção** — fácil de entender. Nomes claros, estrutura óbvia.
3. **Sem duplicação** — DRY. Eliminar duplicação frequentemente leva a bons designs emergentes.
4. **Mínimo de elementos** — menor número de classes e métodos. Nunca adicione abstração "para organizar".

---

## Lei de Demeter

"Não fale com estranhos." Um método de um objeto deveria chamar apenas:
- Métodos do próprio objeto
- Métodos de objetos recebidos como parâmetro
- Métodos de objetos criados dentro do método
- Métodos de objetos componentes diretos

```
❌ Violação (train wreck):
user.getAddress().getCity().getZipCode()

✅ Correto:
user.getZipCode()  // User delega internamente
```

---

## Code Smells

| Smell | Indica | Refatoração |
|-------|--------|-------------|
| Funções longas (50+ linhas) | Responsabilidades demais | Extract Method |
| Muitos parâmetros (4+) | Falta de abstração | Introduce Parameter Object |
| Classes grandes (500+ linhas) | God Class | Extract Class + SRP |
| Feature Envy | Método usa mais dados de outra classe | Move Method |
| Data Clumps | Grupos de dados sempre juntos | Extract Class / Value Object |
| Primitive Obsession | Primitivos para conceitos de domínio | Value Objects |
| Divergent Change | Uma classe muda por N razões | SRP + Extract Class |
| Shotgun Surgery | Uma mudança = N arquivos | Consolide lógica |
| Dead Code | Código nunca executado | Delete |
| Speculative Generality | Abstrações "para o futuro" | YAGNI — delete |
