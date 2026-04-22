> **Documento de Requisitos**
> **Projeto Tutor**
> **Responsável:** Patricia Pereira Martins – Time de Requisitos e Testes
> **Data:** Abril/2026
> **Versão:** 1.1 (Consolidada)

---

# Sitemap — Tutor

**Versão:** 1.0
**Data:** Abril de 2026
**Status:** Rascunho

---

## Legenda de acesso por perfil

| Símbolo | Perfil |
|---------|--------|
| `ADM` | Administrador |
| `PRO` | Professor |
| `ALU` | Aluno |

---

## 1. Área pública (sem autenticação)

| # | Tela | Descrição | Acesso |
|---|------|-----------|--------|
| 1.1 | **Login** | Autenticação por matrícula/e-mail + senha ou via conta Google (OAuth). Redireciona para a home do perfil após autenticação. | `ADM` `PRO` `ALU` |
| 1.2 | **Recuperar senha** | Solicitar link de recuperação de senha via e-mail cadastrado. | `ADM` `PRO` `ALU` |
| 1.3 | **Redefinir senha** | Tela acessada via link enviado por e-mail (primeiro acesso por link de convite ou recuperação de senha). Exige definição de nova senha antes de liberar o acesso. | `ADM` `PRO` `ALU` |

---

## 2. Área do Administrador

Acessível apenas por usuários com perfil **Administrador**. Ponto de entrada após login.

| # | Tela | Descrição | Épico/US |
|---|------|-----------|----------|
| 2.1 | **Painel do administrador** | Tela inicial após login do admin. Acesso rápido aos módulos de gestão. | — |
| **2.2** | **Gestão de usuários** | | |
| 2.2.1 | ↳ Lista de administradores | Exibe todos os administradores cadastrados (ativos e desativados). Acesso ao formulário de cadastro de novo administrador. | EP-02 / US-06b |
| 2.2.2 | ↳ Formulário de administrador | Cadastrar novo administrador ou editar dados de um existente. | EP-02 / US-06b |
| 2.2.3 | ↳ Lista de professores | Exibe todos os professores cadastrados (ativos e desativados). Acesso ao formulário de cadastro. | EP-02 / US-07 |
| 2.2.4 | ↳ Formulário de professor | Cadastrar novo professor ou editar dados de um existente. Gera e envia link de convite. | EP-02 / US-07 |
| 2.2.5 | ↳ Lista de alunos | Exibe todos os alunos cadastrados (ativos e desativados). Acesso ao formulário de cadastro. | EP-02 / US-08 |
| 2.2.6 | ↳ Formulário de aluno | Cadastrar novo aluno ou editar dados de um existente. Gera e envia link de convite. | EP-02 / US-08 |
| **2.3** | **Gestão de matérias** | | |
| 2.3.1 | ↳ Lista de matérias | Exibe todas as matérias cadastradas (ativas e desativadas). Acesso ao formulário de cadastro. | EP-03 / US-10, US-10b |
| 2.3.2 | ↳ Formulário de matéria | Cadastrar nova matéria ou editar/desativar uma existente. | EP-03 / US-10, US-10b |
| **2.4** | **Gestão de turmas** | | |
| 2.4.1 | ↳ Lista de turmas | Exibe todas as turmas cadastradas (ativas e desativadas). Acesso ao formulário de cadastro. | EP-03 / US-11, US-11b |
| 2.4.2 | ↳ Formulário de turma | Cadastrar nova turma ou editar/desativar uma existente. | EP-03 / US-11, US-11b |
| 2.4.3 | ↳ Detalhe da turma | Visão consolidada de uma turma: matérias associadas, professores vinculados e alunos matriculados. Ponto de entrada para as ações de vínculo abaixo. | EP-03 |
| 2.4.4 | ↳ Associação de matérias à turma | Associar ou remover matérias de uma turma (TURMA_MATERIA). | EP-03 / US-12 |
| 2.4.5 | ↳ Vínculo de professor a turma+matéria | Vincular ou remover professor de uma combinação turma+matéria (PROFESSOR_TURMA_MATERIA). | EP-03 / US-13 |
| 2.4.6 | ↳ Matrícula de alunos em turma | Matricular ou cancelar matrícula de alunos em uma turma (ALUNO_TURMA). | EP-03 / US-14 |
| **2.5** | **Gestão do modelo de IA** | | |
| 2.5.1 | ↳ Seleção de modelo | Lista de modelos disponíveis na biblioteca do Ollama, com indicação visual de instalados vs. disponíveis para download. Permite ativar modelo instalado ou iniciar download com progresso em tempo real. | EP-09 / US-38 |

---

## 3. Área do Professor

Acessível apenas por usuários com perfil **Professor**. Ponto de entrada após login.

