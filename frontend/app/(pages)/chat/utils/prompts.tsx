export const promptQuestion = `Você é um professor especialista em ________ [área do conhecimento, ex: física quântica].

Explique o conceito de ________ [nome do conceito] de forma clara e didática, seguindo esta estrutura:

1. Definição simples (como explicaria para um iniciante)
2. Explicação aprofundada com os principais fundamentos
3. Um exemplo prático do cotidiano ou da área de ________ [contexto de aplicação]
4. Analogia criativa para fixar o entendimento
5. Os 3 pontos mais importantes para não esquecer

Nível do público-alvo: ________ [iniciante / intermediário / avançado].
Seja objetivo, use linguagem acessível e evite jargões desnecessários.`

export const promptSummarize = `Você é um especialista em síntese de informações acadêmicas e técnicas.

Leia atentamente o conteúdo abaixo sobre ________ [tema principal do conteúdo] e produza um resumo estruturado com:

- Ideia central (1 parágrafo)
- Pontos-chave (lista de até 7 tópicos essenciais)
- Conceitos ou termos importantes mencionados
- O que o autor/material conclui ou recomenda
- O que ainda ficou em aberto ou merece aprofundamento

Formato desejado: ________ [bullet points / texto corrido / tabela]
Extensão: ________ [curto ~150 palavras / médio ~300 palavras / detalhado ~500 palavras]

Conteúdo a resumir:
________ [cole aqui o texto, capítulo ou material]`

export const promptExam = `Você é um professor avaliador com experiência em ________ [tipo de prova: vestibular / concurso / faculdade / certificação].

Crie ________ [número, ex: 10] questões sobre o tema ________ [tema ou conteúdo], distribuídas da seguinte forma:

- ____ questões de múltipla escolha (com 4 alternativas e gabarito ao final)
- ____ questões dissertativas (com resposta modelo ao final)
- ____ questões verdadeiro ou falso (com justificativa)

Nível de dificuldade: ________ [fácil / médio / difícil / misto]
Foco em: ________ [compreensão / aplicação / análise crítica]

Ao final, inclua um gabarito comentado explicando o porquê de cada resposta correta.`

export const promptDeep = `Você é um pesquisador sênior especializado em ________ [área, ex: biologia molecular / história contemporânea].

Faça uma análise aprofundada sobre ________ [tema específico], abordando:

1. Contexto histórico e evolução do tema
2. Estado atual do conhecimento (o que já sabemos com certeza)
3. Debates, controvérsias ou correntes de pensamento divergentes
4. Conexões com outros temas relacionados: ________ [temas correlatos, opcional]
5. Fronteiras do conhecimento (o que ainda não sabemos / está em pesquisa)
6. Implicações práticas ou impactos no campo de ________ [área de aplicação]
7. Referências ou autores de destaque para aprofundamento

Tom desejado: ________ [acadêmico / jornalístico / técnico]
Extensão: detalhada, sem superficialidade.`

export const mockMessages = [
  { type: "user", message: "O que é inteligência artificial?" },
  { type: "llm", message: `Ótima pergunta! **Inteligência Artificial (IA)** é um campo da computação que desenvolve sistemas capazes de realizar tarefas que normalmente exigiriam inteligência humana, como:

- Reconhecer padrões
- Tomar decisões
- Compreender linguagem natural
- Aprender com experiências passadas

Quer que eu aprofunde algum desses aspectos?` },
  { type: "user", message: "Sim! Como funciona o aprendizado de máquina?" },
  { type: "llm", message: `**Aprendizado de Máquina (Machine Learning)** é um subcampo da IA onde o sistema aprende a partir de dados, sem ser explicitamente programado para cada situação.

O processo funciona assim:

1. **Dados de entrada** — o modelo recebe exemplos (ex: milhares de fotos de gatos e cachorros)
2. **Treinamento** — ele ajusta seus parâmetros internos para minimizar erros
3. **Validação** — testamos com dados que ele nunca viu
4. **Inferência** — o modelo está pronto para fazer previsões novas

Existem três tipos principais:
- **Supervisionado** — aprende com exemplos rotulados
- **Não supervisionado** — encontra padrões sozinho
- **Por reforço** — aprende através de recompensas e punições` },
  { type: "user", message: "E o que são redes neurais?" },
  { type: "llm", message: `**Redes Neurais** são modelos inspirados no funcionamento do cérebro humano.

Imagine neurônios artificiais organizados em camadas:

- **Camada de entrada** — recebe os dados brutos
- **Camadas ocultas** — processam e extraem padrões
- **Camada de saída** — produz o resultado final

Cada conexão entre neurônios tem um **peso**, que é ajustado durante o treinamento. Quanto mais camadas ocultas, mais "profunda" é a rede — daí o termo **Deep Learning**.

Uma analogia útil: é como um filtro de café em várias etapas, onde cada camada refina mais a informação até chegar ao resultado final.` },
  { type: "user", message: "Quais são as aplicações práticas disso tudo?" },
  { type: "llm", message: `As aplicações são vastas e já fazem parte do dia a dia! Alguns exemplos:

**Linguagem e texto**
- Assistentes virtuais (como eu!)
- Tradução automática
- Correção gramatical inteligente

**Visão computacional**
- Reconhecimento facial
- Diagnóstico médico por imagem
- Carros autônomos

**Recomendação**
- Netflix sugerindo séries
- Spotify montando playlists
- E-commerce mostrando produtos relevantes

**Finanças**
- Detecção de fraudes em tempo real
- Análise de risco de crédito

A tendência é que essa lista cresça rapidamente nos próximos anos. Há alguma área específica que te interessa mais?` },
  { type: "user", message: "Me fala mais sobre carros autônomos" },
  { type: "llm", message: `**Carros autônomos** são um dos casos mais complexos de IA aplicada, pois combinam múltiplas tecnologias simultaneamente.

**Como eles enxergam o mundo:**
- **Câmeras** — detectam faixas, sinais e pedestres
- **LiDAR** — cria um mapa 3D do ambiente com laser
- **Radar** — mede velocidade de objetos ao redor

**Como tomam decisões:**
O sistema processa tudo em tempo real e decide: acelerar, frear, virar. Isso envolve redes neurais treinadas em **milhões de horas** de direção humana.

**Níveis de autonomia (SAE):**
| Nível | Descrição |
|-------|-----------|
| 0 | Sem automação |
| 1 | Assistência (ex: controle de cruzeiro) |
| 2 | Parcial (Tesla Autopilot) |
| 3 | Condicional (humano em standby) |
| 4 | Alta autonomia (contextos limitados) |
| 5 | Totalmente autônomo |

Hoje a maioria dos carros comerciais está entre os níveis 2 e 3.` },
];