> **Documento de Requisitos**
> **Projeto Tutor**

| Versão | Data | Descrição | Autor |
|--------|-----------|---------------|-----------|
| 1.3 Sprint 3 | 10/05/2026 | Cadastro, edição e desativação de matéria US-10 e US-10b, Cadastro de turma US-11, Associação de matéria a turma US-12, Vinculação de professor a turma e matéria US-13 e Matrícula de aluno em turma US-14 | Patricia Pereira Martins |
| 1.4 Sprint 3 | 19/05/2026 | Refatoração do modelo de associação para alinhar com o diagrama: US-12 passa a vincular professor↔matéria (entidade MateriaProfessor) e US-13 oferta a dupla (Professor+Matéria) a uma turma (entidade MateriaProfessorTurma). Ajustes terminológicos em US-14. | Patricia Pereira Martins |
| 1.5 Sprint 3 | 30/05/2026 | Alinhamento do texto de confirmação de desativação de matéria (US-10b-RI1) ao protótipo do Figma | Patricia Pereira Martins |

---

# EP-03 — Gestão de Matérias e Turmas

**Descrição:** Permite ao administrador organizar a estrutura acadêmica da plataforma. Matérias e turmas são cadastradas de forma independente. O professor é primeiro vinculado às matérias que está habilitado a lecionar (MateriaProfessor, US-12); essas duplas (Professor + Matéria) são então ofertadas em turmas específicas (MateriaProfessorTurma, US-13) — a mesma dupla pode ser ofertada em várias turmas. O aluno é matriculado em uma ou várias turmas (US-14) e tem acesso automaticamente ao chat de todas as ofertas (Professor + Matéria) daquelas turmas (turma fechada — sem seleção individual de matérias pelo aluno).

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
- Não é possível desativar uma matéria que possua vínculos ativos com professores (US-12) ou ofertas ativas em turmas (US-13). O administrador deve primeiro encerrar essas ofertas e remover os vínculos.

### Regras de Validação

- O nome editado deve ser preenchido e não pode estar em branco.
- O código é exibido no formulário de edição mas está bloqueado para alteração.
- Ao tentar desativar uma matéria com vínculos professor↔matéria (US-12) ou ofertas em turmas (US-13) ativas, exibir: _"Esta matéria possui vínculos com professores ou ofertas em turmas ativas. Encerre essas ofertas e remova os vínculos antes de desativar a matéria."_

### Regras de Interface

- Na listagem de matérias, cada linha deve ter opções de "Editar" e "Desativar" (ou "Reativar" para matérias desativadas).
- A ação de desativar deve solicitar confirmação: _"Tem certeza que deseja desativar a matéria [nome]? A matéria fica inacessível para chat e gerenciamento de materiais. Todo o histórico é preservado e pode ser restaurado ao reativar."_ (conforme protótipo no Figma)
- Matérias desativadas devem ser identificadas visualmente na listagem.

### Requisitos Não Funcionais

- A desativação deve ter efeito imediato.

### Pré-requisitos

- O administrador deve estar autenticado.
- A matéria deve estar cadastrada.

### Critérios de Aceitação

- [ ] Administrador consegue editar o nome de uma matéria.
- [ ] Código da matéria não pode ser alterado — campo bloqueado no formulário.
- [ ] Administrador consegue desativar uma matéria sem vínculos com professores (US-12) nem ofertas ativas em turmas (US-13).
- [ ] Tentativa de desativar matéria com vínculos ou ofertas ativas é bloqueada com mensagem explicativa.
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
- A turma é **fechada**: ao matricular um aluno em uma turma, ele automaticamente tem acesso a todas as matérias ofertadas naquela turma (US-13) — não há escolha individual de matérias pelo aluno.

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

## US-12 — Vinculação de professor a matéria

**Como** administrador,
**quero** vincular um professor a uma matéria,
**para que** fique registrado que aquele professor está habilitado a lecionar essa disciplina e a combinação possa ser ofertada em turmas (US-13).

### Regras de Negócio

- Apenas o administrador pode criar ou remover vínculos professor-matéria.
- Cada vínculo representa "Professor X leciona Matéria Y" e corresponde à entidade **MateriaProfessor** no diagrama.
- Um professor pode estar vinculado a várias matérias.
- Uma matéria pode estar vinculada a vários professores.
- O vínculo (Professor + Matéria) é **pré-requisito** para a oferta dessa combinação em uma turma (US-13).
- Ao desvincular, ofertas ativas dessa combinação em turmas devem ter sido previamente removidas (US-13). O histórico é preservado.

### Regras de Validação

- Não é possível criar o mesmo vínculo (professor, matéria) duas vezes. Caso se tente, exibir: _"Este professor já está vinculado a esta matéria."_
- Não é possível remover o vínculo se existirem ofertas ativas em turmas (US-13). Exibir: _"Existem ofertas ativas para este vínculo. Encerre as ofertas antes de remover."_
- A remoção deve solicitar confirmação.

### Regras de Interface

- Na tela de gerenciamento de professores (ou de matérias), uma seção "Vínculos" lista os pares ativos.
- Ao adicionar, o administrador pesquisa o professor por nome/matrícula e a matéria por código/nome.

### Pré-requisitos

- Professor cadastrado e ativo.
- Matéria cadastrada e ativa.
- Administrador autenticado.

