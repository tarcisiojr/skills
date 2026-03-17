---
name: rest-api-design
description: Design de APIs REST seguindo convenções padronizadas. Use quando o usuário pedir para criar, desenhar ou refatorar endpoints REST. Define padrões de nomenclatura, status codes, envelopes de erro, paginação e versionamento. O framework (FastAPI) gera o OpenAPI automaticamente a partir do código.
license: MIT
metadata:
  author: tarcisiojunior
  version: "2.0"
---

Design de APIs REST orientado a **convenções**. O OpenAPI é gerado automaticamente pelo FastAPI a partir dos schemas Pydantic e decorators de rota — não criamos YAML manualmente.

**Arquivos de referência** — leia sob demanda conforme a fase exigir:
- `conventions.md` — URIs, métodos HTTP, status codes, erros, versionamento, IDs
- `patterns.md` — paginação, filtros, busca, ordenação, expansão, fieldsets, extensibilidade
- `spec-template.md` — referência de schemas Pydantic e padrões FastAPI para garantir que o OpenAPI gerado seja correto

Todos estão no mesmo diretório deste skill.

---

## Fluxo de Trabalho

### Fase 1 — Elicitação de Contexto (nunca pule)

Antes de qualquer implementação, colete com **AskUserQuestion**:

1. **Domínio e recursos** — entidades centrais (ex: pacientes, consultas, exames)
2. **Público** — serviço interno, parceiros ou público?
3. **Autenticação** — nenhuma, API Key, OAuth 2.0/JWT?
4. **Nova ou existente?** — se existente, versão atual e breaking changes aceitáveis?
5. **Escala** — baixo tráfego interno vs. alto volume público?

**Não assuma. Não prossiga sem esse contexto.**

### Fase 2 — Design de Recursos

Leia `conventions.md` e aplique as regras de nomenclatura de URIs.
Mapeie os recursos, seus relacionamentos e sub-recursos.
Sinalize anti-patterns se o usuário propuser algum.

### Fase 3 — Decisões de Design

Apresente ao usuário para aprovação:
- Lista de recursos e relacionamentos
- Formato de ID (ULID padrão — consultar `conventions.md`)
- Estratégia de paginação (offset vs cursor — consultar `patterns.md`)
- Esquema de autenticação
- Justificativa para decisões não óbvias

Peça confirmação antes de prosseguir à implementação.

### Fase 4 — Implementação

Implemente diretamente no FastAPI seguindo a arquitetura em camadas:
1. **Schemas Pydantic** (`app/schemas/`) — Create, Update, Response por recurso
2. **Rotas FastAPI** (`app/api/v1/`) — endpoints com type hints, status codes, tags
3. **Services** (`app/services/`) — lógica de negócio
4. **Repositories** (`app/repositories/`) — acesso a dados

Consulte `conventions.md` para status codes e envelope de erro.
Consulte `patterns.md` para paginação, filtros e expansão.
Consulte `spec-template.md` para padrões de schemas Pydantic.

O FastAPI gera automaticamente:
- OpenAPI 3.1 em `/docs` (Swagger UI) e `/redoc` (ReDoc)
- Schemas JSON a partir dos modelos Pydantic
- Validação de request/response

### Fase 5 — Verificação

Após implementar, verifique:
1. **Convenções** — URIs, status codes, envelopes seguem os padrões
2. **OpenAPI gerado** — acesse `/docs` e confirme que a documentação está correta
3. **Testes** — cenários WHEN/THEN cobertos
4. **Tabela de códigos de erro** — todos os `error.code` documentados

### Fase 6 — Próximos Passos

Pergunte ao usuário:
> "Endpoints implementados! Posso: (1) adicionar novos endpoints, (2) refatorar endpoints existentes, (3) revisar o OpenAPI gerado."

---

## Guardrails

- **Não pule a Fase 1** — sem contexto, não há design
- **Não gere YAML OpenAPI manualmente** — o FastAPI gera a partir do código
- **Não aceite anti-patterns** — sinalize e proponha correção (tabela completa em `conventions.md`)
- **Não invente requisitos** — pergunte se algo não está claro
- **Reutilize schemas** — schemas base compartilhados, nunca duplique inline
- **Documente todos os status codes** por endpoint via `responses={}` no decorator
- **Use type hints** em todos os parâmetros e retornos para garantir OpenAPI correto
