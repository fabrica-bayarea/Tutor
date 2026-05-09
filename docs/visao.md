> **Documento de Requisitos**
> **Projeto Tutor**
> **Responsável:** Patricia Pereira Martins – Time de Requisitos e Testes
> **Data:** Abril/2026
> **Versão:** 1.1 (Consolidada)

---

# Tutor — Especificação do Chat

**Versão:** 1.0  
**Data:** Abril de 2026  
**Status:** Rascunho  
**Audiência:** Produto, Engenharia, UX, Negócio

---

## Sumário

1. [Introdução](#1-introdução)
2. [Visão do Produto](#2-visão-do-produto)
3. [Escopo](#3-escopo)
4. [Personas](#4-personas)
5. [Fluxos Principais](#5-fluxos-principais)
6. [Regras de Negócio](#6-regras-de-negócio)
7. [Requisitos Funcionais](#7-requisitos-funcionais)
8. [Requisitos Não Funcionais](#8-requisitos-não-funcionais)
9. [Regras de Interface](#9-regras-de-interface)
10. [Requisitos Condicionantes](#10-requisitos-condicionantes)
11. [Considerações de Arquitetura](#11-considerações-de-arquitetura)
12. [Critérios de Aceite](#12-critérios-de-aceite)

---

## 1. Introdução

Este documento descreve a especificação funcional do sistema **Tutor**, cobrindo todos os módulos da plataforma: autenticação, gestão de usuários, matérias e turmas, materiais didáticos, ingestão de conteúdo, chat educacional com IA, escalonamento de dúvidas ao professor e dashboard analítico.

O objetivo desta especificação é orientar as equipes de produto, engenharia e UX na construção da plataforma, garantindo que todos os módulos sejam entregues com qualidade e coerência entre si.

---

## 2. Visão do Produto

### 2.1 O que é o Tutor

O **Tutor** é uma plataforma educacional baseada em Inteligência Artificial que conecta alunos ao conteúdo disponibilizado por seus professores por meio de um chat inteligente.

A IA atua como um **tutor acadêmico confiável**, respondendo perguntas dos alunos com base exclusivamente nos materiais de estudo fornecidos pelos professores das disciplinas.

### 2.2 Problema que Resolve

| Problema | Impacto |
|---|---|
| Alunos têm dúvidas fora do horário de aula | Estudos interrompidos, desmotivação |
| Professores são sobrecarregados com dúvidas repetitivas | Menos tempo para atividades de maior valor |
| Acesso desigual a tutoria de qualidade | Alunos de diferentes contextos socioeconômicos sem suporte |
| IAs genéricas "alucinam" e geram respostas incorretas | Baixa confiança no aprendizado mediado por IA |

### 2.3 Proposta de Valor

- **Para o aluno:** Tutoria disponível 24/7, baseada no conteúdo exato da sua disciplina, sem alucinação.
- **Para o professor:** Redução de dúvidas repetitivas, com escalonamento apenas das dúvidas genuinamente complexas.
- **Para a instituição:** Melhora de indicadores de aprendizado, retenção e satisfação dos alunos com escalabilidade.

---

## 3. Escopo

### 3.1 O que está no Escopo

| # | Funcionalidade |
|---|---|
| 1 | Cadastro de administradores, professores e alunos |
| 2 | Cadastro de matérias e turmas |
| 3 | Vinculação de professores e alunos a matérias |
| 4 | Upload de materiais didáticos pelo professor |
| 5 | Ingestão e indexação dos materiais na base de conhecimento |
| 6 | Chat entre aluno e IA, por matéria |
| 7 | Respostas da IA restritas ao conteúdo da disciplina |
| 8 | Escalonamento de perguntas não respondidas ao professor |
| 9 | Seleção e ativação do modelo de IA (Ollama) pelo administrador |
| 10 | Autenticação por matrícula/senha e via OAuth Google, com controle de acesso por perfil |
| 11 | Consulta de histórico de dúvidas escalonadas pelo professor e pelo aluno |
| 12 | Dashboard analítico do professor com KPIs de engajamento, dúvidas frequentes, efetividade dos materiais, lacunas de conteúdo e padrões de uso da IA |

---

## 4. Personas

### 4.1 Administrador

**Descrição:** Responsável pela gestão operacional da plataforma. Normalmente um gestor de TI ou coordenador acadêmico da instituição.

**Objetivos:**
- Configurar o ambiente da instituição
- Cadastrar e gerenciar usuários
- Selecionar e ativar o modelo de IA (Ollama) utilizado pela plataforma
- Garantir que a plataforma funcione corretamente

**Necessidades:**
- Painel administrativo simples e eficiente
- Visibilidade do status do sistema

---

### 4.2 Professor

**Descrição:** Docente responsável por fornecer o conteúdo que a IA utilizará como base de conhecimento.

**Objetivos:**
- Fazer upload de materiais de suas disciplinas
- Receber e responder perguntas que a IA não conseguiu responder
- Gerenciar o conteúdo disponível para a IA
- Acompanhar indicadores de aprendizado e engajamento das suas turmas

**Necessidades:**
- Interface simples para upload de arquivos variados
- Visibilidade sobre o conteúdo indexado
- Notificações de perguntas escalonadas pelos alunos
- Painel analítico para identificar dúvidas frequentes, lacunas de conteúdo e padrões de uso da IA pelos alunos

---

### 4.3 Aluno

**Descrição:** Principal usuário da plataforma. Utiliza o chat para sanar dúvidas sobre as matérias em que está matriculado.

**Objetivos:**
- Fazer perguntas sobre o conteúdo das disciplinas
- Receber respostas confiáveis e contextualizadas
- Estudar de forma autônoma usando a IA como suporte

**Necessidades:**
- Chat intuitivo e responsivo
- Respostas claras, com referência ao material da disciplina
- Feedback quando a pergunta é encaminhada ao professor

---

## 5. Fluxos Principais

### 5.1 Fluxo de Cadastro

```
[Administrador]
  └─ Acessa painel administrativo
  └─ Cadastra professores (nome, matrícula, e-mail) → sistema envia link de convite por e-mail
  └─ Cadastra alunos (nome, matrícula, e-mail) → sistema envia link de convite por e-mail
  └─ Cadastra matérias
  └─ Cadastra turmas (entidade independente: código, semestre, turno)
  └─ Associa matérias à turma (TURMA_MATERIA)
  └─ Vincula professor à combinação turma+matéria (PROFESSOR_TURMA_MATERIA)
  └─ Matricula alunos em turma (ALUNO_TURMA) — aluno acessa automaticamente todas as matérias da turma
  └─ Seleciona e ativa o modelo de IA via Ollama

[Professor / Aluno — primeiro acesso]
  └─ Recebe link de convite por e-mail
  └─ Acessa o link e define sua própria senha
  └─ Token do link expira apenas após o primeiro uso
```

**Dados mínimos para cadastro de usuário:**
- Nome completo
- Matrícula institucional
- E-mail institucional
- Perfil (admin / professor / aluno)
- Acesso concedido via link de convite enviado por e-mail (sem senha temporária)

---

### 5.2 Fluxo de Upload de Material

```
[Professor]
  └─ Acessa área da matéria
  └─ Seleciona "Adicionar material"
  └─ Faz upload do arquivo (PDF, vídeo, áudio, slide, doc, link)
  └─ Sistema valida formato e tamanho
  └─ Sistema enfileira material para ingestão
  └─ Pipeline de ingestão processa o material:
      └─ Extração de conteúdo (OCR, transcrição, parsing)
      └─ Chunking e embeddings
      └─ Indexação na base de conhecimento da matéria
  └─ Sistema notifica professor sobre status da ingestão
  └─ Material fica disponível para consulta da IA
```

**Formatos suportados:**

Documentos:
- PDF
- DOCX
- PPTX
- XLSX
- CSV
- HTML / XHTML
- MD (Markdown)

Vídeo (transcrição via Whisper):
- MP4, MOV, MKV, AVI

Áudio (transcrição via Whisper):
- MP3, WAV, M4A, FLAC, OGG

Web:
- Links externos (scraping via Selenium)

---

### 5.3 Fluxo do Chat do Aluno

```
[Aluno]
  └─ Realiza login
  └─ Seleciona a matéria
  └─ Abre o chat da matéria
  └─ Digita a pergunta
  └─ Sistema envia pergunta + contexto para pipeline de RAG
      └─ Recupera chunks relevantes da base de conhecimento da matéria
      └─ Monta prompt com contexto recuperado
      └─ Envia para o modelo de IA ativo via Ollama
      └─ Modelo gera resposta baseada no contexto
  └─ Resposta é exibida ao aluno
  └─ Aluno pode fazer perguntas de acompanhamento na mesma sessão
      └─ Janela de contexto enviada à IA: últimas 10 trocas da sessão
      └─ Botão de envio permanece desabilitado enquanto a IA processa a resposta
```

---

### 5.4 Fluxo de Fallback para Professor

```
[Sistema — quando IA não encontra resposta confiável]
  └─ Detecta que confiança da resposta é baixa (abaixo do threshold)
  └─ Informa ao aluno que a pergunta será encaminhada ao professor
  └─ Registra a pergunta com contexto na fila de perguntas do professor
  └─ Notifica o professor (e-mail ou notificação in-app)
  
[Professor]
  └─ Acessa painel de perguntas pendentes
  └─ Visualiza pergunta e contexto do aluno
  └─ Responde diretamente pelo sistema
  └─ Aluno recebe notificação da resposta
```

---

## 6. Regras de Negócio

### RN-01 — Restrição de conhecimento por matéria

A IA **somente pode responder** com base nos materiais indexados para a matéria em questão. Não é permitido que a IA utilize conhecimento externo ou de outras matérias para responder ao aluno.

### RN-02 — Seleção do modelo de IA via Ollama

O administrador seleciona o modelo de IA a ser utilizado a partir da biblioteca do Ollama. O modelo ativo é global e aplica-se a todas as matérias da plataforma. Não há mecanismo de fallback entre modelos — se o Ollama estiver indisponível, o sistema retorna erro ao aluno.

### RN-03 — Escalonamento por baixa confiança

Quando o sistema detectar que não há contexto suficiente na base de conhecimento para responder à pergunta com confiança adequada, a pergunta deve ser **automaticamente encaminhada ao professor** da disciplina. O aluno deve ser informado sobre o encaminhamento.

### RN-04 — Professor é dono do conteúdo da matéria

Apenas o professor vinculado a uma turma+matéria pode adicionar ou desativar materiais daquela combinação. A desativação remove o material da base de conhecimento da IA imediatamente, mas mantém o arquivo armazenado para fins de histórico e auditoria. Materiais desativados não podem ser reativados — devem ser reenviados como novos.

### RN-05 — Aluno restrito às suas matérias

O aluno só pode acessar o chat das matérias em que está matriculado.

### RN-06 — Histórico de chat por sessão

O histórico completo da sessão de conversa é mantido e exibido ao aluno enquanto o chat estiver aberto. A janela de contexto enviada à LLM é limitada às **últimas 10 trocas** da sessão (cada troca = 1 pergunta + 1 resposta). Trocas mais antigas não influenciam a resposta da IA, mas permanecem visíveis ao aluno na tela.

### RN-07 — Autenticação obrigatória

Todas as funcionalidades do sistema exigem autenticação prévia. Não há acesso público a nenhuma função do produto. O usuário pode autenticar via matrícula ou e-mail com senha, ou via OAuth Google, desde que sua conta Google esteja vinculada a um cadastro ativo na plataforma.

### RN-08 — Unicidade de matrícula e e-mail

Cada usuário do sistema possui matrícula e e-mail institucionais, ambos únicos na plataforma. O login pode ser realizado com qualquer um dos dois identificadores.

### RN-09 — Rastreabilidade das respostas

Toda resposta gerada pela IA deve ser rastreável ao(s) trecho(s) de material que a embasaram, para fins de auditoria e confiança. Essa rastreabilidade é também a base dos indicadores analíticos de efetividade de materiais (EP-08).

### RN-11 — Baixa confiança: critérios de escalonamento

A resposta da IA é considerada de baixa confiança — e a pergunta é automaticamente encaminhada ao professor — quando ocorrer qualquer uma das situações: (1) nenhum fragmento relevante encontrado nos materiais; (2) fragmentos encontrados, mas insuficientes para uma resposta fundamentada; (3) pergunta claramente fora do escopo da matéria; (4) pergunta ambígua sem contexto suficiente para interpretação segura. Em nenhum desses casos a IA deve responder com conhecimento externo ou inventado.

---

## 7. Requisitos Funcionais

### Módulo: Autenticação e Controle de Acesso

| ID | Requisito | Prioridade |
|---|---|---|
| RF-01 | O sistema deve permitir login via matrícula ou e-mail, combinado com senha | Alta |
| RF-01a | O sistema deve permitir login via OAuth Google | Alta |
| RF-01b | O acesso via OAuth Google deve ser vinculado a um usuário previamente cadastrado na plataforma | Alta |
| RF-02 | O sistema deve forçar redefinição de senha no primeiro acesso (somente para login por matrícula/senha) | Alta |
| RF-03 | O sistema deve controlar acesso por perfil (admin, professor, aluno) | Alta |
| RF-04 | O sistema deve suportar logout e expiração de sessão | Alta |
| RF-05 | O sistema deve permitir recuperação de senha via matrícula ou e-mail | Média |

### Módulo: Gestão de Usuários

| ID | Requisito | Prioridade |
|---|---|---|
| RF-06 | O administrador deve poder cadastrar professores via link de convite | Alta |
| RF-06b | O administrador deve poder cadastrar administradores adicionais via link de convite | Alta |
| RF-07 | O administrador deve poder cadastrar alunos via link de convite | Alta |
| RF-08 | O administrador deve poder editar e desativar usuários (exceto o administrador principal cadastrado via seed) | Alta |

### Módulo: Gestão de Matérias e Turmas

| ID | Requisito | Prioridade |
|---|---|---|
| RF-10 | O administrador deve poder cadastrar e editar matérias | Alta |
| RF-10b | O administrador deve poder cadastrar e editar turmas (entidade independente de matéria) | Alta |
| RF-11 | O administrador deve poder associar matérias a turmas e vincular professores a combinações turma+matéria | Alta |
| RF-12 | O administrador deve poder matricular alunos em turmas | Alta |
| RF-13 | O administrador deve poder selecionar o modelo de IA ativo a partir de uma lista obtida dinamicamente da biblioteca do Ollama | Alta |
| RF-13a | O sistema deve verificar quais modelos estão instalados localmente via API do Ollama e indicar visualmente o estado de cada modelo | Alta |
| RF-13b | O sistema deve realizar o download (pull) de modelos não instalados via API do Ollama antes de ativá-los, exibindo o progresso em tempo real | Alta |

### Módulo: Gestão de Materiais

| ID | Requisito | Prioridade |
|---|---|---|
| RF-14 | O professor deve poder fazer upload de materiais didáticos | Alta |
| RF-15 | O sistema deve aceitar documentos (PDF, DOCX, PPTX, XLSX, CSV, HTML, XHTML, MD), vídeos (MP4, MOV, MKV, AVI), áudios (MP3, WAV, M4A, FLAC, OGG) e links externos | Alta |
| RF-16 | O sistema deve validar formato e tamanho máximo do arquivo no upload | Alta |
| RF-17 | O sistema deve exibir o status de processamento do material | Média |
| RF-18 | O professor deve poder desativar materiais da base de conhecimento (arquivo mantido para auditoria) | Média |
| RF-19 | O professor deve poder visualizar a lista de materiais indexados | Média |

### Módulo: Pipeline de Ingestão

| ID | Requisito | Prioridade |
|---|---|---|
| RF-20 | O sistema deve extrair texto de PDFs e documentos via parsing | Alta |
| RF-21 | O sistema deve transcrever áudio e vídeo para texto (STT) | Alta |
| RF-23 | O sistema deve realizar scraping básico de links externos | Média |
| RF-24 | O sistema deve segmentar (chunk) o conteúdo extraído | Alta |
| RF-25 | O sistema deve gerar embeddings dos chunks | Alta |
| RF-26 | O sistema deve indexar os embeddings em base vetorial por matéria | Alta |

### Módulo: Chat Educacional

| ID | Requisito | Prioridade |
|---|---|---|
| RF-27 | O aluno deve poder selecionar uma matéria e iniciar chat | Alta |
| RF-28 | O sistema deve consultar a base vetorial da matéria ao receber pergunta | Alta |
| RF-29 | O sistema deve montar prompt com contexto recuperado e histórico | Alta |
| RF-30 | O sistema deve enviar o prompt para o modelo de IA ativo via Ollama | Alta |
| RF-31 | A resposta da IA deve ser exibida ao aluno no chat | Alta |
| RF-32 | O chat deve manter histórico da sessão atual | Alta |
| RF-33 | O sistema deve identificar respostas de baixa confiança | Alta |

### Módulo: Escalonamento para Professor

| ID | Requisito | Prioridade |
|---|---|---|
| RF-34 | O sistema deve encaminhar perguntas de baixa confiança ao professor automaticamente | Alta |
| RF-35 | O aluno deve ser informado quando sua pergunta for encaminhada | Alta |
| RF-36 | O professor deve receber notificação de perguntas pendentes | Média |
| RF-37 | O professor deve poder responder às perguntas pelo sistema ou marcá-las como "Não consegui responder" | Alta |
| RF-38 | O aluno deve ser notificado quando o professor responder | Média |
| RF-39 | O professor deve ter acesso ao histórico completo de perguntas escalonadas (em aberto e respondidas) com filtros e busca por texto | Média |
| RF-40 | O aluno deve poder consultar suas próprias perguntas encaminhadas e verificar se foram respondidas | Média |

### Módulo: Dashboard Analítico do Professor

| ID | Requisito | Prioridade |
|---|---|---|
| RF-41 | O sistema deve exibir indicadores de engajamento por turma+matéria (alunos ativos, total de perguntas, alunos sem interação, horários de pico) | Média |
| RF-42 | O sistema deve agrupar perguntas semanticamente semelhantes e exibir as dúvidas mais frequentes com pergunta representativa e contagem de alunos | Média |
| RF-43 | O sistema deve exibir o ranking de materiais por uso (fragmentos usados em respostas) e identificar materiais nunca consultados | Média |
| RF-44 | O sistema deve exibir a taxa de escalonamento e a distribuição por tipo de lacuna de conteúdo | Média |
| RF-45 | O sistema deve categorizar as perguntas dos alunos por intenção (exercícios, resumo, conceitual, aplicação, outras) e exibir a distribuição | Média |

---

## 8. Requisitos Não Funcionais

### 8.1 Desempenho

| ID | Requisito |
|---|---|
| RNF-01 | O tempo de resposta do chat deve ser inferior a **30 segundos** em condições normais de carga |
| RNF-02 | O sistema deve suportar pelo menos **500 usuários simultâneos** |
| RNF-03 | O pipeline de ingestão deve processar um PDF de 100 páginas em no máximo **30 minutos** |
| RNF-04 | A busca vetorial deve retornar resultados em menos de **500ms** |

### 8.2 Escalabilidade

| ID | Requisito |
|---|---|
| RNF-05 | A arquitetura deve suportar escalonamento horizontal dos serviços de chat e ingestão |
| RNF-06 | A base de conhecimento deve ser particionada por matéria para isolar escala |
| RNF-07 | O sistema deve suportar a seleção e troca do modelo de IA ativo via Ollama sem reinicialização do servidor |

### 8.3 Disponibilidade e Confiabilidade

| ID | Requisito |
|---|---|
| RNF-08 | A disponibilidade mínima do sistema deve ser **99,5%** (uptime mensal) |
| RNF-09 | O sistema deve ter estratégia de retry para falhas de comunicação com LLMs |
| RNF-10 | Falhas na ingestão não devem afetar o funcionamento do chat |
| RNF-11 | O sistema deve ter backups diários da base de dados e da base vetorial |

### 8.4 Segurança

| ID | Requisito |
|---|---|
| RNF-12 | Todas as comunicações devem ser criptografadas via **TLS 1.2+** |
| RNF-13 | Senhas devem ser armazenadas com hashing seguro (**bcrypt** ou equivalente) |
| RNF-14 | Tokens de autenticação devem ter expiração configurável |
| RNF-15 | O sistema deve implementar **rate limiting** nas APIs de chat |
| RNF-16 | Uploads de arquivo devem ser verificados contra malware |
| RNF-17 | O acesso à base vetorial deve ser isolado por matéria (nenhum aluno acessa dados de outra disciplina) |

### 8.5 Privacidade de Dados

| ID | Requisito |
|---|---|
| RNF-18 | O sistema deve estar em conformidade com a **LGPD** |
| RNF-19 | Dados pessoais de alunos não devem ser enviados às APIs de LLM externas |
| RNF-20 | A instituição deve poder solicitar exclusão de dados de usuários |
| RNF-21 | Logs de acesso devem ser armazenados por prazo definido e com acesso controlado |

### 8.6 Usabilidade

| ID | Requisito |
|---|---|
| RNF-22 | A interface deve ser responsiva e funcionar em navegadores modernos (Chrome, Firefox, Edge) |
| RNF-23 | O chat deve ser acessível via dispositivos móveis (design responsivo) |
| RNF-24 | O tempo de carregamento inicial da interface deve ser inferior a **5 segundos** |

---

## 9. Regras de Interface

### 9.1 Chat do Aluno

- A tela de chat deve ser a principal interface do aluno após login
- O aluno deve selecionar a matéria antes de iniciar o chat
- A caixa de texto de pergunta deve ter limite de **1.000 caracteres**
- Respostas da IA devem exibir formatação markdown (listas, negrito, código)
- Quando a pergunta for encaminhada ao professor, exibir mensagem clara:  
  _"Não encontrei uma resposta nos materiais disponíveis. Sua dúvida foi enviada ao professor."_
- O histórico da sessão deve ser visível na lateral ou acima do campo de texto
- Indicador de "digitando…" deve ser exibido enquanto a IA processa a resposta
- O botão de envio deve permanecer **desabilitado** enquanto a IA estiver processando — o aluno não pode enviar nova pergunta até a resposta chegar

### 9.2 Upload de Conteúdo (Professor)

- Interface de drag-and-drop para upload de arquivos
- Exibir progresso de upload e status de processamento (Em fila / Processando / Concluído / Erro)
- Exibir lista de materiais indexados com nome, tipo, data e status
- Permitir remoção de material com confirmação
- Limite de tamanho de arquivo deve ser exibido claramente antes do upload

### 9.3 Dashboard do Administrador

- Visão geral de: usuários cadastrados, matérias ativas, materiais indexados
- Gerenciamento de usuários com busca e filtros (perfil, status)
- Gestão do modelo de IA em seção dedicada: lista de modelos Ollama disponíveis, com indicação visual de instalados vs. disponíveis para download, e ativação com um clique

### 9.4 Experiência Geral

- Navegação por menu lateral fixo com ícones e rótulos textuais
- Estados de carregamento devem ser exibidos para todas as operações assíncronas
- Mensagens de erro devem ser claras, em linguagem não técnica
- Sistema deve exibir confirmações para ações destrutivas (desativar material, desativar usuário)

### 9.5 Dashboard Analítico do Professor

- O painel deve ser acessível no menu principal do professor, em seção dedicada "Análise e KPIs"
- Filtros globais disponíveis em todos os painéis: matéria+turma e período (2 semanas / 1 mês / 3 meses / personalizado)
- Todos os painéis permitem exportação dos dados exibidos em CSV
- Dados de dúvidas e padrões de uso devem ser exibidos de forma **agregada** — sem identificação individual de qual aluno fez qual pergunta
- O painel de padrões de uso deve incluir aviso visível: _"A categorização é baseada em palavras-chave e tem caráter indicativo."_
- Contador de perguntas pendentes do professor deve ser exibido em destaque no menu (ícone com número)

---

*Documento gerado em Abril de 2026. Revisão recomendada a cada sprint de planejamento.*
