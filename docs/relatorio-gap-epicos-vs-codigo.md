# Relatório de GAP - Épicos vs Código

> **Projeto Tutor** — Análise de conformidade funcional e técnica
> **Escopo primário:** `docs/epicos/` (EP-01, EP-02, EP-03, EP-06, EP-09)
> **Referências complementares:** `docs/rbac.md`, `docs/sitemap.md`, `docs/visao.md`
> **Data da análise:** 2026-05-30
> **Método:** análise por épico + verificação adversarial (releitura do código citado) + varredura transversal.

---

## Sumário Executivo

### Aderência geral estimada

| Épico | Aderência estimada |
|-------|:------------------:|
| EP-01 — Autenticação e Controle de Acesso | **~72%** |
| EP-02 — Gestão de Usuários | **~55%** |
| EP-03 — Gestão de Matérias e Turmas (v1.4) | **~52%** |
| EP-06 — Chat Educacional | **~45%** |
| EP-09 — Gestão do Modelo de IA | **~28%** |
| **Aderência média ponderada** | **~50%** |

### Épicos mais completos
- **EP-01 (Autenticação)** — login matrícula/senha, login Google, convite/primeiro acesso, hashing e expiração de token estão majoritariamente implementados e coerentes; falhas concentradas em sessão por inatividade e textos de mensagem.
- **EP-02 (Gestão de Usuários)** — o fluxo de cadastro/edição/desativação está presente no frontend e parcialmente no backend, mas comprometido por falhas graves de autorização no backend.

### Épicos mais incompletos
- **EP-09 (Gestão do Modelo de IA)** — funcionalidade central (scraping da biblioteca Ollama, consulta de instalados, pull/download, UI do catálogo) **ausente**; tela vazia; **a migration da coluna `status` na tabela `llm` não existe**, o que quebra todo o fluxo em ambiente migrado.
- **EP-06 (Chat Educacional)** — UI presente, mas o **núcleo de RAG está quebrado em runtime** (bug em `busca_semantica.py:57`), a **detecção de baixa confiança é ausente** (a IA pode alucinar), e faltam limite de 1.000 caracteres e janela de 10 trocas.

### Principais riscos funcionais
1. **EP-09:** migration ausente da coluna `status` em `llm` → `ativar_modelo`/`getActiveModel` e o chat falham em produção (deploy roda apenas `flask db upgrade`). *(EP-09 GAP-01)*
2. **EP-06:** `busca_semantica.py:57` usa `asyncio.to_thread(buscar_no_vector_db(...))` — chama a função e passa o **resultado** como callable → `TypeError` em runtime sempre que há material indexado; o RAG nunca recupera contexto. *(EP-06 GAP-02)*
3. **EP-06:** sem gate de baixa confiança (bloco de contexto vazio comentado; `MCPPipeline.valid_stream` nunca usado) → IA responde sem embasamento. *(EP-06 GAP-01)*
4. **EP-03:** modelo de associação v1.4 (entidades `MateriaProfessor` US-12 e `MateriaProfessorTurma` US-13) **inexistente**; sem tela de detalhe de turma; sem oferta, sem desmatrícula. *(EP-03 G1/G2/G4)*
5. **EP-09:** catálogo dinâmico, pull e UI ausentes; tela `catalogoLLM` vazia. *(EP-09 GAP-02/03/04)*

### Principais riscos de autorização/segurança (ligados aos épicos)
1. **CRÍTICO — EP-02:** rotas de gestão de usuários (`/usuarios/criar`, `/all`, `/<id>`, `/delete/<id>`, `/reativar`) **sem `@token_obrigatorio`/`@apenas_admins`** → API pública: qualquer um lista, cria, edita, desativa e reativa usuários. *(EP-02 GAP-01)*
2. **CRÍTICO — EP-03:** `POST /alunos_turmas` com `@apenas_alunos` **comentado** → qualquer usuário autenticado matricula alunos. *(EP-03 G3)*
3. **CRÍTICO/ALTO — EP-01 + EP-03:** `apenas_professores`/`apenas_alunos` comparam `g.usuario_role` contra `'1'/'2'/'3'`, mas o JWT grava o **nome** (`'PROFESSOR'/'ALUNO'`) → decorators **sempre negam (403)**; RBAC de professor/aluno quebrado (rotas de arquivos e de associação/oferta inacessíveis). *(EP-01 GAP-02 / EP-03 G7)*
4. **CRÍTICO — EP-02:** ao desativar um usuário, a sessão (JWT) ativa **não é encerrada** → acesso mantido por ~60 min. *(EP-02 GAP-02)*
5. **CRÍTICO — EP-02:** admin pode **desativar a própria conta** (sem verificação; endpoint sequer identifica o solicitante). *(EP-02 GAP-03)*
6. **ALTO — EP-06:** o socket de chat valida apenas o formato UUID de `materia_id`, **não a matrícula** → aluno pode consultar matéria não matriculada. *(EP-06 GAP-06)*
7. **ALTO — EP-09:** `route_llm` sem proteção de auth (endpoint público). *(EP-09 GAP-06)*

> **Padrão recorrente:** a maioria das regras de autorização e validação está protegida **apenas no frontend** (middleware/forms), com o backend exposto ou inconsistente. Isso afeta EP-01, EP-02, EP-03, EP-06 e EP-09.

---

## Matriz de Conformidade por Épico

Legenda de status: **Implementado** · **Parcial** · **Ausente** · **Divergente** · **Não verificável**

### EP-01 — Autenticação e Controle de Acesso (US-01, US-02, US-03, US-05)

| ID / US | Requisito (épico) | Status | Evid. épico | Evid. código | Observação |
|---|---|---|---|---|---|
| US-01-RN1 | Login por matrícula (identificador) + senha obrigatória | Implementado | EP01:31-32 | `route_usuarios.py:179-183`; `service_usuario.py:80-85`; `login/page.tsx:111` | Backend exige ambos (400); botão desabilitado com campos vazios. |
| US-01-RN2 | Apenas usuários ativos logam; desativados bloqueados | Implementado | EP01:33-34 | `route_usuarios.py:189-190` (403) | `service_aluno.ts:112` mapeia 403→deactivated. |
| US-01-RN3 | Redirecionar por perfil (admin/professor/aluno) | Implementado | EP01:35-38 | `utils/roles.ts:16-20`; `login/page.tsx:52-57`; `middleware.ts:47-49` | JWT grava `role.name`; redirect casa. Mismatch de role afeta autorização (GAP-02), não o redirect. |
| US-01-RN4 | Mensagem genérica de credenciais (não revela campo) | Implementado | EP01:44 | `route_usuarios.py:185-187`; `login/page.tsx:46` | `logar_aluno` retorna None p/ matrícula inexistente e senha errada. |
| US-01-RV1 | Campo de senha oculto com opção de visualizar | Implementado | EP01:45 | `components/Input/Input.tsx:61-72` | Toggle Eye/EyeOff automático p/ `type='password'`. |
| US-01-RI1 | Login 1ª tela; botão desabilitado; "Esqueci minha senha"; Google; erro abaixo do form | Parcial | EP01:49-54 | `middleware.ts:39-43`; `login/page.tsx:111,154-156,174-189,219-225` | Label "Matrícula" (não "Matrícula institucional"); erro via Toast, não "abaixo do formulário". |
| US-01-RNF1 | Senhas com hashing | Implementado | EP01:60 | `service_usuario.py:4,22,168,83` | `generate_password_hash`/`check_password_hash` (werkzeug). |
| US-01-RNF2 | Comunicação protegida (HTTPS) | Não verificável | EP01:59 | `route_usuarios.py:139,202` (`secure=False`); `route_admin.py:359` | Cookie JWT `secure=False`; depende de TLS no ambiente. |
| US-01-RNF3 | Sessão expira por inatividade configurável | Parcial | EP01:61 | `jwt_handler.py:5,19`; `route_usuarios.py:141,204` | Expiração **absoluta** de 60 min hardcoded, não por inatividade nem configurável. |
| US-02-RN1 | Google só p/ usuário ativo; e-mail deve corresponder; não cria usuário | Implementado | EP01:85-87 | `route_usuarios.py:119-127`; `test_login_google.py:106-122` | 404 se inexistente, 403 se inativo; não cria. |
| US-02-RV1 | Mensagem específica "conta Google não vinculada... contate o admin" | Divergente | EP01:92 | `route_usuarios.py:121-124`; `service_aluno.ts:127-130` | Backend retorna 404 c/ texto diferente; front mapeia só 401/403, 404 vira "unknown". |
| US-02-RV2 | Usuário desativado bloqueado também no Google | Implementado | EP01:93 | `route_usuarios.py:126-127`; `service_aluno.ts:128` | 403→deactivated. |
| US-02-RI1 | Botão Google separado; mensagem de falha específica | Divergente | EP01:97-99 | `login/page.tsx:168-189,102-105,48` | Botão presente/separado, mas textos de falha não correspondem ao épico. |
| US-02-PRE1 | Plataforma configurada p/ Google (config técnica) | Implementado | EP01:109 | `route_usuarios.py:100-105`; `login/page.tsx:33,199-216` | `verify_oauth2_token` com `GOOGLE_CLIENT_ID`. |
| US-03-RN1 | Gera link de convite único e envia por e-mail | Implementado | EP01:128 | `service_usuario.py:36-43`; `route_admin.py:130-136`; `email_sender.py:29` | Token UUID + e-mail com "Criar minha senha". |
| US-03-RN2 | Link de uso único; expira só após uso; sem prazo | Implementado | EP01:129-130 | `model_token_convite.py:15`; `service_usuario.py:163-169,145-153` | Só flag `used`, sem expiração temporal. |
| US-03-RN3 | Após criar senha, link invalidado e redireciona à home do perfil | Divergente | EP01:131-132 | `alterar-senha/page.tsx:76,90`; `route_auth.py:110-118` | Fluxo usado (`/auth/invite/set-password`) **não inicia sessão**; redireciona a `/login`. |
| US-03-RN4 | Fluxo só p/ login matrícula+senha (Google não cria senha) | Implementado | EP01:134 | `service_usuario.py:36`; `route_admin.py:132` | Flag `via_google` controla. |
| US-03-RV1 | Senha forte (8+, maiúscula/minúscula/número); confirmação dupla | Parcial | EP01:138-141 | `service_usuario.py:176-186`; `alterar-senha/page.tsx:21-29`; `route_auth.py:96-98` | Endpoint usado não recebe/valida `passwordConfirmation` no backend; mensagem literal ausente. |
| US-03-RV2 | Link já usado → orientar "Esqueci minha senha" | Implementado | EP01:142 | `route_auth.py:47-51,104-108`; `token-validate/page.tsx:38-42` | 410 Gone com orientação. |
| US-03-RI1 | E-mail de convite + tela de boas-vindas + 2 campos com visualizar | Parcial | EP01:146-149 | `email_sender.py:85,109`; `alterar-senha/page.tsx:108-159` | Campos e toggle OK; texto da tela diverge do literal do épico. |
| US-03-RNF1 | Senha protegida (hash); e-mail em até 2 min | Parcial | EP01:153-154 | `service_usuario.py:168`; `route_admin.py:133-136` | Hash OK; envio síncrono sem fila/retry — falha de SMTP só logada. |
| US-03-AC7 | "Esqueci minha senha" funciona como alternativa | Implementado | EP01:169 | `route_auth.py:121-145`; `esqueci-senha/page.tsx:18-25` | Invalida tokens antigos, gera novo, resposta genérica. |
| US-05-RN1 | Logout voluntário; redireciona ao login | Parcial | EP01:181,183 | `route_usuarios.py:238-252`; `AuthContext.tsx:40-43` | Invalidação em memória (frágil); redirect depende do middleware. |
| US-05-RN2 | Expiração automática por inatividade configurável (admin) | Ausente | EP01:182 | `jwt_handler.py:5,19`; `model_sessao.py:5-13` | Exp absoluto hardcoded; `Sessao` não usado no fluxo de auth. |
| US-05-RV1 | Sessão expirada → login c/ "Sua sessão expirou..." | Implementado | EP01:188 | `api.ts:34-38`; `login/page.tsx:35-39,227-233` | Texto exato exibido via `returnTo`. |
| US-05-RI1 | "Sair" sempre visível; logout imediato; "voltar" não retorna | Parcial | EP01:192-194 | `middleware.ts:39-43`; `AuthContext.tsx:40-43` | Logout imediato OK; visibilidade do "Sair" não verificada. |

