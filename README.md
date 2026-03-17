# Skills

Coleção pessoal de skills para agentes de IA (Claude Code, Copilot, OpenCode, Gemini, Cursor, etc.).

Skills seguem o formato [Agent Skills](https://agentskills.io/) e podem ser instaladas via [`npx skills`](https://github.com/vercel-labs/skills).

## Instalação

```bash
# Instalar skills (modo interativo)
npx skills add tarcisiojr/skills

# Listar skills disponíveis no repositório
npx skills add tarcisiojr/skills --list

# Instalar skill específica
npx skills add tarcisiojr/skills --skill dev-python

# Instalar múltiplas skills
npx skills add tarcisiojr/skills --skill dev-python --skill dev-design-patterns

# Instalar globalmente (disponível em todos os projetos)
npx skills add tarcisiojr/skills --skill dev-python -g

# Instalar para agentes específicos
npx skills add tarcisiojr/skills -a claude-code -a opencode

# Instalar todas as skills para todos os agentes
npx skills add tarcisiojr/skills --all

# Instalação não-interativa (CI/CD friendly)
npx skills add tarcisiojr/skills --skill dev-python -g -a claude-code -y
```

### Formatos de origem suportados

```bash
# GitHub shorthand (owner/repo) - recomendado
npx skills add tarcisiojr/skills

# URL completa do GitHub
npx skills add https://github.com/tarcisiojr/skills

# URL git via SSH
npx skills add git@github.com:tarcisiojr/skills.git

# Caminho local
npx skills add ./caminho-local
```

### Outros comandos

| Comando | Descrição |
|---------|-----------|
| `npx skills list` | Listar skills instaladas |
| `npx skills find [query]` | Buscar skills por palavra-chave |
| `npx skills remove [skills]` | Remover skills instaladas |
| `npx skills check` | Verificar atualizações disponíveis |
| `npx skills update` | Atualizar todas as skills |
| `npx skills init [name]` | Criar template de SKILL.md |

## Skills Disponíveis

| Skill | Descrição |
|-------|-----------|
| [dev-python](skills/dev-python/) | Desenvolvimento Python com boas práticas, estilo Pythônico e padrões modernos. Baseada em Fluent Python, Effective Python, PEPs oficiais e ferramentas modernas (ruff, mypy, pytest, uv). |
| [dev-design-patterns](skills/dev-design-patterns/) | Padrões de projeto, princípios de design e arquitetura de software. Cobre Clean Code, SOLID, GoF, Clean Architecture, Hexagonal, DDD, CQRS e TDD. |
| [dev-architecture-principles](skills/dev-architecture-principles/) | Princípios de arquitetura de sistemas modernos — segurança by design, escalabilidade, resiliência, observabilidade, API-First, multi-tenancy SaaS e cloud native. |
| [rest-api-design](skills/rest-api-design/) | Design de APIs REST seguindo convenções padronizadas. Define padrões de nomenclatura, status codes, envelopes de erro, paginação e versionamento. |

## Sincronização com `skills-sync`

CLI Python para escanear skills instaladas localmente por qualquer agente de IA e sincronizá-las com este repositório.

### Instalação

```bash
# Criar venv e instalar
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
```

### Uso

```bash
# Listar agentes detectados na máquina
skills-sync agents

# Listar skills já no repositório
skills-sync list

# Escanear todos os agentes e escolher quais sincronizar (interativo)
skills-sync scan

# Escanear apenas um agente específico
skills-sync scan --agent claude-code

# Sincronizar tudo sem confirmação
skills-sync scan --yes

# Ver o que seria feito sem executar
skills-sync scan --dry-run

# Filtrar por nome da skill
skills-sync scan --skill learning

# Escanear apenas diretórios globais (sem projetos)
skills-sync scan --global-only

# Escanear projetos em diretório específico
skills-sync scan --projects-dir ~/Projetos
```

Agentes suportados: Claude Code, Codex, Gemini CLI, GitHub Copilot, Cursor, OpenCode, Windsurf, Roo Code, Continue, Aider, Cline, e 30+ outros.

## Estrutura

```
skills/
├── pyproject.toml                # CLI skills-sync
├── src/skills_sync/              # Código-fonte do CLI
├── tests/                        # Testes automatizados
├── skills/
│   ├── dev-python/               # Desenvolvimento Python
│   ├── dev-design-patterns/      # Padrões de projeto e arquitetura de software
│   ├── dev-architecture-principles/ # Princípios de arquitetura de sistemas
│   └── rest-api-design/          # Design de APIs REST
└── README.md
```

Cada skill contém um `SKILL.md` (definição principal) e opcionalmente um diretório `references/` com documentação detalhada.

## Como criar uma nova skill

Cada skill é um diretório dentro de `skills/` contendo um `SKILL.md` com frontmatter YAML:

```yaml
---
name: minha-skill
description: >
  Descrição clara de quando e como a skill deve ser usada.
---

# Conteúdo da skill com instruções detalhadas
```

Referências adicionais podem ser incluídas em um subdiretório `references/`.

## Licença

MIT