| # | Tela | Descrição | Épico/US |
|---|------|-----------|----------|
| 3.1 | **Home do professor** | Lista das turmas+matérias que o professor leciona. Ponto de entrada para materiais, perguntas e analytics de cada turma+matéria. | EP-03 / US-13 |
| **3.2** | **Gestão de materiais** | | |
| 3.2.1 | ↳ Lista de materiais | Exibe todos os materiais enviados pelo professor, com nome, tipo, turma+matéria, data de envio e status (Na fila / Processando / Disponível / Erro / Desativado). Filtros por matéria, turma, tipo e status. | EP-04 / US-15, US-17 |
| 3.2.2 | ↳ Envio de material | Upload de arquivos, inclusão de URLs ou texto direto como material didático. Seleção de turma+matéria de destino. | EP-04 / US-14 |
| **3.3** | **Perguntas escalonadas** | | |
| 3.3.1 | ↳ Fila de pendentes | Lista de perguntas encaminhadas pela IA que ainda não foram respondidas. Exibe nome do aluno (anonimizado?), matéria/turma, data e contexto da conversa. Permite responder ou marcar como "Não consegui responder". | EP-07 / US-27, US-28 |
| 3.3.2 | ↳ Histórico de perguntas | Todas as perguntas recebidas (em aberto e respondidas), em abas separadas. Filtros por matéria, turma e período. Busca por texto. | EP-07 / US-28 |
| **3.4** | **Dashboard analítico** | | |
| 3.4.1 | ↳ Engajamento da turma | KPIs de uso: alunos ativos, total de perguntas, alunos sem interação, horários de pico, evolução semanal. | EP-08 / US-30 |
| 3.4.2 | ↳ Dúvidas frequentes | Clusters semânticos das perguntas mais frequentes, com pergunta representativa e contagem de alunos. | EP-08 / US-31 |
| 3.4.3 | ↳ Efetividade dos materiais | Ranking de materiais por uso, materiais nunca consultados, materiais com mais lacunas. | EP-08 / US-32 |
| 3.4.4 | ↳ Lacunas de conteúdo | Taxa de escalonamento, distribuição por tipo de lacuna, tópicos sistematicamente sem resposta. | EP-08 / US-33 |
| 3.4.5 | ↳ Padrões de uso da IA | Categorização de intenção das perguntas: exercícios, resumo, conceitual, aplicação, outras. | EP-08 / US-34 |

---

## 4. Área do Aluno

Acessível apenas por usuários com perfil **Aluno**. Ponto de entrada após login.

| # | Tela | Descrição | Épico/US |
|---|------|-----------|----------|
| 4.1 | **Chat (tela inicial do aluno)** | Tela apresentada diretamente após o login. Contém: sidebar com lista de chats recentes (título + matéria), barra superior com combobox de seleção de matéria, nome e avatar do usuário, seletor de tema. Tela de boas-vindas exibe 4 cartões de ação rápida quando não há conversa ativa. | EP-06 / US-22 |
| 4.2 | **Conversa ativa** | Interface de conversa com a IA. Exibe histórico de mensagens, campo de pergunta, indicador de processamento e fontes do material ao final de cada resposta da IA. | EP-06 / US-23, US-24, US-25 |
| 4.3 | **Minhas dúvidas encaminhadas** | Lista das perguntas que o aluno encaminhou ao professor, com status (Aguardando resposta / Respondida) e resposta do professor quando disponível. Filtros por matéria e status. | EP-07 / US-29 |

---

## 5. Fluxos transversais

Comportamentos que ocorrem em múltiplas áreas do sistema, sem tela dedicada própria.

| # | Comportamento | Descrição | Épico/US |
|---|---------------|-----------|----------|
| 5.1 | **Encerramento de sessão** | Opção disponível em todas as telas autenticadas (menu ou botão de saída). Encerra a sessão e redireciona para o login. | EP-01 / US-05 |
| 5.5 | **Perfil do usuário** | Acessível clicando no nome ou avatar na barra superior (qualquer perfil). Permite editar nome, solicitar troca de e-mail e alterar senha. | EP-02 / US-35 |
| 5.6 | **Seletor de tema visual** | Componente na barra superior (qualquer perfil). Permite alternar entre os temas Claro, Escuro e Índigo com efeito imediato. | EP-01 / US-36 |
| 5.2 | **Notificação de pergunta escalonada** (professor) | O professor recebe notificação quando uma nova pergunta é encaminhada pela IA. O contador no menu de perguntas pendentes é atualizado em tempo real. | EP-07 / US-26, US-28 |
| 5.3 | **Notificação de resposta do professor** (aluno) | O aluno recebe notificação quando o professor responde uma de suas perguntas encaminhadas. | EP-07 / US-27 |
| 5.4 | **Notificação de processamento de material** (professor) | O professor recebe notificação quando um material conclui o processamento (status Disponível) ou quando ocorre um erro. | EP-04 / US-15 |
