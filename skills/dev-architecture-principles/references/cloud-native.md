# Cloud Native, Well-Architected e Infrastructure as Code — Referência

Baseado em: AWS, Azure, Google Cloud, Heroku (12-Factor), HashiCorp, CNCF

## Índice
1. [Well-Architected Framework (Consolidado)](#well-architected)
2. [12-Factor App](#12-factor)
3. [Infrastructure as Code](#iac)
4. [GitOps](#gitops)

---

## Well-Architected Framework

Consolidação dos pilares AWS (6), Azure (5) e Google Cloud (6):

### Pilar 1: Segurança
- Identidade e acesso com least privilege
- Criptografia em trânsito (TLS) e repouso (AES-256)
- Detecção de ameaças e resposta automatizada
- Proteção de dados com classificação e DLP
- Compliance e governança como código

### Pilar 2: Confiabilidade (Reliability)
- Design for failure — assuma que componentes vão falhar
- Redundância em múltiplas AZs/regiões
- Recovery automatizado (auto-healing)
- Testes de resiliência (chaos engineering)
- Backups automatizados e testados

### Pilar 3: Performance
- Right-sizing de recursos baseado em métricas reais
- Cache em múltiplas camadas (CDN, application, database)
- Processamento assíncrono para operações pesadas
- Database optimization (índices, query tuning, read replicas)
- Monitoramento contínuo de latência e throughput

### Pilar 4: Operação (Operational Excellence)
- IaC para toda infraestrutura
- CI/CD automatizado com rollback
- Observabilidade (logs, métricas, traces)
- Runbooks e automação de incidentes
- Post-mortems sem blame

### Pilar 5: Custo (Cost Optimization)
- Right-sizing baseado em uso real
- Reserved/Spot instances para workloads previsíveis
- Auto-scaling com min/max definidos
- Tagging para alocação de custos por equipe/projeto
- Revisão mensal de custos (FinOps)

### Pilar 6: Sustentabilidade
- Maximizar utilização de recursos (evitar ociosidade)
- Regiões com energia limpa quando possível
- Otimizar eficiência de código para reduzir compute
- Data lifecycle management (archive dados antigos)

---

## 12-Factor App

### I. Codebase
- Um repositório por aplicação
- Múltiplos deploys (dev, staging, prod) do mesmo código
- Config diferencia ambientes, não branches

### II. Dependencies
- Declaradas explicitamente (package.json, requirements.txt, go.mod)
- Nunca dependa de pacotes instalados no sistema
- Lock file para reproducibilidade (package-lock.json, poetry.lock)

### III. Config
- Tudo que varia entre ambientes → variáveis de ambiente
- Nunca no código-fonte (nem em arquivo de config commitado)
- Secrets em serviços dedicados (Vault, AWS Secrets Manager)

### IV. Backing Services
- Banco, cache, fila, email = recursos substituíveis
- Trocar MySQL por PostgreSQL = mudança de config, não de código
- Nenhum tratamento especial para serviços locais vs remotos

### V. Build, Release, Run
- **Build:** Compila código + dependências em artefato
- **Release:** Build + config = release imutável (com ID único)
- **Run:** Executa release no ambiente
- Releases nunca são mutáveis — nova mudança = nova release

### VI. Processes
- Stateless e share-nothing
- Sem estado em memória entre requests
- Sessões em backing service (Redis), não em memória do processo
- Filesystem do processo é efêmero

### VII. Port Binding
- App exporta HTTP como serviço via port binding
- Não depende de servidor web externo (Apache, Nginx como runtime)
- Um app pode ser backing service de outro

### VIII. Concurrency
- Escale adicionando processos, não threads
- Processos por tipo: web (HTTP), worker (background jobs), scheduler
- Process manager (systemd, Kubernetes) gerencia lifecycle

### IX. Disposability
- Startup em segundos (não minutos)
- Shutdown graceful: pare de aceitar requests, termine em-progresso, saia
- Tolerante a crash: processo pode morrer a qualquer momento
- Workers devem retornar jobs para a fila no shutdown

### X. Dev/Prod Parity
- Minimize gap de tempo: deploy horas após code, não semanas
- Minimize gap de pessoal: dev que escreveu faz deploy
- Minimize gap de ferramentas: mesmo banco em dev e prod (não SQLite vs PostgreSQL)

### XI. Logs
- App escreve para stdout, nunca gerencia arquivos de log
- Ambiente de execução coleta, roteia e armazena (Fluentd, CloudWatch)
- Logs estruturados (JSON) para análise automatizada

### XII. Admin Processes
- Migrations, scripts de manutenção = mesmo código, mesmo ambiente
- Executar como one-off processes, não manualmente no servidor
- Incluir no mesmo repositório que a aplicação

---

## Infrastructure as Code

### Princípios Fundamentais

| Princípio | O que Significa |
|-----------|----------------|
| **Declarativo** | Defina o estado desejado, ferramenta converge. Não scripts imperativos. |
| **Versionado** | Todo IaC em Git. Mudança = commit com review. |
| **Idempotente** | Aplicar N vezes = mesmo resultado. Seguro re-executar. |
| **Imutável** | Substitua servidores, não modifique. Nova versão = nova instância. |
| **Modular** | Módulos reutilizáveis por projeto/equipe. |
| **Testável** | Validate/plan antes de apply. Testes de infra (Terratest, Checkov). |

### Secret Management
- Nunca em plaintext no código ou variáveis de ambiente
- Ferramentas: HashiCorp Vault, AWS Secrets Manager, Azure Key Vault
- Rotação automática de secrets
- Acesso auditado (quem acessou qual secret quando)

### Policy as Code
- Regras de segurança/compliance como código (OPA, Sentinel, Checkov)
- Validação automática antes de apply
- Bloqueia deploy que viola política

### Drift Detection
- Detecta quando infra real diverge do declarado
- Alerta quando drift é detectado
- Reconciliação automática ou manual conforme criticidade

---

## GitOps

### Princípios
1. **Git como single source of truth** — Estado desejado está no Git
2. **Mudanças via PR** — Nenhuma mudança manual. Tudo revisado e auditável
3. **Reconciliação contínua** — Controller compara desejado (Git) vs atual (cluster)
4. **Observabilidade** — Status de convergência é visível

### Fluxo
```
Developer → PR → Review → Merge → GitOps Controller → Apply → Cluster
                                         ↑
                              Reconciliation Loop
                              (compara Git vs cluster)
```

### Ferramentas
- **ArgoCD** — GitOps para Kubernetes (declarativo, UI)
- **Flux** — GitOps toolkit (CNCF, mais leve)
- **Terraform Cloud** — GitOps para infraestrutura
