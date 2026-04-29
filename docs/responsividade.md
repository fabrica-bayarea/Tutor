# Responsividade — Projeto Tutor

> **Documento de Requisitos**
> **Projeto Tutor**
> **Responsável:** Patricia Pereira Martins – Time de Requisitos e Testes
> **Versão:** 1.0
> **Status:** Rascunho

---

## 1. Visão geral

A plataforma Tutor é acessada por administradores, professores e alunos em **dispositivos variados**: alunos majoritariamente no celular, professores em laptops e tablets, administradores em laptops/desktops.

Este documento define os **breakpoints de tela**, as **decisões de layout** por componente e os **critérios de aceitação** que toda tela do produto deve cumprir.

---

## 2. Breakpoints

| Nome | Faixa de largura | Frame de referência (Figma) | Dispositivo de referência | Tailwind |
|---|---|---|---|---|
| **Mobile** | < 768 px | **360 × 800** | Samsung Galaxy S22 | abaixo de `md` |
| **Tablet** | 768 – 1023 px | **820 × 1180** | iPad Air retrato | `md` (≥768) |
| **Desktop** | ≥ 1024 px | **1440 × 900** | laptop/desktop | `lg` (≥1024) |

> **Ponto crítico:** `lg` (1024 px). Acima desse valor, a sidebar é persistente; abaixo, vira drawer.

---

## 3. Decisões de layout por componente

### 3.1 Sidebar de navegação

| | Mobile | Tablet | Desktop |
|---|---|---|---|
| Estado padrão | escondida (drawer) | escondida (drawer) | persistente, 280 px |
| Como abrir | botão hambúrguer no top bar | botão hambúrguer no top bar | sempre visível |
| Largura quando aberta | 80% da viewport (overlay) | 320 px (drawer lateral) | n/a |
| Fundo da página atrás do drawer | escurecido (overlay 50%) | escurecido (overlay 30%) | n/a |
| Como fechar | tap fora do drawer ou no botão "X" | idem | n/a |

**Identidade visual da sidebar (logo "Tutor", ícones do menu, item ativo, contadores) é idêntica em todos os breakpoints** — só muda o comportamento.

### 3.2 Top Bar / Cabeçalho

| Elemento | Mobile | Tablet | Desktop |
|---|---|---|---|
| Hambúrguer | sim, à esquerda | sim, à esquerda | não |
| Logo/breadcrumb | breadcrumb colapsado: só o último segmento + seta voltar | breadcrumb completo (chevrons) | breadcrumb completo |
| Combobox de matéria (Chat) | ícone livro + nome encurtado (≤ 14 chars) | nome completo | nome completo |
| Nome do usuário | oculto | oculto | visível |
| Sino de notificações | ícone (sem badge "5" expandido — só o ponto vermelho) | ícone com badge | ícone com badge |
| Avatar | sim | sim | sim |

### 3.3 Cards de boas-vindas (Chat — tela inicial)

| | Mobile | Tablet | Desktop |
|---|---|---|---|
| Grid | 1 coluna × 4 linhas | 2 × 2 | 2 × 2 |
| Largura do cartão | 100% – 32 px (margem) | ~340 px | ~280 px |
| Altura | mais comprimido (90 px) | 110 px | 110 px |
| Texto secundário | ocultar em telas muito estreitas (< 360 px) — manter só o título | manter | manter |

### 3.4 Bolhas de mensagem (Chat)

| | Mobile | Tablet | Desktop |
|---|---|---|---|
| Largura máxima | 90% da viewport | 80% | 75% (640 px) |
| Avatar IA | oculto (poupa espaço) | visível | visível |
| Padding interno | 12 px | 14 px | 16 px |
| Fonte | 14 px | 14 px | 14 px |

### 3.5 Input bar (Chat)

| | Mobile | Tablet | Desktop |
|---|---|---|---|
| Largura | 100% – 16 px de margem lateral | 100% – 24 px | 1112 px (centralizado) |
| Altura | 56 px | 64 px | 64 px |
| Contador de caracteres | "120/1k" abreviado | "120/1000" completo | idem |
| Botão de enviar | sempre dentro do campo (à direita) | idem | idem |

### 3.6 Tabelas (CRUD Aluno, Provedores LLM)

