> **Documento de Requisitos**
> **Projeto Tutor**
> **Responsável:** Patricia Pereira Martins – Time de Requisitos e Testes
> **Data:** Abril/2026
> **Versão:** 1.1 (Consolidada)

---

# RBAC — Controle de Acesso Baseado em Perfil

**Versão:** 1.0
**Data:** Abril de 2026
**Status:** Rascunho

---

## 1. Perfis de acesso

| Perfil | Descrição | Como é criado |
|--------|-----------|---------------|
| **Administrador** | Gerencia usuários, matérias, turmas e configurações da plataforma. Não interage com o chat educacional. | Primeiro admin via seed/implantação. Demais admins criados por outro administrador via convite. |
| **Professor** | Envia materiais, responde perguntas escalonadas e consulta analytics das suas turmas. | Criado por administrador via link de convite. |
| **Aluno** | Usa o chat educacional para tirar dúvidas sobre as suas matérias. | Criado por administrador via link de convite. |

---

## 2. Resumo de acesso por módulo

| Módulo | Administrador | Professor | Aluno |
|--------|:-------------:|:---------:|:-----:|
| Autenticação (login, recuperar senha) | Sim | Sim | Sim |
| Gestão de administradores | **Total** | — | — |
| Gestão de professores | **Total** | — | — |
| Gestão de alunos | **Total** | — | — |
| Gestão de matérias | **Total** | — | — |
| Gestão de turmas | **Total** | — | — |
| Associação turma+matéria | **Total** | — | — |
| Vínculo professor a turma+matéria | **Total** | — | — |
| Matrícula de aluno em turma | **Total** | — | — |
| Gestão do modelo de IA (Ollama) | **Total** | — | — |
| Upload e gestão de materiais didáticos | — | **Próprios** | — |
| Perguntas escalonadas (responder) | — | **Próprias turmas** | — |
| Histórico de perguntas escalonadas | — | **Próprias turmas** | — |
| Dashboard analítico (KPIs) | — | **Próprias turmas** | — |
| Chat educacional | — | — | **Próprias matérias** |
| Consulta de dúvidas encaminhadas | — | — | **Próprias** |

---

## 3. Matriz de permissões detalhada

As ações possíveis são:
- **C** — Criar
- **R** — Ler / Listar
- **U** — Editar / Atualizar
- **D** — Desativar (exclusão lógica — registros nunca são apagados fisicamente)
- **—** — Sem acesso

### 3.1 Usuários

| Recurso | Administrador | Professor | Aluno |
|---------|:-------------:|:---------:|:-----:|
| Administrador — próprio perfil | R / U | — | — |
| Administrador — outros | C / R / U / D | — | — |
| Professor | C / R / U / D | R (próprio perfil) | — |
| Aluno | C / R / U / D | — | R (próprio perfil) |

**Restrições:**
- O administrador principal (cadastrado via seed) **não pode ser desativado** por nenhum administrador, incluindo ele próprio.
- Um administrador **não pode desativar o último administrador ativo** da plataforma.
- Um administrador **não pode alterar o próprio perfil para outro perfil** (ex: se rebaixar para professor).
- Professor e aluno podem editar apenas dados do próprio perfil (nome, e-mail, senha).

---

### 3.2 Matérias

| Ação | Administrador | Professor | Aluno |
|------|:-------------:|:---------:|:-----:|
| Criar matéria | Sim | — | — |
| Listar matérias | Sim (todas) | Sim (vinculadas a ele) | — |
| Editar matéria | Sim | — | — |
| Desativar matéria | Sim | — | — |

**Restrições:**
- Matéria desativada não pode ser associada a novas turmas.
- A desativação de uma matéria não remove automaticamente as associações existentes — elas devem ser gerenciadas manualmente.

---

### 3.3 Turmas

| Ação | Administrador | Professor | Aluno |
|------|:-------------:|:---------:|:-----:|
| Criar turma | Sim | — | — |
| Listar turmas | Sim (todas) | Sim (vinculadas a ele) | Sim (matriculado) |
| Editar turma | Sim | — | — |
| Desativar turma | Sim | — | — |

---