### EP-02 — Gestão de Usuários (US-07, US-08, US-09)

| ID / US | Requisito (épico) | Status | Evid. épico | Evid. código | Observação |
|---|---|---|---|---|---|
| US-07-RN1 | Apenas admin cadastra professores | Parcial | EP02:33,58 | `route_admin.py:87-88` (sem decorators); `middleware.ts:47` | Backend público; restrição só no frontend. |
| US-07-RN2 | Professor recebe perfil "Professor" no cadastro | Divergente | EP02:34 | `service_usuario.py:29` (role=ALUNO fixo); `service_professor.ts:28-47` | Backend grava ALUNO; frontend faz POST+PUT (não atômico). |
| US-07-RN3 | Link de convite por e-mail | Implementado | EP02:35,65 | `route_admin.py:130-136`; `email_sender.py:18-29` | Convite gerado/enviado. |
| US-07-RN4 | Matrícula e e-mail únicos | Implementado | EP02:37,42-43 | `model_usuario.py:16,18`; `route_admin.py:123-128` | Unique + checagem 409 na criação. |
| US-07-RV1 | Nome/matrícula/e-mail obrigatórios; e-mail institucional | Implementado | EP02:41-43 | `route_admin.py:117-121`; `FormularioProfessor.tsx:24-26` | Exige `@iesb.edu.br`. |
| US-07-RV2 | Mensagens específicas de matrícula/e-mail duplicado | Divergente | EP02:44-45 | `route_admin.py:128`; `FormularioProfessor.tsx:60-74` | Backend retorna genérico; frontend marca ambos os campos. |
| US-07-RI1 | Formulário com Nome/Matrícula/E-mail | Implementado | EP02:49 | `FormularioProfessor.tsx:135-174` | Três campos presentes. |
| US-07-RI2 | Confirmação + opção cadastrar outro/voltar | Parcial | EP02:50 | `FormularioProfessor.tsx:117-120` | Toast + redirect; sem "cadastrar outro". |
| US-07-AC4 | Professor cria senha e acessa | Implementado | EP02:65 | `route_admin.py:284-365`; `service_usuario.py:156-186` | Coberto por `test_primeiro_acesso.py`. |
| US-08-RN1 | Apenas admin cadastra alunos | Parcial | EP02:77,105 | `route_admin.py:87-88`; `middleware.ts:47` | Mesmo endpoint sem auth backend. |
| US-08-RN2 | Aluno recebe perfil "Aluno" | Implementado | EP02:78 | `service_usuario.py:29-30` | role=ALUNO, status=ATIVO. |
| US-08-RN3 | Link de convite por e-mail | Divergente | EP02:79,93,112 | `route_admin.py:130-136`; `service_aluno.ts:24-46`; `FormularioAluno.tsx:24-32` | Convite funciona; frontend gera "senha temporária" inútil (backend ignora). |
| US-08-RN4 | Matrícula e e-mail únicos | Implementado | EP02:80,85-86 | `model_usuario.py:16,18`; `route_admin.py:123-128` | Igual US-07-RN4. |
| US-08-RV1 | E-mail com formato válido (institucional) | Divergente | EP02:86,43 | `FormularioAluno.tsx:34-36`; `route_admin.py:120` | Form de aluno não exige `@iesb.edu.br`; backend exige → inconsistência. |
| US-08-RV2 | Mensagens específicas de duplicidade | Divergente | EP02:87-88 | `route_admin.py:128`; `FormularioAluno.tsx:113-127` | Genérico; fallback marca ambos. |
| US-08-RI1 | Formulário com Nome/Matrícula/E-mail | Implementado | EP02:92 | `FormularioAluno.tsx:137-176` | Presentes. |
| US-08-RI2 | Confirmação + opção cadastrar outro/voltar | Parcial | EP02:94 | `FormularioAluno.tsx:107-110` | Toast + redirect; sem "cadastrar outro". |
| US-08-RI3 | Listagem com busca (acima) e paginação (abaixo) | Parcial | EP02:95,113 | `alunos/page.tsx:211-217,228-234,89-92` | UI correta, mas opera só no cliente. |
| US-08-RNF1 | Paginação **server-side** | Divergente | EP02:100,113 | `service_aluno.ts:9-18`; `alunos/page.tsx:89-92`; `route_admin.py:46-69` | Backend suporta, frontend não usa; traz todos e fatia no cliente. |
| US-08-RNF2 | Busca server-side por nome/matrícula/**e-mail** | Divergente | EP02:101,114 | `alunos/page.tsx:76-85`; `service_usuario.py:126-142` | Frontend filtra em memória; backend não filtra por e-mail. |
| US-08-AC3 | Aluno listado com status ativo | Implementado | EP02:111 | `service_usuario.py:30`; `alunos/page.tsx:145-157` | Badge de status. |
| US-09-RN1 | Editar nome e e-mail de qualquer usuário | Parcial | EP02:126,157,152 | `route_admin.py:198-241`; `service_usuario.py:99-112` | Funciona, mas sem auth backend e sobrescreve matrícula/role/status. |
| US-09-RN2 | Matrícula imutável após cadastro | Parcial | EP02:127,159 | `FormularioAluno.tsx:153`; `service_usuario.py:105` | Bloqueio só no frontend; backend grava qualquer matrícula. |
| US-09-RN3 | Desativar usuário (impede login) | Implementado | EP02:128,160 | `route_admin.py:141-169`; `service_usuario.py:88-96` | status=INATIVO bloqueia novos logins. |
| US-09-RN4 | Desativação não exclui histórico (soft delete) | Implementado | EP02:129 | `service_usuario.py:88-96` | Só altera status. |
| US-09-RN5 | Reativar usuário | Implementado | EP02:130,161 | `route_admin.py:245-282`; `service_usuario.py:115-123` | Botão Reativar p/ desativados. |
| US-09-RV1 | E-mail editado único c/ mensagem específica | Ausente | EP02:134,158 | `route_admin.py:198-241`; `service_usuario.py:99-112` | Sem checagem; IntegrityError → 500, não 409. |
| US-09-RV2 | Desativar com sessão ativa → encerra a sessão | Ausente | EP02:136,148,160 | `service_usuario.py:88-96`; `auth_decorators.py:31-51` | JWT não invalidado; sem reconsulta de status. |
| US-09-RV3 | Admin não desativa a própria conta | Ausente | EP02:162 | `route_admin.py:141-169`; `service_usuario.py:88-96` | Sem verificação; endpoint nem identifica solicitante. |
| US-09-RI1 | Linha com Editar/Desativar/Reativar | Implementado | EP02:140 | `alunos/page.tsx:158-196`; `professores/page.tsx:170-208` | Presente. |
| US-09-RI2 | Confirmação de desativar com texto específico | Implementado | EP02:141 | `alunos/page.tsx:258-262` | Texto idêntico ao épico. |
| US-09-RI3 | Desativados identificados visualmente | Implementado | EP02:142 | `alunos/page.tsx:145-157` | Badge distinto. |
| US-09-RI4 | Edição pré-preenchida | Implementado | EP02:143 | `editarAluno/page.tsx:7-25`; `FormularioAluno.tsx:38-53` | Dados via query params (frágil/expõe na URL). |
| US-09-AC2 | E-mail duplicado na edição rejeitado | Ausente | EP02:158 | `route_admin.py:198-241` | Ver US-09-RV1 (500 em vez de 409). |

### EP-03 — Gestão de Matérias e Turmas v1.4 (US-10, US-10b, US-11, US-12, US-13, US-14)

| ID / US | Requisito (épico) | Status | Evid. épico | Evid. código | Observação |
|---|---|---|---|---|---|
| US-10-RN1 | Apenas admin cadastra matéria | Implementado | EP03:33 | `route_admin.py:405-407` (`@apenas_admins` OK) | `apenas_admins` compara 'ADMIN' (funciona). |
| US-10-RN2 | Matéria independente; código único + nome | Implementado | EP03:34-35 | `model_materia.py:14-16`; `service_materia.py:78-90` | Código unique/index. |
| US-10-RV1 | Código único c/ mensagem específica | Implementado | EP03:39 | `route_admin.py:420-425` | Mensagem idêntica ao épico. |
| US-10-RV2 | Nome obrigatório | Implementado | EP03:40 | `route_admin.py:416-417`; `FormularioMateria.tsx:42-44` | Mensagem de erro backend textualmente incorreta, mas regra funciona. |
| US-10-RI1 | Form Código/Nome; status "Ativa"; busca | Implementado | EP03:44-46 | `FormularioMateria.tsx:114-139`; `materias/page.tsx:100-108` | Busca client-side. |
| US-10-CA | Critérios de aceite US-10 | Implementado | EP03:58-60 | `route_admin.py:405-430` | Cobertos. |
| US-10b-RN1 | Editar nome; código imutável | Divergente | EP03:72 | `service_materia.py:93-105`; `route_admin.py:436-454` | Bloqueio só no frontend; backend sobrescreve código. |
| US-10b-RN2 | Desativação preserva histórico; reativar | Implementado | EP03:73-74 | `service_materia.py:131-132`; `service_materia.ts:93-101` | Soft delete via status. |
| US-10b-RN3 | Bloquear desativação com vínculos (US-12)/ofertas (US-13) | Divergente | EP03:75,102 | `service_materia.py:115-129` | Baseado no modelo v1.3 + `llm_id` (fora do escopo); entidades v1.4 inexistentes. |
| US-10b-RV1 | Nome não vazio; código bloqueado | Parcial | EP03:79-80 | `FormularioMateria.tsx:42-44,128-137`; `route_admin.py:442` | Backend não trava imutabilidade do código. |
| US-10b-RV2 | Mensagem específica ao bloquear desativação | Divergente | EP03:81 | `route_admin.py:470-478`; `materias/page.tsx:142-159` | Textos genéricos; lógica v1.3. |
| US-10b-RI1 | Listagem c/ ações; confirmação; badge | Parcial | EP03:85-87 | `materias/page.tsx:205-238,279-339,186-198` | Frase principal de confirmação OK; complemento diverge. |
| US-10b-CA | Critérios de aceite US-10b | Divergente | EP03:100-106 | `service_materia.py:93-134` | Código mutável; bloqueio sobre modelo v1.3. |
| US-11-RN1 | Apenas admin cadastra turma | Implementado | EP03:118 | `route_turmas.py:72-75` (`@apenas_admins`) | Protegido. |
| US-11-RN2 | Turma independente; código único, semestre, turno | Implementado | EP03:119-120 | `model_turma.py:14-16`; `service_turma.py:64-78` | Código unique/index. |
| US-11-RN3 | Turma fechada: acesso automático às ofertas (US-13) | Ausente | EP03:121 | `service_vinculos.py:10-26` | Sem entidade de oferta nem propagação de acesso. |
| US-11-RV1 | Código único c/ mensagem | Implementado | EP03:125 | `route_turmas.py:90-95`; `FormularioTurma.tsx:72-74` | Mensagem quase idêntica. |
| US-11-RV2 | Semestre obrigatório (ex 2026.1) | Implementado | EP03:126 | `route_turmas.py:84-85`; `utils/turno.ts:26` | Front valida formato; back valida presença. |
| US-11-RV3 | Turno obrigatório (Manhã/Tarde/Noite) | Divergente | EP03:127 | `route_turmas.py:87-88`; `utils/turno.ts:4-14` | Backend só aceita Matutino/Vespertino/Noturno. |
| US-11-RI1 | Form Código/Semestre/Turno; status; busca/filtros | Implementado | EP03:131-133 | `FormularioTurma.tsx:40-66`; `turmas/page.tsx:282-311`; `service_turma.py:44-61` | Filtros server-side. |
| US-11-CA | Critérios de aceite US-11 | Implementado | EP03:145-147 | `route_turmas.py:72-100` | Cobertos. |
| US-12-RN1 | Vínculo professor↔matéria (entidade MateriaProfessor) | Ausente | EP03:158-162 | Inexistente (grep 0 fora de docs) | Só `ProfessorTurmaMateria` (v1.3). |
| US-12-RN2 | Vínculo é pré-requisito da oferta (US-13) | Ausente | EP03:163 | `service_vinculos.py:96-114` | Cria tripla direta sem pré-requisito. |
| US-12-RV1 | Não duplicar vínculo; mensagem específica | Ausente | EP03:168 | — | Sem rota/serviço/mensagem. |
| US-12-RV2 | Não remover vínculo com ofertas ativas; confirmação | Ausente | EP03:169-170 | `route_vinculos.py:279` (só arquivos) | Sem remoção de vínculo prof↔matéria. |
| US-12-RI1 | Seção "Vínculos"; busca prof/matéria | Ausente | EP03:174-175 | `service_vinculos.ts:32-40` (só GET) | Sem UI. |
| US-12-CA | Critérios de aceite US-12 | Ausente | EP03:185-190 | — | Toda a US-12 v1.4 ausente. |
| US-13-RN1 | Oferta (Prof+Matéria) a turma (MateriaProfessorTurma) | Divergente | EP03:200-203 | `model_professor_turma_materia.py:3-12`; `route_vinculos.py:162-192` | Tripla v1.3 cobre conceito, mas sem pré-requisito; rota com `@apenas_professores` quebrado. |
| US-13-RN2 | Oferta requer vínculo MateriaProfessor existente | Ausente | EP03:204 | `service_vinculos.py:96-114` | Pré-requisito inexistente. |
| US-13-RN3 | Criar oferta concede acesso; remover retira (histórico) | Ausente | EP03:208-209 | — | Sem propagação nem DELETE de oferta. |
| US-13-RV1 | Não duplicar oferta; mensagem; confirmação | Divergente | EP03:213-214 | `service_vinculos.py:107-109`; `route_vinculos.py:186-187` | Checa duplicidade, mas mensagem "Vínculo já existe."; sem remoção. |
| US-13-RI1 | Tela de turma c/ seção "Ofertas" | Ausente | EP03:218-220 | — | Sem página de detalhe de turma. |
| US-13-CA | Critérios de aceite US-13 | Ausente | EP03:230-235 | — | Maioria ausente. |
| US-14-RN1 | Apenas admin matricula/desmatricula | Divergente | EP03:247 | `route_vinculos.py:15-18` (`#@apenas_alunos`) | Restrição comentada → qualquer autenticado matricula. |
| US-14-RN2 | Matrícula → acesso automático às ofertas; multi-turma | Parcial | EP03:248-249 | `service_vinculos.py:10-26`; `model_aluno_turma.py:9-10` | Multimatrícula OK; acesso automático ausente. |
| US-14-RN3 | Desmatrícula retira acesso; só aluno ativo | Ausente | EP03:250-251 | `route_vinculos.py` (sem DELETE alunos_turmas) | Sem desmatrícula; sem checagem de aluno ativo. |
| US-14-RV1 | Não duplicar matrícula; mensagem específica | Divergente | EP03:255 | `service_vinculos.py:20-22`; `route_vinculos.py:37-38` | Mensagem "Vínculo já existe." (diverge). |
| US-14-RV2 | Desmatrícula pede confirmação | Ausente | EP03:256 | — | Sem fluxo. |
| US-14-RI1 | Seção "Alunos" na turma; busca; confirmação | Ausente | EP03:260-262 | `service_vinculos.ts:8-16` (só GET) | Sem UI. |
| US-14-CA | Critérios de aceite US-14 | Parcial | EP03:272-276 | `service_vinculos.py:10-26` | Só matrícula básica/duplicidade. |

### EP-06 — Chat Educacional (US-22, US-23, US-24, US-25)

| ID / US | Requisito (épico) | Status | Evid. épico | Evid. código | Observação |
|---|---|---|---|---|---|
| US-22-RN1 | Acesso só a matérias matriculadas | Parcial | EP06:32 | `service_data.py:16-33`; `validacao_emit.py:26-52`; `event_handler.py:48-60` | Dropdown filtra; socket **não valida matrícula** (só UUID). |
| US-22-RN2 | Sessão por matéria; histórico próprio | Parcial | EP06:33-34 | `registrar_chat.py:5-23`; `event_handler.py:81,118` | Chat por matéria; `sessao_id=None` sempre. |
| US-22-RN3 | IA usa só material indexado da matéria (RAG restrito) | Divergente | EP06:35 | `busca_semantica.py:9-32,57` | RAG restrito implementado, mas **quebrado** (`asyncio.to_thread` bug, l.57). |
| US-22-RV1 | Matéria sem material → aviso específico | Ausente | EP06:39 | `event_handler.py:65-68` (comentado); `busca_semantica.py:55` | Fluxo segue à LLM com contexto vazio. |
| US-22-RV2 | Aluno sem matrícula → tela informativa | Divergente | EP06:40 | `chat/page.tsx:188-195`; `service_data.py:33`; `route_data.py:7-17` | Tela dispara corretamente; só o texto diverge. |
| US-22-RI1 | Direto ao chat, sem tela intermediária | Implementado | EP06:44,67 | `middleware.ts:49`; `chat/page.tsx` | Sem etapa de seleção. |
| US-22-RI2 | Dropdown pré-preenchido (1ª em ordem alfabética) | Divergente | EP06:45,68 | `Header.tsx:45-65`; `page.tsx:44-48`; `service_data.py:22-33` | Sem ordenação alfabética. |
| US-22-RI3 | 4 cartões de boas-vindas **sem ação ao clicar** | Divergente | EP06:47-51,69 | `NoMessageField.tsx:19-31`; `page.tsx:170-175` | Cartões têm `onClick` (injeta prompt). Contradição interna do épico (l.47 vs l.69). |
| US-22-RI4 | Sidebar c/ logo, "Novo Chat", chats recentes (título+matéria) | Implementado | EP06:52,70 | `Aside.tsx:43-80`; `layout.tsx:33-48` | Limita a 5 recentes. |
| US-22-RI5 | Campo de digitação pronto após carregamento | Implementado | EP06:53 | `TextArea.tsx:26-37`; `page.tsx:177-184` | Disponível imediatamente. |
| US-23-RN1 | IA responde só com base no material; não inventa | Parcial | EP06:84-87 | `prompt_builder.py:5-19`; `event_handler.py:60-101` | Só instrução de prompt; sem gate de embasamento. |
| US-23-RN2 | Recupera trechos relevantes (top-k) | Divergente | EP06:85 | `busca_semantica.py:14-32,57` | top_k=5 codificado, mas quebrado (l.57). |
| US-23-RN3 | Sem trecho relevante → não inventar | Ausente | EP06:87,121 | `event_handler.py:65-68` (comentado) | Segue à LLM. |
| US-23-RN4 | IA responde no idioma da pergunta | Divergente | EP06:88 | `prompt_builder.py:8` | Força português. |
| US-23-RN5 | Fallback automático entre provedores de IA | Ausente | EP06:89,126 | `gerar_resposta.py:10-43`; `event_handler.py:93-114` | Só Ollama. (Conflito documental c/ visao.md.) |
| US-23-RV1 | Pergunta vazia bloqueada; botão desabilitado | Parcial | EP06:93,100,122 | `TextArea.tsx:14-17,35`; `validacao_emit.py:35` | Envio bloqueado, mas botão não fica visualmente desabilitado com campo vazio. |
| US-23-RV2 | Limite 1.000 chars + contador + aviso | Ausente | EP06:94,99,123 | `TextArea.tsx:26-37`; `model_mensagem.py:14` | Sem maxLength/contador; modelo aceita 3200. |
| US-23-RV3 | Mensagem de indisponibilidade | Ausente | EP06:95,127 | `event_handler.py:112-114`; `chat/page.tsx:92-97` | Só `console.error`. |
| US-23-RI1 | Botão desabilitado enquanto IA processa | Implementado | EP06:101,124 | `chat/page.tsx:135,89,95`; `TextArea.tsx:29,35` | `podeEnviarMensagem`. |
| US-23-RI2 | Indicador "digitando..." | Parcial | EP06:102,125 | `chat/page.tsx:33,54-90`; `ErrorField.tsx:8-21` | Estados de socket; sem indicador textual dedicado. |
| US-23-RI3 | Resposta em Markdown (sem texto bruto) | Implementado | EP06:103,125 | `MessageField.tsx:3,59` | `ReactMarkdown`. |
| US-23-RI4 | Formato de conversa (balões) | Implementado | EP06:104 | `MessageField.tsx:54-61` | Classes user/LLM. |
| US-23-RNF2 | Não enviar dados pessoais à IA | Implementado | EP06:109 | `prompt_builder.py:1-19`; `event_handler.py:101` | Prompt só com matéria/contexto/histórico/pergunta. |
| US-23-RNF3 | Rastreabilidade da resposta aos trechos | Ausente | EP06:110 | `event_handler.py:116-118`; `model_mensagem.py:6-18` | Sem vínculo a chunks/fontes. |
| US-24-RN1 | Histórico da sessão visível | Implementado | EP06:139,166 | `MessageField.tsx:18-65`; `chat/page.tsx:74-77` | Todas as mensagens renderizadas. |
| US-24-RN2 | IA considera contexto anterior + trechos | Parcial | EP06:140,167 | `chat/page.tsx:115,121`; `event_handler.py:87-101` | Funciona, sem janela de 10. |
| US-24-RN3 | Janela de contexto = últimas 10 trocas | Ausente | EP06:141,168 | `chat/page.tsx:115`; `event_handler.py:87-90`; `service_mensagem.py:17-33` | Envia histórico inteiro; `buscar_ultimas_n_mensagens` não usado. |
| US-24-RI2 | Mensagens user/IA diferenciadas | Implementado | EP06:152,169 | `MessageField.tsx:55-58` | OK. |
| US-24-RN5 | Reabrir chat → nova conversa | Implementado | EP06:143 | `chat/page.tsx:148-158`; `Aside.tsx:39-42` | `deleteAllMessages` no mount. |
| US-25-RN1 | Detecção de baixa confiança (não inventar) | Ausente | EP06:181-191,214 | `event_handler.py:65-68` (comentado); `MCP_pipeline.py:14-17` (não usado) | Nenhum dos 4 critérios avaliado. |
| US-25-RN2 | Não revelar detalhes técnicos | Divergente | EP06:182 | `event_handler.py:45,63,114,121` | `str(e)` trafega ao cliente (front não exibe). |
| US-25-RV1 | Resposta nunca enviada sem embasamento | Ausente | EP06:195 | `event_handler.py:104-111` | Sempre streama, sem gate. |
| US-25-RI1 | Mensagem "Não encontrei uma resposta..." | Ausente | EP06:200-201 | — | Sem detecção/mensagem. |
| US-25-RNF1 | Detecção dentro de 30s | Não verificável | EP06:205 | N/A | Sem detecção + depende de ambiente. |

### EP-09 — Gestão do Modelo de IA (US-38, US-38.1)

| ID / US | Requisito (épico) | Status | Evid. épico | Evid. código | Observação |
|---|---|---|---|---|---|
| US-38-RN1 | Scraping da biblioteca oficial do Ollama | Ausente | EP09:32 | `scraping_handler.py:38` (genérico) | Sem referência a ollama.com/library. |
| US-38-RN2 | Consultar API local p/ instalados (/api/tags) | Ausente | EP09:33 | `gerar_resposta.py:22` (só /api/generate) | Sem /api/tags. |
| US-38-RN3 | Estados Instalado/Disponível | Ausente | EP09:34 | `catalogoLLM/page.tsx:4-7` (vazio) | Tela vazia. |
| US-38-RN4 | Pull via API antes de ativar | Ausente | EP09:35 | — (sem /api/pull) | Sem download. |
| US-38-RN5 | Progresso de download em tempo real | Ausente | EP09:36 | — | Sem download. |
| US-38-RN6 | Modal de confirmação ao ativar | Ausente | EP09:37,55-59 | `catalogoLLM/page.tsx:4-7` | Sem UI/modal. |
| US-38-RN7 | Definir modelo como ativo | Parcial | EP09:38 | `service_llm.py:5-24`; `route_llm.py:10-30` | Lógica existe; sem rota POST nem UI. |
| US-38-RN8 | Modelo ativo persistido e usado na geração | Parcial | EP09:39 | `model_llm.py:8-13`; `event_handler.py:93-94`; `service_llm.py:64` | Depende da **coluna `status` sem migration** (GAP-01). |
| US-38-RN9 | Um ativo por vez; troca sem reprocessar | Parcial | EP09:40 | `service_llm.py:20-21` | Unicidade em app; só via serviço. |
| US-38-RN10 | Configuração global | Implementado | EP09:41 | `service_llm.py:55-65`; `event_handler.py:93`; `test_modelo_ativo.py:120-143` | Modelo global. |
| US-38-RV1 | Mensagem de falha de scraping | Ausente | EP09:45 | — | Sem scraping/mensagem. |
| US-38-RV2 | Mensagem "Ollama não encontrado" | Ausente | EP09:46 | `gerar_resposta.py:33` | Erro genérico no chat. |
| US-38-RV3 | Mensagem de falha de download | Ausente | EP09:47 | — | Sem download. |
| US-38-RV4 | Não ativar modelo não instalado | Divergente | EP09:48 | `service_llm.py:16` | Só verifica registro em banco, não instalação. |
| US-38-RI1 | Lista c/ nome, tamanho, estado | Ausente | EP09:52 | `catalogoLLM/page.tsx:4-7`; `Aside.tsx:16` | Menu existe; tela vazia; sem "tamanho". |
| US-38-RI2 | Botões Ativar/Fazer Download | Ausente | EP09:53 | — | Tela vazia. |
| US-38-RI3 | Modelo ativo destacado (badge) | Ausente | EP09:54 | `route_llm.py:10-30` (não consumido) | Sem UI. |
| US-38-RI4 | Modal de ativação (textos exatos) | Ausente | EP09:55-59 | — | Sem componente. |
| US-38-RI5 | Barra de progresso c/ cancelar | Ausente | EP09:60 | — | Sem UI. |
| US-38-RI6 | Confirmação "Modelo [nome] ativado" | Ausente | EP09:61 | `route_llm.py` (só GET) | Sem rota/UI. |
| US-38-RNF1 | Progresso em tempo real (SSE/polling) | Ausente | EP09:65 | `event_handler.py:107-111` (só chat) | Sem download. |
| US-38-RNF2 | Troca não interrompe sessões em andamento | Divergente | EP09:66 | `event_handler.py:93`; `test_modelo_ativo.py:87-117` | Resolve por mensagem; novo modelo já na próxima mensagem da sessão. |
| US-38-RNF3 | Cache de 1h da lista | Ausente | EP09:67 | — | Sem listagem/cache. |
| US-38-PR1 | Apenas admin autenticado acessa | Divergente | EP09:71; RBAC:211 | `route_llm.py:1-30` | Sem auth backend; padrão existe mas é omitido. |
| US-38-CA | Critérios de aceite US-38 | Ausente | EP09:76-87 | `service_llm.py`; `event_handler.py:93` | Só persistência/uso parciais (comprometidos por GAP-01). |
| US-38.1-RN1 | Migration add_status_column_to_llm.py | Ausente | EP09:97-99,110 | migrations llm (3 arquivos) | **Migration não existe**; coluna só no model. |
| US-38.1-RN2 | Model com coluna status | Implementado | EP09:99 | `model_llm.py:8-13` | Enum NOT NULL default 'desativada'. |
| US-38.1-RN3 | Service ativação/desativação | Implementado | EP09:99,105 | `service_llm.py:5-65` | Garante unicidade do ativo. |
| US-38.1-RN4 | Testes do service | Parcial | EP09:99 | `tests/migration/test_llm.py`; `test_modelo_ativo.py` | Mockam db (não tocam schema); chave stale 'model_id'. |
| US-38.1-RN5 | Coluna NOT NULL/default persistida após restart | Divergente | EP09:103-106,110-113 | `model_llm.py:8-13` | CA marcados [v], mas migration inexistente. |

---

## Gaps por Épico

### EP-01 — Autenticação

**GAP-01-A (US-01/GAP-02) — Decorators de perfil quebrados** · **Severidade: Crítica**
- **Épico exige:** controle de acesso por perfil coerente (EP01:35-38; RBAC relacionado).
- **Código faz:** JWT grava `role` como nome (`'PROFESSOR'/'ALUNO'`, `route_usuarios.py:129,192` via `model_usuario.py:38`), mas `apenas_professores` (`auth_decorators.py:76`) e `apenas_alunos` (`:87`) comparam contra `'1'/'2'/'3'` → nunca casam.
- **Impacto:** toda rota protegida por esses decorators (`route_arquivos.py:43,121,197,256,279,335,414`; `route_vinculos.py:47,91,141,164,196,251,281`) retorna **403 incondicional**; professores/alunos não acessam suas funcionalidades.
- **Arquivos:** `auth_decorators.py:76,87`; `jwt_handler.py:5,16-21`; `model_usuario.py:5-8,38`.
- **Ref. complementar:** rbac.md (redirecionamento/403 por perfil).
- **Recomendação:** padronizar o claim `role` (nome em maiúsculas) em geradores e decorators; corrigir `apenas_professores`→'PROFESSOR', `apenas_alunos`→'ALUNO'.
- **Testes:** unitários dos decorators com roles reais; integração de rota de professor/aluno com token correto (200) e incorreto (403).

**GAP-01-B (US-05/GAP-01) — Sessão sem expiração por inatividade configurável** · **Alta**
- **Épico exige:** expiração por inatividade configurável pelo admin (EP01:61,182,207).
- **Código faz:** JWT com exp **absoluta** de 60 min hardcoded (`jwt_handler.py:5,19`); `model_sessao.py` não usado.
- **Impacto:** critério "sessão inativa expira" não atendido; tempo não administrável.
- **Recomendação:** sliding expiration / `last_activity` em `Sessao` + valor configurável.
- **Testes:** expiração por inatividade; renovação por atividade; leitura do valor configurável.

**GAP-01-C (US-03/GAP-03) — Criação de senha não inicia sessão / rota duplicada** · **Alta**
- **Épico exige:** após criar senha, link invalidado e usuário acessa a home do perfil (EP01:132,167).
- **Código faz:** frontend usa `/auth/invite/set-password` (`route_auth.py:55-118`) que **não** inicia sessão → redireciona a `/login`. O endpoint que inicia sessão (`route_admin.py:284-365`) não é chamado e redireciona a `/painel/{role_slug}` (rota inexistente).
- **Recomendação:** unificar em um endpoint que valide confirmação, defina senha, invalide token, emita JWT e retorne destino coerente com `homeForRole`.
- **Testes:** e2e convite→criar senha→sessão iniciada→home do perfil.

**GAP-01-D (US-02/GAP-04) — Mensagens do Google divergentes** · **Média**
- **Código faz:** backend retorna 404 com texto diferente (`route_usuarios.py:122-124`); frontend só mapeia 401/403 (`service_aluno.ts:127-130`).
- **Recomendação:** mapear 404→mensagem de contatar admin; padronizar mensagem genérica de falha do Google.

**GAP-01-E (US-05/GAP-05) — Invalidação de token em memória** · **Média**
- **Código faz:** `TOKENS_INVALIDADOS` é set em memória do processo (`auth_decorators.py:6,23`).
- **Impacto:** logout não é globalmente efetivo (multi-worker/restart); token "encerrado" segue aceito por outros workers.
- **Recomendação:** denylist persistida (Redis/DB) ou sessões server-side.

**GAP-01-F (US-03/GAP-06) — Confirmação de senha só no cliente** · **Média**
- **Código faz:** endpoint usado não valida `passwordConfirmation` (`route_auth.py:96-98`); mensagem literal ausente.
- **Recomendação:** validar confirmação no servidor com a mensagem do épico (consolidar com GAP-01-C).

**GAP-01-G (US-01/GAP-07) — Label "Matrícula"** · **Baixa**
- **Código faz:** `login/page.tsx:128-139` usa "Matrícula" em vez de "Matrícula institucional".

### EP-02 — Gestão de Usuários

**GAP-02-A (US-07/08/09) — Endpoints de gestão de usuários sem autenticação** · **Crítica**
- **Épico exige:** apenas admin autenticado cadastra/edita/desativa/reativa (EP02:33,77,126-128,58,105,152).
- **Código faz:** `GET /usuarios/all`, `POST /usuarios/criar`, `GET/PUT /usuarios/<id>`, `DELETE /usuarios/delete/<id>`, `PATCH /usuarios/<id>/reativar` **sem** `@token_obrigatorio`/`@apenas_admins` (`route_admin.py:22,87,141,173,198,245`). Em `route_admin.py` só as rotas `/materia` têm decorators.
- **Impacto:** qualquer pessoa (até não autenticada) lista/cria/edita/desativa/reativa usuários via API.
- **Ref. complementar:** rbac.md (gestão de usuários = admin total; 403 p/ outros). `GET /alunos/professors` (`route_usuarios.py:256-257`) já é protegido — evidencia o padrão omitido.
- **Recomendação:** aplicar `@token_obrigatorio`+`@apenas_admins` em todas as rotas `/usuarios/*`.
- **Testes:** por endpoint — sem token 401, perfil errado 403, admin 2xx.

**GAP-02-B (US-09) — Desativar não encerra sessão ativa** · **Crítica**
- **Código faz:** `desativar_aluno` (`service_usuario.py:88-96`) não invalida o JWT; `token_obrigatorio` não reconsulta status.
- **Impacto:** usuário desativado mantém acesso a rotas protegidas por ~60 min.
- **Recomendação:** invalidar tokens ativos ao desativar OU reconsultar status no `token_obrigatorio`.

**GAP-02-C (US-09) — Auto-desativação não bloqueada** · **Crítica**
- **Código faz:** sem comparação solicitante×alvo (`route_admin.py:141-169`); endpoint sem `@token_obrigatorio` (sem `g.usuario_id`).
- **Recomendação:** após aplicar auth (GAP-02-A), bloquear `g.usuario_id == alvo` (403).

**GAP-02-D (US-08) — Paginação/busca não server-side** · **Alta**
- **Código faz:** frontend chama `/usuarios/all` sem `page/limit/filtros` e pagina/filtra no cliente (`service_aluno.ts:9-18`; `alunos/page.tsx:40-92`); backend suporta paginação/nome/matrícula mas **não** e-mail (`service_usuario.py:126-142`).
- **Recomendação:** integrar paginação/busca server-side; adicionar filtro por e-mail.

**GAP-02-E (US-09) — Matrícula alterável no backend** · **Alta**
- **Código faz:** bloqueio só no frontend; `alterar_aluno_por_id` grava qualquer matrícula (`service_usuario.py:105`).
- **Recomendação:** ignorar/rejeitar alteração de matrícula no PUT.

**GAP-02-F (US-09) — E-mail duplicado na edição → 500** · **Alta**
- **Código faz:** PUT não valida unicidade nem trata `IntegrityError` (`route_admin.py:198-241`); frontend espera 409 que nunca chega.
- **Recomendação:** verificar e-mail de outro usuário e retornar 409 com mensagem do épico.

**GAP-02-G (US-07/08/09) — Mensagens de duplicidade genéricas** · **Média**
- **Código faz:** backend retorna "Email ou matrícula já cadastrados." (`route_admin.py:128`); frontend marca ambos os campos.
- **Recomendação:** checar matrícula e e-mail separadamente com textos do épico.

**GAP-02-H (US-08) — Validação de e-mail institucional inconsistente** · **Média**
- **Código faz:** `FormularioAluno` não exige `@iesb.edu.br` (`:34-36`), mas backend exige (`route_admin.py:120`).

**GAP-02-I (US-07) — Atribuição de role não atômica** · **Média**
- **Código faz:** `criar_usuario` fixa ALUNO (`:29`); frontend faz POST+PUT (`service_professor.ts:28-47`). Se o PUT falhar, fica ALUNO.
- **Recomendação:** permitir role no `/usuarios/criar` (operação atômica).

**GAP-02-J (US-07/08) — Sem opção "cadastrar outro"** · **Baixa**
- **Código faz:** toast + redirect automático (`FormularioAluno.tsx:107-110`).

**GAP-02-K (US-09) — Modelagem role/status no mesmo enum** · **Média**
- **Código faz:** `role` e `status` compartilham `RoleEnum` (`model_usuario.py:5-10,21`) → permite estados inválidos (ex: status=PROFESSOR).
- **Recomendação:** separar `RoleEnum` e `StatusEnum`.

### EP-03 — Gestão de Matérias e Turmas

**G1 (US-12) — Entidade MateriaProfessor inexistente** · **Crítica**
- **Épico exige:** vínculo professor↔matéria (sem turma) como pré-requisito de oferta (EP03:158-163).
- **Código faz:** não há model/tabela/serviço/rota; usa `ProfessorTurmaMateria` (v1.3). Grep 0 fora de docs; migration `54bc685a0304` cria só tabelas v1.3.
- **Recomendação:** criar entidade `MateriaProfessor` (par único) + serviço/rotas admin; refatorar oferta (US-13).

**G2 (US-13) — Oferta MateriaProfessorTurma não conforme** · **Crítica**
- **Código faz:** cria tripla direta sem pré-requisito; sem DELETE de oferta; mensagem genérica; sem propagação de acesso ao chat; rota com `@apenas_professores` quebrado.
- **Recomendação:** referenciar `MateriaProfessor`+turma; validar pré-requisito; DELETE com confirmação; conceder/remover acesso; `@apenas_admins`.

**G3 (US-14) — Matrícula sem proteção de admin** · **Crítica**
- **Código faz:** `POST /alunos_turmas` com `@apenas_alunos` **comentado** (`route_vinculos.py:15-18`); sem checagem de aluno ativo; sem DELETE de desmatrícula.
- **Impacto:** qualquer autenticado matricula alunos.
- **Recomendação:** `@apenas_admins`; validar status ATIVO; criar DELETE de desmatrícula.

**G4 (US-12/13/14) — Sem tela de detalhe de turma** · **Crítica**
- **Código faz:** não há página de detalhe; `service_vinculos.ts` só tem GET.
- **Impacto:** admin não tem UI para ofertas, matrícula ou vínculos.
- **Recomendação:** criar página de detalhe com seções Ofertas/Alunos/Vínculos + funções POST/DELETE.

**G5 (US-10b) — Código da matéria mutável no backend** · **Alta**
- **Código faz:** `updateSubject` sobrescreve `materia.codigo` (`service_materia.py:100`); bloqueio só no frontend.

**G6 (US-10b) — Bloqueio de desativação sobre modelo v1.3** · **Alta**
- **Código faz:** bloqueia por `llm_id` (fora do escopo) e `TurmaMateria` ativa; mensagens genéricas.
- **Recomendação:** checar `MateriaProfessor`/`MateriaProfessorTurma` ativos; mensagem exata (EP03:81).

**G7 (US-12/13) — Decorator `apenas_professores` quebrado** · **Alta**
- **Código faz:** rotas de `turmas_materias`/`professores_turmas_materias` usam `@apenas_professores` (`auth_decorators.py:76`, compara '1'/'2') → **403 universal**.
- **Impacto:** rotas inacessíveis (falha funcional); mesmo corrigido restringiria a professor, não a admin.
- **Recomendação:** corrigir decorator e aplicar `@apenas_admins`.

**G8 (US-11) — Vocabulário de turno divergente** · **Média**
- **Código faz:** backend só aceita Matutino/Vespertino/Noturno (`route_turmas.py:87,117`); front traduz.

**G9 (US-10b) — Textos de confirmação/bloqueio divergentes** · **Média**
- **Código faz:** complemento da confirmação e mensagem de bloqueio divergem do épico (`materias/page.tsx:314-338`).

**G10 (US-10/11) — RNF de tempo (≤5s)** · **Baixa**
- **Código faz:** INSERT simples sem instrumentação. Não verificável estaticamente.

### EP-06 — Chat Educacional

**GAP-06-A (US-25) — Detecção de baixa confiança ausente** · **Crítica**
- **Épico exige:** IA não inventa resposta sem embasamento (4 critérios; EP06:181-191,214).
- **Código faz:** bloco de contexto vazio comentado (`event_handler.py:65-68`); `MCPPipeline.valid_stream` nunca usado; resposta sempre gerada.
- **Impacto:** IA pode alucinar — compromete o núcleo do produto.
- **Recomendação:** gate de confiança (threshold/contexto vazio) antes da LLM + persistir trecho-fonte.

**GAP-06-B (US-22/23) — RAG quebrado em runtime** · **Crítica**
- **Código faz:** `busca_semantica.py:57` → `await asyncio.to_thread(buscar_no_vector_db(query,arquivos_ids))` chama a função e passa o **resultado** como callable → `TypeError` sempre que há material.
- **Recomendação:** `chunks = await asyncio.to_thread(buscar_no_vector_db, query, arquivos_ids)`.

**GAP-06-C (US-24) — Janela de 10 trocas ausente** · **Alta**
- **Código faz:** envia histórico inteiro (`chat/page.tsx:115`; `event_handler.py:87-90`); `buscar_ultimas_n_mensagens(n=20)` não usado.
- **Recomendação:** recortar últimas 10 trocas no backend.

**GAP-06-D (US-23) — Limite de 1.000 chars/contador ausente** · **Alta**
- **Código faz:** `TextArea` sem maxLength/contador; modelo aceita 3200 (`model_mensagem.py:14`).
- **Recomendação:** `maxLength=1000` + contador + validação backend.

**GAP-06-E (US-23) — Sem fallback/mensagem de indisponibilidade** · **Alta**
- **Código faz:** só Ollama; falha → `console.error` (`chat/page.tsx:92-97`).
- **Ref. complementar:** visao.md afirma NÃO haver fallback (resolver divergência primeiro).

**GAP-06-F (US-22) — Acesso ao chat sem validação de matrícula no backend** · **Alta**
- **Código faz:** `validacao_emit.py:32` só valida UUID; socket processa qualquer `materia_id`.
- **Impacto:** aluno consulta matéria não matriculada.
- **Recomendação:** validar `(id_usuario, materia_id)` via `AlunoTurma→TurmaMateria` no handler.

**GAP-06-G (US-22) — Cartões com ação ao clicar** · **Média**
- **Código faz:** `onClick` injeta prompt (`NoMessageField.tsx:20-30`). Contradição interna do épico (l.47 vs l.69).

**GAP-06-H (US-22) — Sem aviso de matéria sem material** · **Média**
- **Código faz:** segue à LLM com contexto vazio (`event_handler.py:65-68` comentado).

**GAP-06-I (US-22) — Dropdown sem ordenação alfabética** · **Média**
- **Código faz:** ordem de iteração (`service_data.py:22-33`); front usa `materias[0]` sem sort.

**GAP-06-J (US-23) — Indicador "digitando..." ausente** · **Média**

**GAP-06-K (US-23) — Botão não desabilita com campo vazio** · **Baixa**

**GAP-06-L (US-23) — Idioma forçado em português** · **Baixa** (`prompt_builder.py:8`)

**GAP-06-M (US-23) — Sem rastreabilidade de fontes** · **Baixa**

**GAP-06-N (US-22) — Texto da tela "sem matrícula" divergente** · **Baixa**

### EP-09 — Gestão do Modelo de IA

**GAP-09-A (US-38.1) — Migration da coluna `status` inexistente** · **Crítica**
- **Épico exige:** migration que adiciona `status` ENUM NOT NULL DEFAULT 'desativada' (CA marcados [v]; EP09:97-99,110-113).
- **Código faz:** nenhuma migration adiciona a coluna; `63125fcdb5a0` é no-op (`pass`); coluna só no model (`model_llm.py:8-13`). Deploy usa `flask db upgrade` (`entrypoint.sh:20`).
- **Impacto:** em produção/CI a tabela `llm` não terá `status` → `ativar_modelo`/`getActiveModel` e o chat falham.
- **Recomendação:** criar migration Alembic alinhada ao model; validar contra banco real.

**GAP-09-B (US-38) — Catálogo dinâmico ausente** · **Crítica**
- **Código faz:** sem scraping de ollama.com/library nem `/api/tags`; só `/api/generate`; sem cache.
- **Recomendação:** serviço de catálogo (scraping c/ cache 1h + `/api/tags`) protegido por admin.

**GAP-09-C (US-38) — Download (pull) ausente** · **Crítica**
- **Código faz:** sem `/api/pull` nem progresso.
- **Recomendação:** `/api/pull` com streaming de progresso (SSE/Socket.IO), cancelamento e falha sem trocar o ativo.

**GAP-09-D (US-38) — UI do catálogo ausente** · **Alta**
- **Código faz:** `catalogoLLM/page.tsx:4-7` vazio; só item de menu (`Aside.tsx:16`).
- **Recomendação:** implementar tela (lista, badge, modal com textos exatos, progresso, toasts).

**GAP-09-E (US-38) — Sem rota/UI de ativação** · **Alta**
- **Código faz:** `service_llm.ativar_modelo` existe, mas `route_llm.py` só tem `GET /llm/active`.
- **Recomendação:** `POST /llm/<id>/activate` protegido por admin.

**GAP-09-F (US-38) — `route_llm` sem autenticação** · **Alta**
- **Código faz:** sem `@token_obrigatorio`/`@apenas_admins`; `/llm/active` público.
- **Recomendação:** aplicar decorators existentes.

**GAP-09-G (US-38) — Sem mensagens de erro específicas / valida só registro** · **Média**

**GAP-09-H (US-38.1) — Divergência de schema (PK model_id vs id+nome)** · **Baixa**

---

## Divergências Documentais

> Inconsistências entre os épicos e RBAC/sitemap/visão (ou entre épicos). **Não** são tratadas como falha de código.

1. **Destino do aluno após login.** EP-01 US-01 (l.38) diz "tela de seleção de matéria"; EP-06 US-22 (l.44,67) e sitemap 4.1 dizem que **não há tela intermediária** (vai direto ao chat). Divergência épico×épico (e épico×sitemap). O código segue EP-06.
2. **Fallback entre provedores de IA.** EP-06 US-23 (l.89,126) exige fallback automático; visao.md RN-02 (l.258) afirma que **não há fallback** (Ollama indisponível = erro); EP-09 corrobora modelo único. Contradição direta de regra de negócio.
3. **Modelo de associação US-12.** EP-03 v1.4: US-12 = professor↔matéria (`MateriaProfessor`). rbac.md 3.4 e sitemap 2.4.4 ainda descrevem US-12 como "Associação turma+matéria (TURMA_MATERIA)". Documentos de apoio desatualizados frente ao épico.
4. **Modelo de associação US-13.** EP-03 v1.4: US-13 = oferta `MateriaProfessorTurma` (depende de US-12). rbac.md 3.5/sitemap 2.4.5 modelam como `PROFESSOR_TURMA_MATERIA` direto, sem pré-requisito. Divergência de modelo e nomenclatura.
5. **Numeração de telas do sitemap (2.4.4/2.4.5).** O sitemap mapeia US-12/US-13 a telas cujas descrições não correspondem ao conteúdo atual dessas US (refatoração v1.4 não propagada).
6. **Local de gestão das associações.** EP-03 US-12 (l.174) coloca os vínculos na tela de professores/matérias; sitemap 2.4.3 concentra tudo no "Detalhe da turma".
7. **Numeração US-14.** Colisão: US-14 é "Matrícula de aluno" (EP-03) e também "Envio de material" (EP-04, conforme sitemap 3.2.2 e diagrama). Como não há arquivo EP-04, a numeração conflita.
8. **Mensagem de escalonamento.** EP-06 US-25 (l.200): "Não encontrei uma resposta nos materiais disponíveis."; visao.md 9.1 acrescenta "Sua dúvida foi enviada ao professor." Copy divergente.
9. **Escalonamento ao professor (EP-07).** rbac/sitemap/visão descrevem o módulo (US-26 a US-29), mas **não há arquivo de épico EP-07**; EP-06 só referencia marginalmente.
10. **Numeração das US de escalonamento.** Dentro do próprio sitemap, US-27 do EP-07 aparece com dois significados conflitantes.
11. **Módulos sem épico (EP-04/EP-05/EP-08).** Materiais, ingestão e dashboard são detalhados/numerados em rbac/sitemap/visão (US-15, US-17, US-30 a US-34) mas **não têm arquivo de épico**.
12. **Login por matrícula vs matrícula OU e-mail.** EP-01 US-01 restringe à matrícula; visao.md (RN-07/RN-08/RF-01) e sitemap 1.1 permitem matrícula **ou** e-mail.
13. **Escopo do professor.** EP-03 introduz vínculo professor↔matéria desacoplado de turma (US-12); rbac.md modela escopo do professor só por "turmas+matérias".
14. **US-11b inexistente.** Sitemap 2.4.1/2.4.2 referenciam "EP-03/US-11b" (editar/desativar turma) que não existe no épico (há US-10b para matéria, sem equivalente para turma).
15. **US-06b e US-35 inexistentes no EP-02.** Sitemap 2.2.1/2.2.2 (US-06b cadastro de admin) e fluxo 5.5 (US-35 perfil do usuário) referenciam US ausentes do arquivo do EP-02.
16. **US-36 (tema) atribuída ao EP-01.** Sitemap fluxo 5.6 referencia "EP-01/US-36" (seletor de tema), inexistente no épico; EP-01 também menciona US-06 ("Esqueci minha senha") sem especificá-la.
17. **EP-09 — CA marcados como concluídos.** US-38.1 marca os critérios como [v] ("Migration criada e aplicada"), mas a migration não existe (divergência status declarado × código).
18. **EP-09 — schema e nomes de arquivos.** Épico descreve PK `model_id` + `status` (sem `nome`); código usa PK `id` + `nome` + `status`. Nomes citados (`llm.py`, `tests/test_llm.py`) divergem dos reais (`model_llm.py`, `application/tests/migration/test_llm.py`).

---

## Funcionalidades dos Épicos Ausentes

> Apenas itens **especificados nos épicos** sem evidência relevante no código.

**EP-01:**
- Expiração de sessão por **inatividade configurável** pelo admin (US-05-RN2).

**EP-02:**
- Validação server-side de **e-mail único na edição** com mensagem (US-09-RV1/AC2).
- **Encerramento da sessão ativa ao desativar** usuário (US-09-RV2).
- Bloqueio de **auto-desativação** do admin (US-09-RV3).

**EP-03 (núcleo do v1.4):**
- Entidade/fluxo **MateriaProfessor** — vínculo professor↔matéria (US-12 inteira).
- **Pré-requisito** de vínculo para oferta (US-13-RN2).
- **Acesso automático** do aluno às ofertas da turma (US-11-RN3, US-13-RN3, US-14-RN2 parcial).
- **Desmatrícula** de aluno (US-14-RN3/RV2).
- **Telas/seções** de Ofertas, Alunos e Vínculos no detalhe de turma (US-12-RI1, US-13-RI1, US-14-RI1).

**EP-06:**
- **Detecção de baixa confiança** e não-invenção (US-25 inteira; US-23-RN3).
- **Janela de contexto de 10 trocas** (US-24-RN3).
- **Limite de 1.000 caracteres** + contador + aviso (US-23-RV2).
- **Fallback de provedor** + mensagem de indisponibilidade (US-23-RN5/RV3).
- **Aviso de matéria sem material** (US-22-RV1).
- **Rastreabilidade** da resposta aos trechos (US-23-RNF3).

**EP-09:**
- **Scraping da biblioteca Ollama** + cache 1h (US-38-RN1/RNF3).
- **Consulta de instalados** (`/api/tags`) e estados Instalado/Disponível (US-38-RN2/RN3).
- **Download (pull)** + progresso em tempo real (US-38-RN4/RN5/RNF1).
- **Modal de confirmação**, botões e **toda a UI do catálogo** (US-38-RN6/RI1-RI6).
- **Migration da coluna `status`** na tabela `llm` (US-38.1-RN1).
- Mensagens de erro específicas (US-38-RV1/RV2/RV3).

---

## Funcionalidades Implementadas Fora do Escopo dos Épicos

> Código encontrado que **não** corresponde a nenhum dos 5 épicos com arquivo. Mapeado, quando possível, ao módulo de apoio relacionado (EP-04/EP-07/EP-08).

| Funcionalidade | Arquivos (principais) | Doc relacionado |
|---|---|---|
| **Upload e ingestão de materiais (arquivos)** — upload, validação de extensões, metadados, extração (Docling/Whisper), indexação no ChromaDB | `route_arquivos.py:41`; `service_arquivo.py:23,41,68,92`; `libs/docling_handler.py`, `whisper_handler.py`; `service_arquivo.ts:15` | EP-04 (RF-14–19); visao 5.2; sitemap 3.2.2; rbac 3.7 |
| **Upload via links externos (scraping Selenium)** | `route_arquivos.py:119`; `service_arquivo.py:188`; `libs/scraping_handler.py`; `service_link.ts:5` | EP-04 (RF-15/RF-23) |
| **Upload via texto direto** | `route_arquivos.py:195`; `service_arquivo.py:255`; `service_arquivo.ts:45` | EP-04 (RF-14) |
| **Gestão de arquivos (obter/download/editar/excluir/listar)** | `route_arquivos.py:254,277,333,412,448`; `service_arquivo.py:318-512` | EP-04 (RF-17–19); rbac 3.7; sitemap 3.2.1 |
| **Vínculo Arquivo-Turma-Matéria** (associação material↔turma+matéria) | `route_vinculos.py:217,249,279`; `service_vinculos.py` (arquivo_turma_materia); `service_vinculos.ts:44,54` | EP-04; rbac 3.7 |
| **Página de upload de fontes (professor)** | `professor/pages/upload/page.tsx:14`; `SourceUpload.tsx`; `professor/components/Aside/Aside.tsx:50` | EP-04 (RF-14); sitemap 3.2.2; visao 9.2 |
| **Detalhe de matéria do professor (listagem de fontes)** | `professor/pages/materias/materia/[materiaId]/page.tsx:18`; `professor/pages/materias/page.tsx` | EP-04 (RF-19); sitemap 3.2.1; rbac 3.7 |
| **Dashboard analítico do professor (estatísticas/KPIs)** — dados mock/estáticos | `professor/pages/estatisticas/page.tsx:12`; `CardPequeno/CardMedio/BarraDeProgresso`; `Aside.tsx:56` | EP-08 (RF-41–45); sitemap 3.4; rbac 3.10; visao 9.5 |
| **Home do professor com KPIs e ações rápidas** (mock) | `professor/page.tsx:9`; `CardPequeno.tsx` | EP-08; sitemap 3.1/3.4 |
| **Detalhe de turma do professor com estatísticas** (mock) | `professor/pages/turmas/turma/[turmaId]/page.tsx:18` | EP-08; sitemap 3.4; rbac 3.10 |
| **Chat Tutor para o professor** | `professor/page.tsx:70`; `professor/components/Aside/Aside.tsx:62` | Nenhum (EP-06 restringe chat ao aluno; rbac diz que professor não interage com o chat) |
| **Endpoint genérico `/data` (matérias/turmas do usuário)** | `route_data.py:7,19`; `service_data.py:5,16`; `service_data.ts:6,16` | Parcialmente EP-06/US-22; `/data` não descrito em épico |
| **Migração de metadados do ChromaDB (`arquivo_id`)** | `route_arquivos.py:18`; `service_arquivo.py:514` | Nenhum (tarefa técnica) |
| **Criação de vínculos turma-matéria / professor-turma-matéria pelo professor** | `route_vinculos.py:89,162` (`@apenas_professores`), `:15` (`@apenas_alunos` comentado) | EP-03 atribui essas ações ao Admin; rbac 3.4/3.5/3.6 |

---

## Cobertura de Testes por Épico

### EP-01 — Autenticação
- **Testes encontrados:** `tests/routes/test_login_google.py` (US-02: 400/401/403/404/200, não cria usuário); `tests/routes/test_primeiro_acesso.py` (US-03: criar usuário, e-mail de convite, validação de token 200/410, recriar_senha, força de senha, token used). *(Obs.: mocks usam `role='3'`/`'RoleEnum.ALUNO'`, divergente do `to_dict` real → não detectam o mismatch de role do GAP-01-A.)*
- **Requisitos sem teste:** login matrícula/senha (sucesso/401 genérico/403 inativo/400); `/encerrar-sessao` e invalidação; expiração; decorators `apenas_professores`/`apenas_alunos` (GAP-01-A); endpoint realmente usado `/auth/invite/set-password`; todo o frontend.
- **Testes recomendados:** `test_login` (200+cookie, 401 genérico, 403 inativo, 400); decorators de RBAC com nomes reais; `/auth/invite/set-password`; logout/expiração; frontend (mensagens, mapeamento de erros Google, redirect por perfil, middleware).

### EP-02 — Gestão de Usuários
- **Testes encontrados:** `tests/routes/test_primeiro_acesso.py` cobre criação + convite + primeiro acesso (US-07/08). **Nenhum teste de frontend** (Glob só retorna node_modules).
- **Requisitos sem teste:** autorização dos endpoints (GAP-02-A), encerramento ao desativar (GAP-02-B), auto-desativação (GAP-02-C), paginação/busca server-side (GAP-02-D), matrícula imutável backend (GAP-02-E), e-mail único na edição (GAP-02-F), edição/desativação/reativação, mensagens de duplicidade, role atômica, modelagem role/status.
- **Testes recomendados:** autorização por endpoint (401/403/2xx), auto-desativação (403), invalidação ao desativar, PUT (nome/e-mail, matrícula imutável, 409 e-mail), paginação/filtro server-side; RTL dos formulários e do modal.

### EP-03 — Matérias e Turmas
- **Testes encontrados:** **nenhum** cobrindo o EP-03 (existentes tratam de login/primeiro acesso/sockets/LLM).
- **Requisitos sem teste:** **todos** (US-10, US-10b, US-11, US-12, US-13, US-14).
- **Testes recomendados:** CRUD matéria (código duplicado/imutável, desativação/bloqueio), CRUD turma (semestre/turno, duplicado), RBAC das rotas de associação/oferta/matrícula (regressão do decorator quebrado e da matrícula sem proteção), vínculo professor↔matéria, oferta, matrícula/desmatrícula; formulários no frontend.

### EP-06 — Chat Educacional
- **Testes encontrados:** `tests/socket/` — `test_disparar_emit.py`, `test_registrar_chat.py`, `test_registrar_mensagem.py`, `test_validacao_emit.py` (*sem asserts, usa chave errada `id_materia`*), `test_modelo_ativo.py`. Nenhum teste de frontend.
- **Requisitos sem teste:** RAG e bug `busca_semantica:57`, detecção de baixa confiança (US-25), janela de 10 trocas, limite 1000/botão vazio, fallback/indisponibilidade, restrição backend de matrícula, ordenação do dropdown, cartões sem ação, markdown, aviso de matéria sem material, idioma, rastreabilidade.
- **Testes recomendados:** gate de baixa confiança; integração de `busca_semantica` (com/sem arquivos, cobrindo a correção do `asyncio.to_thread`); recorte de 10 trocas; contador/maxLength; validação backend de `materia_id` não matriculado; fallback + mensagem; ordenação/pré-seleção; cartões sem ação; converter `test_validacao_emit.py` em asserts e corrigir a chave.

### EP-09 — Gestão do Modelo de IA
- **Testes encontrados:** `tests/migration/test_llm.py` (+ duplicado em `backend/tests/migration/test_llm.py`) — mockam `LLM`/`db` (não tocam schema; chave stale `model_id`); `tests/socket/test_modelo_ativo.py` e `tests/routes/test_llm_route.py` (DB real, mas `conftest.py` só ajusta PYTHONPATH, sem `create_all`).
- **Requisitos sem teste:** **a migration real da coluna `status`** (crítico), scraping/cache/`/api/tags`, pull/progresso, UI do catálogo, mensagens de erro, "não ativar não instalado", autorização admin.
- **Testes recomendados:** migration aplicada em banco real (coluna NOT NULL/default); rota POST de ativação (único ativo, 404/401/403); serviço de catálogo (scraping mockado + cache + `/api/tags`); pull (progresso/cancelamento/falha); frontend (lista/badge/modal/progresso); corrigir mocks `model_id`→`id`.

---

## Observações finais

- **Padrão sistêmico de segurança:** regras de autorização frequentemente residem **apenas no frontend** (`middleware.ts`, validação de formulários), com o backend aberto ou com decorators inconsistentes. Recomenda-se uma revisão transversal de autorização no backend (aplicar `@token_obrigatorio`/`@apenas_admins` de forma consistente e padronizar o claim `role`).
- **Modelo de dados EP-03 desatualizado:** o código permanece no modelo v1.3 enquanto o épico (e o diagrama) já estão no v1.4; rbac/sitemap/visão também refletem o modelo antigo — recomenda-se alinhar épico↔documentos↔código antes de implementar US-12/13/14.
- **EP-09 não funcional em produção:** mesmo a parte implementada (modelo ativo) depende de uma coluna sem migration — prioridade de correção imediata.
- **EP-06 com núcleo quebrado:** a correção do bug `asyncio.to_thread` e a implementação do gate de baixa confiança são pré-condições para a proposta de valor do produto ("IA sem alucinação").