### Critérios de Aceitação

- [ ] Administrador consegue vincular um professor ativo a uma matéria ativa.
- [ ] Vínculo duplicado (mesmo par professor+matéria) é rejeitado com mensagem explicativa.
- [ ] Um professor pode estar vinculado a várias matérias.
- [ ] Uma matéria pode estar vinculada a vários professores.
- [ ] O vínculo fica disponível como opção ao ofertar em turma (US-13).
- [ ] Tentativa de remover vínculo com ofertas ativas é bloqueada com mensagem explicativa.

---

## US-13 — Oferta de matéria-professor a turma

**Como** administrador,
**quero** ofertar uma dupla (Professor + Matéria) em uma turma específica,
**para que** os alunos matriculados nessa turma tenham acesso ao chat dessa disciplina sob responsabilidade daquele professor, e o professor possa gerenciar os materiais e receber as perguntas escalonadas dos alunos.

### Regras de Negócio

- Apenas o administrador pode criar ou remover ofertas.
- Cada oferta representa "Professor X leciona Matéria Y na Turma Z" e corresponde à entidade **MateriaProfessorTurma** no diagrama.
- O vínculo (Professor + Matéria) precisa existir previamente (US-12) — a oferta apenas seleciona um vínculo já criado e o associa a uma turma.
- A mesma dupla (Professor + Matéria) pode ser ofertada em várias turmas.
- Uma turma pode receber várias ofertas distintas (com matérias e/ou professores diferentes).
- Mais de uma oferta na mesma turma pode envolver a mesma matéria com professores diferentes.
- Ao criar a oferta, todos os alunos matriculados na turma passam automaticamente a ter acesso ao chat dessa matéria com aquele professor.
- Ao remover a oferta, os alunos perdem o acesso ao chat daquela matéria naquela turma. O histórico de conversas e os materiais enviados pelo professor permanecem preservados.

### Regras de Validação

- Não é possível ofertar a mesma dupla (Professor + Matéria) duas vezes na mesma turma. Caso se tente, exibir: _"Esta dupla já está ofertada nesta turma."_
- A remoção da oferta deve solicitar confirmação.

### Regras de Interface

- Na tela de gerenciamento de uma turma, uma seção "Ofertas" lista as duplas (Professor + Matéria) ativas, com opção de adicionar ou remover.
- Ao adicionar, o administrador escolhe entre os vínculos MateriaProfessor já existentes (US-12), com filtro por professor ou por matéria.
- A remoção deve solicitar confirmação.

### Pré-requisitos

- Turma cadastrada e ativa.
- Vínculo (Professor + Matéria) existente (US-12).
- Administrador autenticado.

### Critérios de Aceitação

- [ ] Administrador consegue ofertar uma dupla (Professor + Matéria) em uma turma ativa.
- [ ] Oferta duplicada na mesma turma é rejeitada com mensagem explicativa.
- [ ] Alunos matriculados na turma passam a visualizar a matéria ofertada no seu painel.
- [ ] A mesma dupla pode ser ofertada em várias turmas distintas.
- [ ] Uma turma pode receber várias ofertas distintas.
- [ ] Remoção da oferta retira o acesso dos alunos àquela matéria naquela turma e preserva histórico e materiais.

---

## US-14 — Matrícula de aluno em turma

**Como** administrador,
**quero** matricular alunos em turmas,
**para que** eles tenham acesso ao chat de todas as matérias ofertadas naquela turma (US-13) automaticamente.

### Regras de Negócio

- Apenas o administrador pode matricular ou desmatricular alunos de turmas.
- Ao ser matriculado em uma turma, o aluno automaticamente tem acesso ao chat de **todas as matérias ofertadas** naquela turma (US-13) — não há seleção individual de matérias.
- Um aluno pode estar matriculado em mais de uma turma simultaneamente — terá acesso às ofertas de cada turma.
- Ao ser desmatriculado, o aluno perde o acesso ao chat de todas as matérias ofertadas naquela turma. O histórico de conversas é preservado.
- Somente alunos com cadastro ativo podem ser matriculados.

### Regras de Validação

- Não é possível matricular o mesmo aluno na mesma turma mais de uma vez. Caso se tente, exibir: _"Este aluno já está matriculado nesta turma."_
- A desmatrícula deve solicitar confirmação antes de ser executada.

### Regras de Interface

- Na tela de gerenciamento de uma turma, deve haver uma seção "Alunos" com a lista dos matriculados e opção de adicionar ou remover.
- Ao adicionar, o administrador pesquisa o aluno por nome ou matrícula.
- A remoção deve exibir confirmação com aviso: _"O aluno perderá o acesso ao chat de todas as matérias ofertadas nesta turma."_

### Pré-requisitos

- A turma deve estar cadastrada e ativa.
- O aluno deve estar cadastrado e ativo.
- O administrador deve estar autenticado.

### Critérios de Aceitação

- [ ] Administrador consegue matricular um aluno ativo em uma turma.
- [ ] Aluno matriculado passa a visualizar todas as matérias ofertadas naquela turma (US-13) no seu painel.
- [ ] Matrícula duplicada é rejeitada com mensagem explicativa.
- [ ] Aluno desmatriculado perde o acesso ao chat de todas as matérias ofertadas naquela turma.
- [ ] Histórico de conversas do aluno é preservado após desmatrícula.