### 3.4 Associação turma+matéria (TURMA_MATERIA)

| Ação | Administrador | Professor | Aluno |
|------|:-------------:|:---------:|:-----:|
| Associar matéria a turma | Sim | — | — |
| Listar matérias de uma turma | Sim | Sim (suas turmas) | Sim (suas turmas) |
| Remover associação | Sim | — | — |

---

### 3.5 Vínculo professor a turma+matéria (PROFESSOR_TURMA_MATERIA)

| Ação | Administrador | Professor | Aluno |
|------|:-------------:|:---------:|:-----:|
| Vincular professor a turma+matéria | Sim | — | — |
| Listar professores de uma turma+matéria | Sim | Sim (suas turmas) | — |
| Remover vínculo | Sim | — | — |

---

### 3.6 Matrícula de aluno em turma (ALUNO_TURMA)

| Ação | Administrador | Professor | Aluno |
|------|:-------------:|:---------:|:-----:|
| Matricular aluno em turma | Sim | — | — |
| Listar alunos de uma turma | Sim | Sim (suas turmas) | — |
| Cancelar matrícula | Sim | — | — |

---

### 3.7 Materiais didáticos

| Ação | Administrador | Professor | Aluno |
|------|:-------------:|:---------:|:-----:|
| Enviar material | — | Sim (suas turmas+matérias) | — |
| Listar materiais | — | Sim (suas turmas+matérias) | — |
| Visualizar status de processamento | — | Sim (seus materiais) | — |
| Desativar (remover da base de conhecimento) | — | Sim (seus materiais) | — |

**Restrições:**
- O professor só pode enviar e gerenciar materiais das turmas+matérias às quais está vinculado.
- A desativação de um material remove-o imediatamente da base de conhecimento da IA, mas mantém o arquivo armazenado para fins de histórico e auditoria.
- Um material desativado não pode ser reativado — deve ser reenviado como novo.
- Se o mesmo material estiver associado a mais de uma turma+matéria, o professor pode desativá-lo em uma associação específica ou em todas.

---

### 3.8 Chat educacional

| Ação | Administrador | Professor | Aluno |
|------|:-------------:|:---------:|:-----:|
| Iniciar conversa em uma matéria | — | — | Sim (suas matérias) |
| Enviar pergunta | — | — | Sim |
| Receber resposta da IA | — | — | Sim |
| Visualizar histórico da sessão | — | — | Sim (próprio) |

**Restrições:**
- O aluno só pode acessar o chat de matérias em que está matriculado.
- O histórico de cada sessão é visível apenas ao aluno que a iniciou.
- A IA responde exclusivamente com base nos materiais indexados da matéria em questão.

---

### 3.9 Escalonamento de perguntas

| Ação | Administrador | Professor | Aluno |
|------|:-------------:|:---------:|:-----:|
| Encaminhar pergunta ao professor (automático) | — | — | Automático pelo sistema |
| Visualizar fila de perguntas pendentes | — | Sim (suas turmas+matérias) | — |
| Responder pergunta escalonada | — | Sim (suas turmas+matérias) | — |
| Marcar pergunta como "Não consegui responder" | — | Sim (suas turmas+matérias) | — |
| Visualizar histórico de perguntas (respondidas + em aberto) | — | Sim (suas turmas+matérias) | — |
| Consultar próprias perguntas encaminhadas | — | — | Sim (próprias) |
| Ler resposta do professor | — | — | Sim (próprias) |

**Restrições:**
- O professor visualiza apenas perguntas das turmas+matérias às quais está vinculado.
- Em matérias com múltiplos professores, todos recebem notificação e qualquer um pode responder. Após respondida por um, a pergunta sai da fila de todos.
- Uma pergunta marcada como "Não consegui responder" permanece na fila para os demais professores vinculados (se houver).
- O aluno visualiza apenas suas próprias perguntas encaminhadas — nunca as de outros alunos.

---

### 3.10 Dashboard analítico (KPIs)