| | Mobile | Tablet | Desktop |
|---|---|---|---|
| Apresentação | **cards verticais** (cada linha vira um card com label + valor empilhados) | tabela com **scroll horizontal** + 1ª coluna sticky (Nome) | tabela completa |
| Ações por linha | botão "..." que abre menu com ações | ícones visíveis | ícones visíveis |
| Header | oculto (cada card já tem labels) | mantido, com indicador visual de scroll | mantido |
| Paginação | "Carregar mais" no fim | paginação numérica | paginação numérica |

### 3.7 Modais (confirmação, danger, info)

- Largura: `min(480 px, 100% - 32 px)` em qualquer breakpoint.
- Altura: auto, com scroll interno se passar de `100vh - 64 px`.
- Botões ficam empilhados verticalmente em **mobile** quando há 2 ou mais (Cancelar embaixo, ação primária em cima ocupando 100%).
- Em tablet/desktop: botões lado a lado, alinhados à direita.

### 3.8 Formulários

| | Mobile | Tablet | Desktop |
|---|---|---|---|
| Campos | 1 coluna sempre | 1 ou 2 colunas conforme contexto | 1 ou 2 colunas |
| Largura do campo | 100% | 100% ou 50% | até 600 px |
| Altura do input | 48 px (alvo de toque) | 44 px | 40 px |
| Mensagem de erro | abaixo do campo, em vermelho | idem | idem |
| Botões de ação | empilhados, primário no topo, full width | lado a lado | lado a lado, à direita |

---

## 4. Critérios de aceitação de responsividade

Toda nova tela ou ajuste de layout deve cumprir:

- [ ] **Sem scroll horizontal** em nenhum breakpoint (exceto onde for explicitamente desejado, como tabela em tablet).
- [ ] **Alvos de toque ≥ 44 × 44 px** em mobile e tablet (botões, ícones clicáveis, links).
- [ ] **Tipografia legível**: corpo do texto ≥ 14 px em mobile.
- [ ] **Sidebar acessível** abaixo de 1024 px **somente** via botão hambúrguer (nunca empurrando o conteúdo).
- [ ] **Modais e drawers** fecham por: clique fora, tecla `Esc` (desktop) ou botão "X".
- [ ] **Formulários**: campos com 100% de largura em mobile; mensagens de erro abaixo do campo.
- [ ] **Tabelas**: viram cards em mobile (não scroll horizontal forçado).
- [ ] **Imagens e ícones**: não pixelizam (usar SVG sempre que possível).
- [ ] **Estado de carregamento e vazio**: presente e adaptado em cada breakpoint.

---

## 5. Como o Figma representa cada breakpoint

Para cada tela "ativa" do produto, o Figma apresenta **3 frames lado a lado**:

```
[ Mobile 360×800 ]   [ Tablet 820×1180 ]   [ Desktop 1440×900 ]
```

Os frames intermediários (drawer aberto, tabela com scroll, etc.) são representados como **estados extras** abaixo da tela principal correspondente.

---

## 6. Convenção para o time de frontend

A implementação no Next.js + Tailwind 3.4 deve usar:

- Classes utilitárias `md:` e `lg:` — **mobile-first**.
- Componente `Sidebar` com prop `mode: "drawer" | "persistent"` decidida via `useMediaQuery` ou container query.
- Componente `Table` com modo automático: detecta breakpoint e renderiza cards em mobile.
- Hook `useBreakpoint()` centralizado para evitar duplicação de lógica.

> ⚠️ A implementação no código não está coberta neste plano e será objeto de um plano separado.

---

## 7. Referências cruzadas

- Épico [EP-06 — Chat Educacional](epicos/EP06-chat-educacional.md) — referência primária para responsividade do chat.
- Épico [EP-02 — Gestão de Usuários](epicos/EP02-gestao-usuarios.md) — referência para tabelas e formulários.
- Épico [EP-01 — Autenticação](epicos/EP01-autenticacao.md) — referência para formulários e tela pública.
- Épico [EP-09 — Gestão do Modelo de IA](epicos/EP09-gestao-modelo-ia.md) — referência para tabela do catálogo.
- Figma file: `5MClPpSqI9R42MPCwTcDzH` (Tutor — Sprint 2).
