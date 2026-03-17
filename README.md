# Skills

Coleção pessoal de skills para agentes de IA (Claude Code, Copilot, OpenCode, Gemini, Cursor, etc.).

Skills seguem o formato [Agent Skills](https://agentskills.io/) e podem ser instaladas via [`npx skill`](https://github.com/vercel-labs/skill).

## Instalação

```bash
# Instalar todas as skills
npx skill add git@github.com:tarcisiojr/skills.git

# Listar skills disponíveis
npx skill add git@github.com:tarcisiojr/skills.git --list

# Instalar skill específica
npx skill add git@github.com:tarcisiojr/skills.git --skill dev-python

# Instalar globalmente (disponível em todos os projetos)
npx skill add git@github.com:tarcisiojr/skills.git --skill dev-python -g

# Instalar para agentes específicos
npx skill add git@github.com:tarcisiojr/skills.git -a claude-code -a opencode

# Instalação não-interativa
npx skill add git@github.com:tarcisiojr/skills.git --skill dev-python -g -a claude-code -y
```

## Skills Disponíveis

| Skill | Descrição |
|-------|-----------|
| [dev-python](skills/dev-python/) | Desenvolvimento Python com boas práticas, estilo Pythônico e padrões modernos. Baseada em Fluent Python, Effective Python, PEPs oficiais e ferramentas modernas (ruff, mypy, pytest, uv). |

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
│   └── dev-python/
│       ├── SKILL.md              # Definição principal da skill
│       └── references/           # Documentação detalhada
│           ├── modern-python.md  # Type hints, async, features 3.10+
│           ├── pythonic-patterns.md  # Idiomas e padrões Pythônicos
│           └── project-setup.md  # Estrutura de projeto e ferramentas
└── README.md
```

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
