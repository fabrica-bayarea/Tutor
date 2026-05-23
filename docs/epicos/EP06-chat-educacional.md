> **Documento de Requisitos**
> **Projeto Tutor**

| Versão | Data | Descrição | Autor |
|--------|-----------|---------------|-----------|
| 1.2 Sprint 2 | 19/04/2026 | Login US-01 e US-02, Criação de senha via link de convite US-03 e Encerramento de sessão US-05 | Patricia Pereira Martins |
| 1.3 Sprint 3 | 10/05/2026 | Inclusão do histórico de revisão | Patricia Pereira Martins |

---

# EP-06 — Chat Educacional

**Descrição:** Permite ao aluno tirar dúvidas sobre o conteúdo das suas disciplinas por meio de uma conversa com a IA, que responde com base exclusivamente nos materiais disponibilizados pelo professor.

**Personas:** Aluno


**Protótipo:** [Design System](https://www.figma.com/design/5MClPpSqI9R42MPCwTcDzH/Tutor----Sprint-2?node-id=258-2&p=f&t=ukWioTEjrb08WqKU-0)

**Protótipo Sprint 2 — Chat:** [Chat Educacional](https://www.figma.com/design/5MClPpSqI9R42MPCwTcDzH/Tutor----Sprint-2?node-id=123-2&p=f&t=ukWioTEjrb08WqKU-0)

---

## US-22 — Iniciar conversa em uma matéria

**Como** aluno,
**quero** selecionar uma das minhas matérias e abrir o chat para fazer perguntas,
**para que** eu possa estudar e tirar dúvidas sobre o conteúdo da disciplina a qualquer hora.

### Regras de Negócio

- O aluno só pode acessar o chat das matérias ofertadas nas turmas em que está matriculado (ver EP-03, US-13/US-14).
- Ao acessar o chat de uma matéria, inicia-se uma sessão de conversa.
- O aluno pode ter sessões de conversa em matérias diferentes, mas cada matéria tem seu próprio histórico.
- A IA utiliza apenas os materiais indexados da matéria selecionada para responder.

### Regras de Validação

- Caso a matéria não possua nenhum material indexado, o aluno pode abrir o chat, mas a IA informará que ainda não há conteúdo disponível: _"Ainda não há materiais disponíveis para esta matéria. Quando o professor enviar o conteúdo, você poderá fazer suas perguntas aqui."_
- Aluno sem matrícula em qualquer turma com matérias ofertadas visualiza uma tela informando: _"Você ainda não está matriculado em nenhuma turma com matérias disponíveis. Entre em contato com a coordenação."_

### Regras de Interface

- Após o login, o aluno é direcionado diretamente para a interface de chat — **não há tela intermediária de seleção de matéria**.
- A seleção de matéria é feita por um **combobox/dropdown** posicionado na barra superior da tela, pré-preenchido automaticamente com a primeira matéria da lista do aluno em ordem alfabética.
- O dropdown exibe apenas as matérias ofertadas nas turmas em que o aluno está matriculado; selecionar uma matéria altera o contexto do chat.
- Na tela de boas-vindas (quando não há conversa ativa), exibir quatro cartões informativos de sugestões de uso. Os cartões **não têm ação ao clicar** — servem apenas como orientação sobre o que o aluno pode perguntar. Os cartões são:
  - **Tirar dúvidas** — _"Explique um conceito da matéria"_
  - **Resumir material** — _"Peça um resumo de um tema do conteúdo"_
  - **Preparar para prova** — _"Crie questões de estudo sobre um tema"_
  - **Aprofundar tema** — _"Informe um tema para explorar em detalhes"_
- A barra lateral (sidebar) exibe o logotipo da plataforma, um botão "Novo Chat" e a lista de **chats recentes** do aluno. Cada item da lista exibe o título resumido da conversa e o nome da matéria correspondente.
- O campo de digitação de perguntas deve estar em destaque e pronto para uso imediatamente após o carregamento.

### Requisitos Não Funcionais

- A interface de chat deve carregar em no máximo 5 segundos após o login.
- A plataforma deve suportar pelo menos 500 alunos usando o chat simultaneamente sem degradação perceptível.

### Pré-requisitos

- O aluno deve estar autenticado.
- O aluno deve estar matriculado em ao menos uma turma com matérias ofertadas (EP-03, US-13/US-14).

### Critérios de Aceitação

- [ ] Após o login, o aluno é direcionado diretamente para a interface de chat, sem tela intermediária.
- [ ] O combobox de matéria exibe apenas as matérias ofertadas nas turmas em que o aluno está matriculado e vem pré-preenchido com a primeira da lista.
- [ ] A tela de boas-vindas exibe os quatro cartões de ação rápida.
- [ ] A lista de chats recentes na sidebar exibe título da conversa e nome da matéria.
- [ ] Chat de matérias sem material indexado exibe aviso adequado.
- [ ] Aluno sem matrícula em qualquer turma com matérias ofertadas recebe orientação.

---

## US-23 — Receber resposta baseada no material da disciplina

**Como** aluno,
**quero** digitar uma pergunta e receber uma resposta da IA baseada nos materiais da minha disciplina,
**para que** eu tenha respostas confiáveis e fundamentadas no conteúdo que meu professor disponibilizou.

### Regras de Negócio

- A IA responde **somente** com base nos materiais indexados da matéria em questão. Não é permitido que a IA invente informações ou use conhecimento externo.
- Antes de gerar a resposta, o sistema localiza os trechos dos materiais da matéria mais relevantes para a pergunta.
- A resposta é gerada a partir desses trechos, mantendo fidelidade ao conteúdo do professor.
- Se nenhum trecho relevante for encontrado, a IA não deve inventar uma resposta.
- A IA deve responder no mesmo idioma da pergunta do aluno.
- Caso o provedor de IA principal esteja indisponível, a plataforma tenta automaticamente os provedores de fallback configurados, de forma transparente ao aluno.

### Regras de Validação

- A pergunta não pode estar em branco; o botão de enviar deve estar desabilitado com campo vazio.
- O campo de pergunta tem limite de 1.000 caracteres; ao atingir o limite, o aluno deve ser informado.
- Caso todos os provedores de IA estejam indisponíveis, exibir: _"O serviço de respostas está temporariamente indisponível. Tente novamente em alguns minutos."_

### Regras de Interface

- O campo de digitação deve ter um contador de caracteres visível (ex: "450/1000").
- O botão de enviar pergunta deve estar desabilitado enquanto o campo estiver vazio.
- O botão de enviar deve permanecer desabilitado enquanto a IA estiver processando a resposta — o aluno não pode enviar uma nova pergunta até a resposta atual ser exibida.
- Enquanto a IA processa a resposta, exibir um indicador de "digitando..." ou similar para que o aluno saiba que a pergunta está sendo processada.
- A resposta da IA deve ser renderizada em **Markdown** — incluindo negrito, itálico, listas, tópicos e blocos de código — para facilitar a leitura. O texto bruto em Markdown não deve ser exibido ao aluno; apenas a versão formatada é apresentada.
- A pergunta do aluno e a resposta da IA devem aparecer na tela em formato de conversa (estilo chat).

### Requisitos Não Funcionais

- A resposta da IA deve ser exibida em no máximo 30 segundos em condições normais de uso.
- Dados pessoais do aluno (nome, matrícula, e-mail) não devem ser enviados ao serviço de IA externo.
- Toda resposta deve ser rastreável aos trechos do material que a embasaram, para fins de verificação.

### Pré-requisitos

- O aluno deve ter aberto o chat de uma matéria (US-22).
- A matéria deve ter materiais indexados disponíveis.
- Ao menos um provedor de IA deve estar configurado e operacional.

### Critérios de Aceitação

- [ ] Aluno faz uma pergunta e recebe resposta baseada nos materiais da matéria em até 30 segundos.
- [ ] A resposta não contém informações inventadas; está fundamentada no conteúdo indexado.
- [ ] Campo de pergunta vazio não permite envio.
- [ ] Limite de 1.000 caracteres é respeitado e o aluno é informado ao atingi-lo.
- [ ] Indicador de processamento é exibido enquanto a resposta não chega.
- [ ] A resposta da IA é renderizada em Markdown formatado — sem exibir o texto bruto ao aluno.
- [ ] Falha no provedor principal é tratada silenciosamente com o uso do fallback.
- [ ] Quando todos os provedores estão indisponíveis, o aluno recebe mensagem de indisponibilidade.

---

## US-24 — Continuidade da conversa na mesma sessão

**Como** aluno,
**quero** fazer perguntas de acompanhamento durante a mesma sessão de estudo e ter minhas perguntas e respostas anteriores visíveis,
**para que** eu possa aprofundar o entendimento de um tema sem perder o contexto da conversa.

### Regras de Negócio

- O histórico completo da sessão atual de conversa deve ser mantido e visível enquanto o aluno estiver com o chat aberto.
- A IA considera o contexto das perguntas e respostas anteriores da sessão ao gerar novas respostas, combinando esse histórico com os trechos de material recuperados da base de conhecimento.
- A **janela de contexto de histórico** enviada à IA é limitada às **últimas 10 trocas** da sessão (cada troca = 1 pergunta do aluno + 1 resposta da IA). Mensagens mais antigas que esse limite não são enviadas à IA, mas permanecem visíveis ao aluno na tela.
- Essa limitação garante que as respostas sejam influenciadas pelo contexto recente da conversa sem comprometer o desempenho ou ultrapassar a capacidade de processamento do serviço de IA.
- Ao fechar o chat e reabrir, a sessão anterior não é necessariamente retomada — inicia-se uma nova conversa.

### Regras de Validação

- Não aplicável para esta funcionalidade.

### Regras de Interface

- Todo o histórico da sessão deve ser visível na tela de chat (com rolagem, se necessário).
- Perguntas do aluno e respostas da IA devem ser visualmente diferenciadas (ex: balões de cores diferentes ou alinhamentos distintos).
- O campo de nova pergunta deve permanecer acessível sem a necessidade de rolar até o final da conversa.

### Requisitos Não Funcionais

- O histórico da sessão deve ser exibido sem necessidade de recarregar a página.

### Pré-requisitos

- O aluno deve ter iniciado uma sessão de chat (US-22).
- Ao menos uma mensagem deve ter sido trocada na sessão.

### Critérios de Aceitação

- [ ] Todo o histórico de perguntas e respostas da sessão atual é visível ao aluno.
- [ ] A IA considera o contexto das mensagens anteriores ao responder novas perguntas na mesma sessão.
- [ ] A IA utiliza no máximo as últimas 10 trocas da sessão como contexto de histórico — trocas mais antigas não influenciam a resposta, mas permanecem visíveis ao aluno.
- [ ] Mensagens do aluno e da IA são visualmente diferenciadas.

---

## US-25 — Identificação de pergunta sem resposta na base

**Como** plataforma,
**quero** identificar quando a IA não encontra conteúdo suficiente nos materiais da matéria para responder com confiança a uma pergunta,
**para que** o aluno tenha uma resposta confiável para estudar.

### Regras de Negócio

- Quando os materiais disponíveis não contêm informação suficiente para responder à pergunta com confiança, a IA **não deve inventar uma resposta**.
- A IA não deve revelar ao aluno detalhes técnicos sobre por que não conseguiu responder.

**Critérios que caracterizam baixa confiança:**

A resposta é considerada de baixa confiança quando ocorrer qualquer uma das seguintes situações:

1. **Nenhum trecho relevante encontrado:** a busca nos materiais da matéria não retorna nenhum fragmento com semelhança mínima à pergunta do aluno — ou seja, o conteúdo da disciplina não contém informação relacionada ao tema perguntado.
2. **Trechos encontrados, mas insuficientes:** os fragmentos recuperados abordam tangencialmente o assunto, mas não contêm informação específica o suficiente para compor uma resposta fundamentada — o sistema identifica que uma resposta gerada a partir deles seria superficial ou imprecisa.
3. **Pergunta fora do escopo da matéria:** a pergunta é claramente sobre um tema que não faz parte dos materiais da disciplina (ex: aluno pergunta sobre um assunto de outra matéria).
4. **Pergunta ambígua sem contexto suficiente:** a pergunta é vaga demais para ser respondida com segurança e o histórico da sessão não fornece contexto adicional que permita interpretá-la com clareza.

### Regras de Validação

- A resposta da IA nunca deve ser enviada ao aluno se o sistema identificar que não há embasamento suficiente no material.
- Em nenhum dos cenários de baixa confiança acima a IA deve tentar responder com base em conhecimento externo ou inventado.

### Regras de Interface

- Quando a pergunta é encaminhada ao professor, exibir ao aluno: _"Não encontrei uma resposta nos materiais disponíveis."_
- A mensagem deve aparecer no chat como parte natural da conversa.

### Requisitos Não Funcionais

- A identificação de resposta com baixa confiança deve ocorrer dentro do tempo total de resposta (máximo 30 segundos).

### Pré-requisitos

- O aluno deve ter feito uma pergunta no chat (US-23).
- O professor responsável pela matéria deve ser vinculado a ela.

### Critérios de Aceitação

- [ ] A IA não gera resposta inventada quando o conteúdo é insuficiente.

