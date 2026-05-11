> **Documento de Requisitos**
> **Projeto Tutor**

| Versão | Data | Descrição | Autor |
|--------|-----------|---------------|-----------|
| 1.3 Sprint 3 | 10/05/2026 | Cadastro, edição e desativação de matéria US-10 e US-10b, Cadastro de turma US-11, Associação de matéria a turma US-12, Vinculação de professor a turma e matéria US-13 e Matrícula de aluno em turma US-14 | Patricia Pereira Martins |

---

# EP-03 — Gestão de Matérias e Turmas

**Descrição:** Permite ao administrador organizar a estrutura acadêmica da plataforma. Matérias e turmas são cadastradas de forma independente e depois associadas. O professor é vinculado ao par turma+matéria — ou seja, leciona uma matéria específica para uma turma específica. O aluno é matriculado na turma e automaticamente tem acesso a todas as matérias daquela turma (turma fechada).

**Personas:** Administrador

**Protótipo:** [Design System](https://www.figma.com/design/5MClPpSqI9R42MPCwTcDzH/Tutor----Sprint-2?node-id=258-2&p=f&t=ukWioTEjrb08WqKU-0)

**Protótipo Sprint 3 — Cadastro de matéria:** [Cadastro de matéria](https://www.figma.com/design/zmoOcbWpUlzlRtJMoqwjPC/Tutor----Sprint-3?node-id=239-6&p=f&t=YQYt419AlJk2mdgq-0)

**Protótipo Sprint 3 — Cadastro de turma:** [Cadastro de turma](https://www.figma.com/design/zmoOcbWpUlzlRtJMoqwjPC/Tutor----Sprint-3?node-id=239-7&p=f&t=YQYt419AlJk2mdgq-0)

---

## US-10 — Cadastro de matéria

**Como** administrador,
**quero** cadastrar matérias na plataforma,
**para que** elas possam ser associadas a turmas e professores.

### Regras de Negócio

- Apenas o administrador pode cadastrar matérias.
- A matéria existe de forma independente da turma — pode ser associada a várias turmas em semestres ou períodos diferentes.
- Cada matéria possui um código único e um nome.

### Regras de Validação

- Código da matéria é obrigatório e deve ser único na plataforma. Caso já exista, exibir: _"Já existe uma matéria com este código."_
- Nome da matéria é obrigatório.

### Regras de Interface

- O formulário de cadastro deve conter: Código e Nome da matéria.
- Após o cadastro, a matéria aparece na listagem com status "Ativa".
- A listagem deve permitir busca por código ou nome.

### Requisitos Não Funcionais

- O cadastro deve ser confirmado em no máximo 5 segundos.

### Pré-requisitos

- O administrador deve estar autenticado.

### Critérios de Aceitação

- [ ] Administrador consegue cadastrar uma matéria com código e nome.
- [ ] Código duplicado é rejeitado com mensagem explicativa.
- [ ] Matéria cadastrada aparece na listagem com status ativo.

---

## US-10b — Edição e desativação de matéria

**Como** administrador,
**quero** poder editar os dados de uma matéria ou desativá-la,
**para que** eu mantenha as informações atualizadas e consiga encerrar disciplinas sem perder o histórico.

### Regras de Negócio

- É permitido editar o nome da matéria. O código não pode ser alterado após o cadastro — é o identificador permanente.
- A desativação suspende o acesso ao chat e ao gerenciamento de materiais daquela disciplina, mas **preserva todo o histórico** — conversas, materiais e vínculos existentes.
- Uma matéria desativada pode ser reativada a qualquer momento, retomando o funcionamento normal.
- Não é possível desativar uma matéria que esteja associada a turmas ativas com alunos matriculados. O administrador deve primeiro encerrar essas turmas.

### Regras de Validação

- O nome editado deve ser preenchido e não pode estar em branco.
- O código é exibido no formulário de edição mas está bloqueado para alteração.
- Ao tentar desativar uma matéria com turmas ativas, exibir: _"Esta matéria está associada a turmas ativas. Encerre essas turmas antes de desativar a matéria."_

### Regras de Interface

- Na listagem de matérias, cada linha deve ter opções de "Editar" e "Desativar" (ou "Reativar" para matérias desativadas).
- A ação de desativar deve solicitar confirmação: _"Tem certeza que deseja desativar a matéria [nome]? O acesso ao chat e aos materiais será suspenso."_
- Matérias desativadas devem ser identificadas visualmente na listagem.

### Requisitos Não Funcionais

- A desativação deve ter efeito imediato.

### Pré-requisitos

- O administrador deve estar autenticado.
- A matéria deve estar cadastrada.

### Critérios de Aceitação

- [ ] Administrador consegue editar o nome de uma matéria.
- [ ] Código da matéria não pode ser alterado — campo bloqueado no formulário.
- [ ] Administrador consegue desativar uma matéria sem turmas ativas.
- [ ] Tentativa de desativar matéria com turmas ativas é bloqueada com mensagem explicativa.
- [ ] Matéria desativada fica inacessível imediatamente para alunos e professores.
- [ ] Matéria desativada pode ser reativada e volta a funcionar normalmente.
- [ ] Histórico de conversas e materiais é preservado após desativação.

---

## US-11 — Cadastro de turma

**Como** administrador,
**quero** cadastrar turmas na plataforma,
**para que** matérias e alunos possam ser organizados em grupos de estudo fechados.

### Regras de Negócio

- Apenas o administrador pode cadastrar turmas.
- A turma existe de forma independente da matéria — as associações são feitas em seguida.
- Cada turma possui um código único, semestre e turno.
- A turma é **fechada**: ao matricular um aluno em uma turma, ele automaticamente tem acesso a todas as matérias associadas àquela turma — não há escolha individual de matérias pelo aluno.

### Regras de Validação

- Código da turma é obrigatório e deve ser único na plataforma. Caso já exista, exibir: _"Já existe uma turma com este código."_
- Semestre é obrigatório (ex: 2026.1).
- Turno é obrigatório (ex: Manhã, Tarde, Noite).

### Regras de Interface

- O formulário de cadastro deve conter: Código, Semestre e Turno.
- Após o cadastro, a turma aparece na listagem com status "Ativa".
- A listagem deve permitir busca por código e filtro por semestre e turno.

### Requisitos Não Funcionais

- O cadastro deve ser confirmado em no máximo 5 segundos.

### Pré-requisitos

- O administrador deve estar autenticado.

### Critérios de Aceitação

- [ ] Administrador consegue cadastrar uma turma com código, semestre e turno.
- [ ] Código duplicado é rejeitado com mensagem explicativa.
- [ ] Turma cadastrada aparece na listagem com status ativo.

---

## US-12 — Associação de matéria a turma

**Como** administrador,
**quero** associar matérias a uma turma,
**para que** os alunos matriculados naquela turma tenham acesso ao chat dessas disciplinas.

### Regras de Negócio

- Apenas o administrador pode associar ou remover matérias de uma turma.
- Uma turma pode ter várias matérias associadas.
- Uma mesma matéria pode estar associada a várias turmas (em semestres ou contextos diferentes).
- Ao associar uma matéria a uma turma, todos os alunos já matriculados nessa turma passam a ter acesso ao chat daquela matéria automaticamente.
- Ao remover uma matéria de uma turma, os alunos perdem o acesso ao chat daquela disciplina. O histórico de conversas é preservado.
- A associação de uma matéria à turma é o pré-requisito para vincular um professor ao par turma+matéria.

### Regras de Validação

- Não é possível associar a mesma matéria à mesma turma mais de uma vez. Caso se tente, exibir: _"Esta matéria já está associada a esta turma."_
- A remoção de uma matéria da turma deve solicitar confirmação.

### Regras de Interface

- Na tela de gerenciamento de uma turma, deve haver uma seção "Matérias" com a lista das associadas e opção de adicionar ou remover.
- Ao adicionar, o administrador pesquisa a matéria por código ou nome.

### Pré-requisitos

- A turma deve estar cadastrada e ativa.
- A matéria deve estar cadastrada e ativa.
- O administrador deve estar autenticado.

### Critérios de Aceitação

- [ ] Administrador consegue associar uma matéria ativa a uma turma ativa.
- [ ] Associação duplicada é rejeitada com mensagem explicativa.
- [ ] Alunos já matriculados na turma passam a ter acesso ao chat da matéria associada.
- [ ] Ao remover a matéria da turma, alunos perdem o acesso ao chat. Histórico é preservado.

---

## US-13 — Vinculação de professor a turma e matéria

**Como** administrador,
**quero** vincular um professor ao par turma+matéria,
**para que** fique registrado que aquele professor leciona aquela disciplina para aquela turma específica, e que ele possa gerenciar os materiais e receber perguntas escalonadas dos alunos.

### Regras de Negócio

- Apenas o administrador pode realizar esse vínculo.
- O vínculo é triplo: **professor + turma + matéria** — significa "Professor X leciona Matéria Y para a Turma Z".
- Um professor pode lecionar a mesma matéria para turmas diferentes.
- Um professor pode lecionar matérias diferentes para a mesma turma.
- Mais de um professor pode lecionar a mesma matéria para a mesma turma.
- A matéria deve estar previamente associada à turma (ver US-12) para que o vínculo com o professor seja possível.
- Ao ser desvinculado, o professor perde o acesso aos materiais e às perguntas escalonadas daquele par turma+matéria. Os materiais enviados por ele permanecem disponíveis.

### Regras de Validação

- O mesmo professor não pode ter o mesmo vínculo turma+matéria registrado mais de uma vez. Caso se tente, exibir: _"Este professor já está vinculado a esta matéria nesta turma."_

### Regras de Interface

- Na tela de gerenciamento de uma turma, dentro de cada matéria associada, deve haver uma seção "Professores" com a lista dos vinculados e opção de adicionar ou remover.
- Ao adicionar, o administrador pesquisa o professor por nome ou matrícula.
- A remoção deve solicitar confirmação.

### Pré-requisitos

- A turma deve estar cadastrada e ativa.
- A matéria deve estar associada à turma (US-12).
- O professor deve estar cadastrado e ativo.
- O administrador deve estar autenticado.

### Critérios de Aceitação

- [ ] Administrador consegue vincular um professor a um par turma+matéria.
- [ ] Vínculo duplicado é rejeitado com mensagem explicativa.
- [ ] Professor vinculado visualiza a turma e matéria no seu painel.
- [ ] Professor desvinculado perde o acesso àquele par turma+matéria.
- [ ] Materiais enviados pelo professor desvinculado permanecem disponíveis na turma+matéria.
- [ ] Mais de um professor pode ser vinculado ao mesmo par turma+matéria.

---

## US-14 — Matrícula de aluno em turma

**Como** administrador,
**quero** matricular alunos em turmas,
**para que** eles tenham acesso ao chat de todas as matérias daquela turma automaticamente.

### Regras de Negócio

- Apenas o administrador pode matricular ou desmatricular alunos de turmas.
- Ao ser matriculado em uma turma, o aluno automaticamente tem acesso ao chat de **todas as matérias** associadas àquela turma — não há seleção individual de matérias.
- Um aluno pode estar matriculado em mais de uma turma simultaneamente.
- Ao ser desmatriculado, o aluno perde o acesso ao chat de todas as matérias daquela turma. O histórico de conversas é preservado.
- Somente alunos com cadastro ativo podem ser matriculados.

### Regras de Validação

- Não é possível matricular o mesmo aluno na mesma turma mais de uma vez. Caso se tente, exibir: _"Este aluno já está matriculado nesta turma."_
- A desmatrícula deve solicitar confirmação antes de ser executada.

### Regras de Interface

- Na tela de gerenciamento de uma turma, deve haver uma seção "Alunos" com a lista dos matriculados e opção de adicionar ou remover.
- Ao adicionar, o administrador pesquisa o aluno por nome ou matrícula.
- A remoção deve exibir confirmação com aviso: _"O aluno perderá o acesso ao chat de todas as matérias desta turma."_

### Pré-requisitos

- A turma deve estar cadastrada e ativa.
- O aluno deve estar cadastrado e ativo.
- O administrador deve estar autenticado.

### Critérios de Aceitação

- [ ] Administrador consegue matricular um aluno ativo em uma turma.
- [ ] Aluno matriculado passa a visualizar todas as matérias daquela turma no seu painel.
- [ ] Matrícula duplicada é rejeitada com mensagem explicativa.
- [ ] Aluno desmatriculado perde o acesso ao chat de todas as matérias da turma.
- [ ] Histórico de conversas do aluno é preservado após desmatrícula.

