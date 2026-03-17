# Multi-Tenancy SaaS e Compliance (GDPR/LGPD) — Referência Detalhada

Baseado em: AWS SaaS, Azure Multi-Tenant, GDPR, LGPD

## Índice
1. [Multi-Tenancy — Modelos](#multi-tenancy)
2. [Problemas Críticos de Multi-Tenancy](#problemas)
3. [Compliance — Privacy by Design](#privacy-by-design)
4. [LGPD/GDPR — Requisitos Técnicos](#requisitos)
5. [Checklist de Compliance](#checklist)

---

## Multi-Tenancy

### Modelos de Isolamento

#### Silo (Single-Tenant / Dedicado)
- Cada tenant tem instância e banco dedicados
- **Isolamento:** Máximo — sem compartilhamento
- **Custo:** Alto — infraestrutura por tenant
- **Quando:** Compliance rigoroso (saúde, financeiro), dados altamente sensíveis, clientes enterprise que exigem

#### Bridge (Schema-per-Tenant / Híbrido)
- Banco compartilhado, schema dedicado por tenant
- **Isolamento:** Alto — separação lógica forte
- **Custo:** Médio
- **Quando:** Equilíbrio entre isolamento e custo, regulamentação moderada

#### Pool (Shared-Everything / Compartilhado)
- Mesmas tabelas com coluna `tenant_id`
- **Isolamento:** Médio — depende de row-level security
- **Custo:** Baixo — máxima eficiência de recursos
- **Quando:** Muitos tenants, custo é prioridade, dados não ultrasensiveis

### Tabela Comparativa

| Aspecto | Silo | Bridge | Pool |
|---------|------|--------|------|
| Isolamento de dados | Físico | Lógico (schema) | Lógico (row) |
| Customização por tenant | Total | Moderada | Limitada |
| Custo por tenant | Alto | Médio | Baixo |
| Onboarding de tenant | Lento (nova infra) | Médio (novo schema) | Rápido (novo registro) |
| Escala (nº de tenants) | Dezenas | Centenas | Milhares+ |
| Migrations | Por tenant | Por tenant | Uma para todos |
| Backup/Restore | Independente | Por schema | Complexo (filtrar) |

---

## Problemas Críticos

### Noisy Neighbor
Um tenant monopoliza recursos compartilhados, degradando performance de outros.

**Soluções:**
- Rate limiting por tenant
- Resource quotas (CPU, memória, IOPS) por tenant
- Fair scheduling — priorização baseada em tier
- Monitoramento de consumo por tenant
- Auto-scaling reativo a picos individuais

### Data Sovereignty
Dados de tenants devem residir em jurisdições específicas.

**Soluções:**
- Multi-region deployment com roteamento por tenant
- Metadata indica jurisdição de cada tenant
- Replicação apenas dentro da jurisdição permitida
- Audit de localização de dados

### Tenant Isolation Leaks
Bug que expõe dados de um tenant a outro — o pior cenário.

**Soluções:**
- Row-Level Security (RLS) no banco de dados
- Middleware que injeta tenant_id em toda query
- Testes automatizados de isolamento (cross-tenant access)
- Code review com checklist de multi-tenancy
- Nunca confie apenas em lógica de aplicação — DB-level enforcement

### Tenant-Aware Operations
- **Logging:** Toda log entry inclui tenant_id
- **Metrics:** Dashboards por tenant para SLA tracking
- **Billing:** Metering de uso por tenant para cobrança
- **Support:** Contexto de tenant disponível para equipe de suporte

---

## Privacy by Design (GDPR / LGPD)

### 7 Princípios Fundamentais (Ann Cavoukian)

1. **Proativo, não reativo** — Prevenir violações antes que ocorram
2. **Privacidade como padrão** — Sem ação do usuário, config mais privada
3. **Privacidade incorporada ao design** — Parte da arquitetura, não add-on
4. **Funcionalidade total** — Privacidade E funcionalidade, não trade-off
5. **Segurança end-to-end** — Proteção do dado em todo ciclo de vida
6. **Visibilidade e transparência** — Operações verificáveis e auditáveis
7. **Respeito à privacidade do usuário** — Usuário no centro de decisões

---

## Requisitos Técnicos LGPD/GDPR

### Direitos do Titular

| Direito | Impacto Técnico |
|---------|----------------|
| **Acesso** | API para exportar todos os dados do usuário em formato legível |
| **Retificação** | Capacidade de corrigir dados em todos os sistemas |
| **Exclusão (Right to be Forgotten)** | Deletar dados de TODOS os sistemas (inclusive backups, logs, caches) |
| **Portabilidade** | Exportar em formato estruturado e interoperável (JSON, CSV) |
| **Oposição** | Mecanismo para opt-out de processamentos específicos |
| **Revogação de consentimento** | Parar processamento imediatamente ao revogar |

### Data Minimization
- Colete apenas dados estritamente necessários para o propósito declarado
- Revise periodicamente — dados que não são mais necessários devem ser deletados
- Anonimização/pseudonimização onde possível
- Pergunte: "preciso REALMENTE deste campo?"

### Consent Management
- Consentimento granular (não "aceito tudo")
- Registro de quando, como e para que foi dado consentimento
- Fácil de revogar (tão fácil quanto dar)
- Consentimento não pode ser pré-selecionado
- Renovação periódica para processamentos de longo prazo

### Audit Trail
- Log de toda operação sobre dados pessoais
- Quem acessou, quando, qual dado, para qual finalidade
- Imutável — não pode ser alterado ou deletado
- Retenção conforme regulamentação (LGPD: enquanto necessário para compliance)

### Data Protection Impact Assessment (DPIA)
- Obrigatório antes de processar dados sensíveis em larga escala
- Identifica riscos e medidas de mitigação
- Documentar e manter atualizado
- Consultar DPO (Data Protection Officer) quando aplicável

### Breach Notification
- LGPD: comunicar ANPD em prazo razoável (sem prazo fixo, mas rápido)
- GDPR: 72 horas para notificar autoridade supervisora
- Plano de resposta a incidentes documentado e testado
- Capacidade técnica de identificar escopo do breach rapidamente

---

## Checklist de Compliance

### Design Phase
- [ ] Dados pessoais mapeados (quais, onde, por quê)
- [ ] Base legal para cada processamento definida
- [ ] Data minimization aplicada
- [ ] DPIA realizado para processamentos de risco
- [ ] Consent management projetado

### Implementação
- [ ] Criptografia em trânsito e repouso
- [ ] API de direitos do titular (acesso, exclusão, portabilidade)
- [ ] Audit trail implementado
- [ ] Anonymization/pseudonymization onde aplicável
- [ ] Data retention policy implementada com auto-delete

### Operação
- [ ] DPO designado (se aplicável)
- [ ] Plano de resposta a breach documentado e testado
- [ ] Treinamento de equipe sobre proteção de dados
- [ ] Revisão periódica de dados coletados vs necessários
- [ ] Contratos com processadores (DPA) assinados
- [ ] Monitoramento de acesso a dados pessoais
