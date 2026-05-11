> **Documento de Requisitos**
> **Projeto Tutor**

| Versão | Data | Descrição | Autor |
|--------|-----------|---------------|-----------|
| 1.2 Sprint 2 | 19/04/2026 | Criação das histórias de usuário US-08 e US-09 | Patricia Pereira Martins |
| 1.3 Sprint 3 | 08/05/2026 | Criação das histórias de usuário US-07 | Patricia Pereira Martins |

---

# EP-02 — Gestão de Usuários

**Descrição:** Permite ao administrador cadastrar, editar e desativar os usuários da plataforma (administradores, professores e alunos), controlando quem tem acesso e com qual perfil.

**Personas:** Administrador

**Protótipo:** [Design System](https://www.figma.com/design/5MClPpSqI9R42MPCwTcDzH/Tutor----Sprint-2?node-id=258-2&p=f&t=ukWioTEjrb08WqKU-0)

**Protótipo Sprint 2 — Gestão de Usuários:** [Gestão de Usuários](https://www.figma.com/design/5MClPpSqI9R42MPCwTcDzH/Tutor----Sprint-2?node-id=239-5&p=f&t=ukWioTEjrb08WqKU-0)

**Protótipo Sprint 3 — Gestão de Usuários:** [Gestão de Usuários](https://www.figma.com/design/zmoOcbWpUlzlRtJMoqwjPC/Tutor----Sprint-3?node-id=239-4&p=f&t=YQYt419AlJk2mdgq-0)

---

## US-07 — Cadastro de professor

**Como** administrador,
**quero** cadastrar um professor na plataforma informando seus dados básicos,
**para que** ele possa acessar a plataforma, gerenciar materiais para a IA responder as perguntas dos alunos.

### Regras de Negócio

- Apenas o administrador pode cadastrar professores.
- O professor recebe automaticamente o perfil "Professor" no cadastro.
- Ao ser cadastrado, o professor recebe um link de convite por e-mail para criar sua própria senha antes do primeiro acesso.
- Um professor pode ser vinculado a uma ou mais matérias após o cadastro.
- A matrícula e o e-mail informados devem ser únicos na plataforma — não é possível ter dois usuários com a mesma matrícula ou mesmo e-mail.

### Regras de Validação

- Nome completo é obrigatório. 
- Matrícula institucional é obrigatória e deve ser única na plataforma.
- E-mail institucional é obrigatório, deve ser único na plataforma e ter formato válido (ex: nome@instituição.br).
- Caso a matrícula já exista, exibir: _"Esta matrícula já está em uso por outro usuário."_
- Caso o e-mail já exista, exibir: _"Este e-mail já está em uso por outro usuário."_

### Regras de Interface

- O formulário de cadastro de professor deve conter os campos: Nome completo, Matrícula, E-mail.
- Ao concluir o cadastro, exibir confirmação e opção de cadastrar outro professor ou voltar à listagem.

### Requisitos Não Funcionais

- O cadastro deve ser confirmado em no máximo 5 segundos após o envio do formulário.

### Pré-requisitos

- O administrador deve estar autenticado.

### Critérios de Aceitação

- [ ] Administrador consegue cadastrar um professor preenchendo os campos obrigatórios.
- [ ] Matrícula ou e-mail duplicados são rejeitados com mensagem explicativa.
- [ ] Professor cadastrado aparece na listagem de usuários com status ativo.
- [ ] Professor recebe e-mail com link de convite e consegue criar sua senha e acessar a plataforma.

---

## US-08 — Cadastro de aluno

**Como** administrador,
**quero** cadastrar um aluno na plataforma informando seus dados básicos,
**para que** ele possa acessar o chat das matérias em que será matriculado.

### Regras de Negócio

- Apenas o administrador pode cadastrar alunos.
- O aluno recebe automaticamente o perfil "Aluno" no cadastro.
- Ao ser cadastrado, o aluno recebe um link de convite por e-mail para criar sua própria senha antes do primeiro acesso.
- A matrícula e o e-mail informados devem ser únicos na plataforma.

### Regras de Validação

- Nome completo é obrigatório.
- Matrícula institucional é obrigatória e deve ser única na plataforma.
- E-mail institucional é obrigatório, deve ser único na plataforma e ter formato válido.
- Caso a matrícula já exista, exibir: _"Esta matrícula já está em uso por outro usuário."_
- Caso o e-mail já exista, exibir: _"Este e-mail já está em uso por outro usuário."_

### Regras de Interface

- O formulário de cadastro de aluno deve conter os campos: Nome completo, Matrícula, E-mail.
- O sistema envia automaticamente um link de convite para o e-mail do aluno ao concluir o cadastro.
- Ao concluir o cadastro, exibir confirmação e opção de cadastrar outro aluno ou voltar à listagem.
- A listagem de alunos exibe uma caixa de pesquisa (acima da tabela) e paginação navegável (abaixo da tabela), com botões "Anterior", números de página e "Próximo".

### Requisitos Não Funcionais

- O cadastro deve ser confirmado em no máximo 5 segundos após o envio do formulário.
- A listagem de alunos deve usar **paginação no servidor (server-side)**: cada página é buscada na base de dados sob demanda, evitando carregar todos os alunos de uma só vez no cliente.
- A **caixa de pesquisa** da listagem deve filtrar alunos já cadastrados por **nome, matrícula ou e-mail**, executando a consulta diretamente na base de dados (não filtra apenas no cliente).

### Pré-requisitos

- O administrador deve estar autenticado.

### Critérios de Aceitação

- [ ] Administrador consegue cadastrar um aluno preenchendo os campos obrigatórios.
- [ ] Matrícula ou e-mail duplicados são rejeitados com mensagem explicativa.
- [ ] Aluno cadastrado aparece na listagem de usuários com status ativo.
- [ ] Aluno recebe e-mail com link de convite e consegue criar sua senha e acessar a plataforma.
- [ ] A listagem de alunos exibe paginação navegável; cada página é carregada da base de dados sob demanda.
- [ ] A caixa de pesquisa filtra a listagem por nome, matrícula ou e-mail consultando a base de dados.

---

## US-09 — Edição e desativação de usuário

**Como** administrador,
**quero** poder editar os dados de um usuário ou desativá-lo na plataforma,
**para que** eu mantenha as informações atualizadas e controle quem tem acesso ativo ao sistema.

### Regras de Negócio

- O administrador pode editar o nome e o e-mail de qualquer usuário.
- A matrícula não pode ser alterada após o cadastro — ela é o identificador permanente do usuário.
- O administrador pode desativar um usuário, impedindo que ele faça login.
- A desativação não exclui o histórico do usuário (conversas, materiais enviados, etc.) — apenas bloqueia o acesso.
- Um usuário desativado pode ser reativado pelo administrador a qualquer momento.

### Regras de Validação

- O e-mail editado deve ser único na plataforma; se já pertencer a outro usuário, exibir: _"Este e-mail já está em uso por outro usuário."_
- O e-mail editado deve ter formato válido.
- Ao desativar um usuário com sessão ativa, a sessão dele deve ser encerrada imediatamente.

### Regras de Interface

- Na listagem de usuários, cada linha deve ter opções de "Editar" e "Desativar" (ou "Reativar" para usuários desativados).
- A ação de desativar deve solicitar confirmação antes de ser executada: _"Tem certeza que deseja desativar o acesso de [nome do usuário]? Ele não conseguirá mais fazer login."_
- Usuários desativados devem ser identificados visualmente na listagem (ex: cor diferente ou indicador de status).
- O formulário de edição deve exibir os dados atuais do usuário pré-preenchidos.

### Requisitos Não Funcionais

- A alteração de dados deve ser salva em no máximo 5 segundos.
- A desativação deve ter efeito imediato — o usuário perde o acesso instantaneamente.

### Pré-requisitos

- O administrador deve estar autenticado.
- O usuário a ser editado ou desativado deve existir na plataforma.

### Critérios de Aceitação

- [ ] Administrador consegue editar nome e e-mail de um usuário.
- [ ] E-mail duplicado é rejeitado com mensagem explicativa.
- [ ] Matrícula não pode ser editada — o campo deve estar bloqueado no formulário.
- [ ] Usuário desativado perde o acesso imediatamente, incluindo sessão em andamento.
- [ ] Usuário desativado pode ser reativado e volta a ter acesso normalmente.
- [ ] Administrador não consegue desativar a própria conta.