| Ação | Administrador | Professor | Aluno |
|------|:-------------:|:---------:|:-----:|
| Visualizar painel de engajamento | — | Sim (suas turmas+matérias) | — |
| Visualizar dúvidas frequentes | — | Sim (suas turmas+matérias) | — |
| Visualizar efetividade dos materiais | — | Sim (suas turmas+matérias) | — |
| Visualizar lacunas de conteúdo | — | Sim (suas turmas+matérias) | — |
| Visualizar padrões de uso da IA | — | Sim (suas turmas+matérias) | — |
| Exportar dados em CSV | — | Sim (suas turmas+matérias) | — |

**Restrições:**
- O professor visualiza apenas dados analíticos das turmas+matérias às quais está vinculado.
- Os dados de dúvidas frequentes e padrões de uso são exibidos de forma **agregada** — o professor não consegue identificar individualmente qual aluno fez qual pergunta.

---

### 3.11 Gestão do modelo de IA

| Ação | Administrador | Professor | Aluno |
|------|:-------------:|:---------:|:-----:|
| Listar modelos disponíveis (biblioteca Ollama) | Sim | — | — |
| Selecionar / ativar modelo instalado | Sim | — | — |
| Iniciar download de modelo não instalado | Sim | — | — |

**Restrições:**
- Apenas administradores autenticados têm acesso à gestão do modelo de IA.
- A troca de modelo ativo não interrompe sessões de chat em andamento — sessões ativas concluem com o modelo anterior.
- O modelo ativo é global: aplica-se a todas as matérias da plataforma.

---

## 4. Regras de escopo (visibilidade dos dados)

As regras abaixo complementam a matriz de permissões, definindo **quais registros** cada perfil pode visualizar dentro das entidades que tem acesso.

| Perfil | Entidade | Escopo de visibilidade |
|--------|----------|----------------------|
| Administrador | Usuários | Todos os usuários da plataforma |
| Administrador | Matérias | Todas as matérias |
| Administrador | Turmas | Todas as turmas |
| Administrador | Associações e vínculos | Todos |
| Administrador | Materiais didáticos | Não tem acesso |
| Professor | Matérias | Apenas as matérias das turmas+matérias às quais está vinculado |
| Professor | Turmas | Apenas as turmas às quais está vinculado |
| Professor | Alunos | Apenas os alunos matriculados nas suas turmas |
| Professor | Materiais didáticos | Apenas os materiais que ele próprio enviou |
| Professor | Perguntas escalonadas | Apenas perguntas das suas turmas+matérias |
| Professor | Analytics | Apenas dados das suas turmas+matérias |
| Aluno | Matérias | Apenas as matérias das turmas em que está matriculado |
| Aluno | Chat / histórico de sessão | Apenas as próprias sessões |
| Aluno | Perguntas encaminhadas | Apenas as próprias perguntas |

---

## 5. Regras de acesso às telas

| Tela (Sitemap) | Administrador | Professor | Aluno |
|----------------|:-------------:|:---------:|:-----:|
| Login | Sim | Sim | Sim |
| Recuperar senha | Sim | Sim | Sim |
| Redefinir senha | Sim | Sim | Sim |
| Painel do administrador | Sim | — | — |
| Lista/formulário de usuários | Sim | — | — |
| Lista/formulário de matérias | Sim | — | — |
| Lista/formulário de turmas | Sim | — | — |
| Detalhe de turma (associações) | Sim | — | — |
| Gestão de modelo de IA | Sim | — | — |
| Home do professor | — | Sim | — |
| Lista de materiais | — | Sim | — |
| Envio de material | — | Sim | — |
| Fila de pendentes | — | Sim | — |
| Histórico de perguntas (professor) | — | Sim | — |
| Dashboard analítico (todas as abas) | — | Sim | — |
| Home do aluno | — | — | Sim |
| Chat por matéria | — | — | Sim |
| Minhas dúvidas encaminhadas | — | — | Sim |

**Regra geral de redirecionamento:**
- Usuário não autenticado que tenta acessar qualquer rota protegida é redirecionado para `/login`.
- Usuário autenticado que tenta acessar uma rota de outro perfil recebe resposta `403 Forbidden` e é redirecionado para a home do seu próprio perfil.
- Após login bem-sucedido, o sistema redireciona automaticamente para a home do perfil correspondente.
