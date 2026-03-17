# Segurança by Design + Zero Trust — Referência Detalhada

Baseado em: OWASP, NIST SP 800-207

## Índice
1. [Security by Design (OWASP)](#security-by-design)
2. [Zero Trust Architecture (NIST)](#zero-trust)
3. [Checklist de Segurança](#checklist)

---

## Security by Design

Segurança integrada desde a fase de design, não adicionada depois.

### Princípios OWASP

| Princípio | O que Significa na Prática |
|-----------|---------------------------|
| **Least Privilege** | Cada componente, usuário e processo recebe apenas o acesso mínimo necessário. Tokens com escopo limitado, roles granulares, acesso temporário (JIT). |
| **Defense in Depth** | Múltiplas camadas de proteção: WAF → API Gateway → Auth → Validação → Criptografia → Audit. Se uma camada falha, as outras protegem. |
| **Fail Securely** | Quando ocorre erro, o sistema vai para estado seguro (acesso negado), não estado aberto. Exemplo: se auth service cai, rejeite todas as requests. |
| **Separation of Duties** | Nenhuma pessoa ou sistema completa operação crítica sozinha. Exemplo: quem aprova deploy não é quem faz merge. |
| **Complete Mediation** | Toda requisição de acesso é verificada. Sem atalhos, sem cache de autorização que pula verificação. |
| **Open Design** | Segurança não depende de obscuridade. O sistema é seguro mesmo que o código-fonte seja público. |
| **Economy of Mechanism** | Mecanismos de segurança simples e pequenos — mais fácil de auditar e menos propenso a bugs. |
| **Input Validation** | Valide TODA entrada no servidor. Whitelist > blacklist. Nunca confie em dados do cliente. |
| **Security by Default** | Configuração padrão é a mais segura. Usuário precisa ativamente relaxar segurança, não ativá-la. |

### Padrões de Implementação

**Autenticação:**
- OAuth 2.0 + OIDC para identidade
- JWT com expiração curta (15min access, 7d refresh)
- MFA obrigatório para operações sensíveis
- Nunca armazene senhas — use bcrypt/argon2 com salt

**Autorização:**
- RBAC (Role-Based) para permissões simples
- ABAC (Attribute-Based) para regras complexas
- Verifique em cada request, não apenas no login

**Dados:**
- Criptografia em trânsito (TLS 1.3) e em repouso (AES-256)
- Nunca logue dados sensíveis (PII, tokens, senhas)
- Mascaramento de dados em ambientes não-produção
- Rotação periódica de secrets e chaves

**APIs:**
- Rate limiting por tenant/IP/API key
- CORS configurado restritivamente
- Headers de segurança (CSP, HSTS, X-Frame-Options)
- Validação de schema (OpenAPI) em toda request

---

## Zero Trust

"Nunca confie, sempre verifique" — NIST SP 800-207.

### Princípios Fundamentais

| Princípio | Mudança de Paradigma |
|-----------|---------------------|
| **Never Trust, Always Verify** | Estar dentro da rede corporativa não concede confiança. Cada request é verificada. |
| **Assume Breach** | Opere como se o ambiente já estivesse comprometido. Minimize raio de explosão. |
| **Verify Explicitly** | Auth baseado em TODOS os dados: identidade, device, localização, horário, comportamento. |
| **Least Privilege Access** | Just-In-Time + Just-Enough-Access. Acesso temporário, nunca permanente. |
| **Micro-Segmentation** | Rede dividida em zonas pequenas. Comprometer uma zona não dá acesso a outras. |

### Os 7 Pilares (NIST)

1. **Identity** — Verificação forte de identidade (MFA, biometria)
2. **Device** — Device compliance (patch level, antivirus, encryption)
3. **Network** — Segmentação, criptografia de tráfego
4. **Application** — Auth contínua em nível de aplicação
5. **Data** — Classificação, criptografia, DLP
6. **Analytics** — Monitoramento contínuo, detecção de anomalias
7. **Automation** — Resposta automatizada a incidentes

---

## Checklist de Segurança Arquitetural

### Antes do Design
- [ ] Threat modeling realizado (STRIDE, DREAD)
- [ ] Requisitos de compliance identificados (LGPD, PCI-DSS, SOC2)
- [ ] Classificação de dados definida (público, interno, confidencial, restrito)

### Durante o Design
- [ ] Autenticação e autorização em todas as fronteiras
- [ ] Input validation em todo ponto de entrada
- [ ] Criptografia em trânsito e em repouso
- [ ] Secrets management (Vault, AWS Secrets Manager)
- [ ] Rate limiting e throttling
- [ ] Audit trail para operações sensíveis

### Antes de Produção
- [ ] SAST/DAST executados (análise estática e dinâmica)
- [ ] Dependências verificadas (CVE scan)
- [ ] Headers de segurança configurados
- [ ] Penetration test em funcionalidades críticas
- [ ] Plano de resposta a incidentes documentado

### Em Produção
- [ ] Monitoramento de segurança ativo
- [ ] Alertas para tentativas de acesso não autorizado
- [ ] Rotação de secrets automatizada
- [ ] Backup criptografado e testado
