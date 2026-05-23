> **Documento de Requisitos**
> **Projeto Tutor**

| Versão | Data | Descrição | Autor |
|--------|-----------|---------------|-----------|
| 1.2 Sprint 2 | 19/04/2026 | Login US-01 e US-02, Criação de senha via link de convite US-03 e Encerramento de sessão US-05 | Patricia Pereira Martins |
| 1.3 Sprint 3 | 10/05/2026 | Inclusão do histórico de revisão | Patricia Pereira Martins |

---

# EP-09 — Gestão do Modelo de IA

**Descrição:** Permite ao administrador selecionar e ativar o modelo de linguagem que será utilizado pela plataforma. Os modelos disponíveis são obtidos dinamicamente da biblioteca oficial do Ollama via scraping. O sistema consulta a API local do Ollama para identificar quais modelos já estão instalados, realiza o download dos ausentes e persiste o modelo ativo em banco de dados. Todas as requisições de geração de texto utilizam o modelo ativo configurado.

**Personas:** Administrador

**Protótipo:** [Design System](https://www.figma.com/design/5MClPpSqI9R42MPCwTcDzH/Tutor----Sprint-2?node-id=258-2&p=f&t=ukWioTEjrb08WqKU-0)

**Protótipo Sprint 2 — Gestão de Modelo de IA:** [Catálogo de LLM](https://www.figma.com/design/5MClPpSqI9R42MPCwTcDzH/Tutor----Sprint-2?node-id=239-8&p=f&t=cBk9R5p5mLL2xpWV-0)


---

## US-38 — Seleção e ativação de modelo de IA via Ollama

**Como** administrador,
**quero** selecionar qual modelo de linguagem será utilizado pela plataforma a partir de uma lista atualizada da biblioteca do Ollama,
**para que** eu possa controlar qual IA processa as perguntas dos alunos e garantir que o modelo esteja disponível localmente antes de ser ativado.

### Regras de Negócio

- A lista de modelos disponíveis é obtida por scraping da página oficial da biblioteca do Ollama — sempre atualizada dinamicamente.
- O sistema consulta a API local do Ollama para identificar quais modelos já estão instalados.
- A lista exibe visualmente dois estados: **Instalado** (pronto para ativar) e **Disponível para download**.
- Ao selecionar um modelo não instalado, o sistema realiza o pull via API do Ollama antes de ativá-lo.
- Durante o download, o sistema exibe o progresso em tempo real (percentual ou barra de progresso).
- Ao clicar em **"Ativar"** de um modelo já instalado, o sistema exibe um modal de confirmação antes de efetuar a troca, evitando ativações acidentais.
- Após instalação (ou se já instalado e confirmado pelo administrador), o modelo é definido como **modelo ativo**.
- O modelo ativo é persistido em banco de dados e passa a ser utilizado em todas as requisições de geração de texto da plataforma.
- Apenas um modelo pode estar ativo por vez; a troca substitui o anterior sem reprocessar materiais já indexados.
- A configuração é global — aplica-se a todas as matérias da plataforma.

### Regras de Validação

- Se a lista de modelos não puder ser obtida (scraping falha), exibir: _"Não foi possível carregar a lista de modelos. Verifique a conexão e tente novamente."_
- Se a API local do Ollama não estiver acessível, exibir: _"Serviço Ollama não encontrado. Verifique se o Ollama está em execução."_
- Se o download falhar, exibir: _"Falha ao baixar o modelo [nome]. Verifique a conexão e tente novamente."_ O modelo anterior permanece ativo.
- Não é permitido ativar um modelo que não está instalado sem concluir o download.

### Regras de Interface

- A tela exibe a lista de modelos com: nome, tamanho estimado e estado (Instalado / Disponível para download).
- Modelos instalados possuem botão **"Ativar"**. Modelos não instalados possuem botão **"Fazer Download"**.
- O modelo atualmente ativo é destacado visualmente (badge ou indicador "Ativo").
- Ao clicar em **"Ativar"** de um modelo instalado, o sistema exibe um modal de confirmação com:
  - Título: _"Ativar o modelo [nome]?"_
  - Texto descritivo: _"O [modelo atual] deixará de atender novas mensagens e o [novo modelo] passará a ser o modelo ativo. As conversas em andamento seguem normalmente com o modelo atual."_
  - Ação primária (accent): botão _"Ativar [nome]"_
  - Ação secundária (outlined): botão _"Cancelar"_
- Durante o download, o botão é substituído por uma barra de progresso com opção de cancelar.
- Após ativação bem-sucedida, o sistema exibe confirmação: _"Modelo [nome] ativado com sucesso."_

### Requisitos Não Funcionais

- O progresso do download deve ser atualizado em tempo real (polling ou streaming via SSE).
- A troca de modelo ativo não deve interromper conversas em andamento — sessões ativas concluem com o modelo anterior.
- A lista de modelos disponíveis deve ser obtida com cache máximo de 1 hora para evitar scraping excessivo da página do Ollama.

### Pré-requisitos

- O administrador deve estar autenticado.
- O serviço Ollama deve estar em execução e acessível pelo backend.

### Critérios de Aceitação

- [ ] A lista de modelos é carregada dinamicamente da biblioteca oficial do Ollama.
- [ ] A lista indica visualmente quais modelos estão instalados e quais precisam ser baixados.
- [ ] Administrador consegue ativar um modelo já instalado após confirmar no modal de confirmação.
- [ ] Ao clicar em "Ativar" de um modelo instalado, o sistema exibe o modal com título, descrição contextual e botões "Cancelar" e "Ativar [nome]".
- [ ] Cancelar no modal mantém o modelo anterior ativo e fecha o modal sem alterações.
- [ ] Administrador consegue baixar e ativar um modelo não instalado; o progresso é exibido em tempo real.
- [ ] Falha no scraping exibe mensagem explicativa sem travar a tela.
- [ ] Falha no download mantém o modelo anterior ativo e exibe mensagem explicativa.
- [ ] O modelo ativo é salvo em banco de dados e persiste após reinicialização do servidor.
- [ ] Todas as requisições de geração de texto passam a usar o modelo ativo imediatamente após a troca.
- [ ] A troca de modelo não reprocessa materiais já indexados.
- [ ] Sessões de chat em andamento no momento da troca concluem normalmente com o modelo anterior.

## US-38.1 — Migration para adicionar coluna de status na tabela LLM

**Como** desenvolvedor,
**quero** criar uma migration que adicione uma coluna status do tipo ENUM(ativada, desativada) na tabela llm,
**para que** o sistema possa registrar e persistir o estado de ativação de cada modelo de IA.

### Schema da Tabela llm

- ColunaTipoRestriçõesmodel_idVARCHARPRIMARY KEYstatusENUM('ativada','desativada')NOT NULL, DEFAULT 'desativada'
- Arquivos Criados/Alterados
- ArquivoDescriçãomigrations/versions/add_status_column_to_llm.pyMigration que adiciona a coluna status na tabela llmapplication/models/llm.pyModel atualizado com a coluna statusapplication/services/service_llm.pyService criado com a lógica de ativação/desativaçãotests/test_llm.pyTestes do service

### Regras de Negócio

A coluna status é obrigatória (NOT NULL).
Valor padrão: desativada.
Apenas um modelo pode estar com status = 'ativada' simultaneamente — garantido em nível de aplicação no service_llm.py.
O valor da coluna é persistido no banco de dados e mantido após reinicialização do servidor.

### Critérios de Aceitação

- [v] Migration criada e aplicada com sucesso no banco de dados.
- [v] Coluna status aparece na tabela llm com valores possíveis ativada e desativada.
- [v] Valor padrão desativada aplicado corretamente em novos registros.
- [v] Testes confirmam que apenas um modelo pode estar com status = 'ativada'.
- [v] Documentação do schema atualizada.