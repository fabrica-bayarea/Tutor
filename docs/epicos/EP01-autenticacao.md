> **Documento de Requisitos**
> **Projeto Tutor**

| Versão | Data | Descrição | Autor |
|--------|-----------|---------------|-----------|
| 1.2 Sprint 2 | 19/04/2026 | Login US-01 e US-02, Criação de senha via link de convite US-03 e Encerramento de sessão US-05 | Patricia Pereira Martins |
| 1.3 Sprint 3 | 10/05/2026 | Inclusão do histórico de revisão | Patricia Pereira Martins |

---

# EP-01 — Autenticação e Controle de Acesso

**Descrição:** Permite que usuários acessem a plataforma de forma segura, com suporte a login por matrícula e senha, login com conta Google, e controle de permissões por perfil.

**Personas:** Administrador, Professor, Aluno

**Protótipo:** [Design System](https://www.figma.com/design/5MClPpSqI9R42MPCwTcDzH/Tutor----Sprint-2?node-id=258-2&p=f&t=ukWioTEjrb08WqKU-0)

**Protótipo Sprint 2 — Autenticação:** [Autenticação](https://www.figma.com/design/5MClPpSqI9R42MPCwTcDzH/Tutor----Sprint-2?node-id=259-2&p=f&t=ukWioTEjrb08WqKU-0)

---

## US-01 — Login com matrícula e senha

**Como** usuário da plataforma (administrador, professor ou aluno),
**quero** acessar minha conta informando minha matrícula e minha senha,
**para que** eu possa utilizar as funcionalidades disponíveis para o meu perfil.

### Regras de Negócio

- O usuário deve informar sua matrícula institucional como identificador de acesso.
- A senha é sempre obrigatória.
- Apenas usuários cadastrados e ativos na plataforma podem realizar login.
- Usuários desativados não conseguem acessar a plataforma.
- Após autenticação, o sistema deve direcionar o usuário para a tela inicial correspondente ao seu perfil:
  - Administrador → painel de administração
  - Professor → painel do professor
  - Aluno → tela de seleção de matéria

### Regras de Validação

- Matrícula é obrigatória; o campo não pode estar em branco.
- Senha é obrigatória; o campo não pode estar em branco.
- Credenciais inválidas (matrícula não encontrada ou senha incorreta) exibem sempre a mesma mensagem genérica: _"Matrícula ou senha incorretos. Verifique e tente novamente."_ — o sistema não revela qual dos campos está errado por motivos de segurança.
- O campo de senha deve ser exibido com caracteres ocultos por padrão, com opção de visualizar.

### Regras de Interface

- A tela de login deve ser a primeira página exibida para usuários não autenticados.
- Deve haver um campo de matrícula institucional com texto de orientação: _"Matrícula institucional"_.
- O botão de entrar deve estar desabilitado enquanto os campos obrigatórios estiverem em branco.
- A tela deve exibir o link "Esqueci minha senha" abaixo do formulário.
- A tela deve exibir a opção de login com Google (ver US-02).
- Mensagens de erro de credenciais devem aparecer abaixo do formulário (não vinculadas a um campo específico), em linguagem clara e sem termos técnicos.

### Requisitos Não Funcionais

- A resposta ao tentar fazer login deve ocorrer em no máximo 5 segundos.
- A comunicação entre o navegador e a plataforma deve ser protegida (dados não trafegam em aberto).
- As senhas nunca são armazenadas em formato legível — apenas de forma protegida.
- A sessão autenticada expira após período configurável de inatividade.

### Pré-requisitos

- O usuário deve ter sido previamente cadastrado por um administrador.
- O usuário deve estar com o status ativo na plataforma.

### Critérios de Aceitação

- [ ] Usuário ativo consegue fazer login informando matrícula + senha correta.
- [ ] Usuário inativo não consegue fazer login e recebe mensagem explicativa.
- [ ] Credenciais incorretas exibem mensagem de erro sem revelar qual campo está errado por motivos de segurança.
- [ ] Após login bem-sucedido, o usuário é redirecionado para a tela correta do seu perfil.

---

## US-02 — Login com conta Google

**Como** usuário da plataforma,
**quero** acessar minha conta utilizando minha conta Google,
**para que** eu não precise memorizar uma senha adicional e tenha um acesso mais ágil.

### Regras de Negócio

- O login com Google só é permitido para usuários que já possuem cadastro ativo na plataforma.
- O e-mail da conta Google utilizada deve corresponder ao e-mail institucional cadastrado para o usuário.
- A plataforma não cria novos usuários automaticamente a partir do login com Google — o cadastro prévio pelo administrador é obrigatório.
- Após autenticação via Google, o usuário é direcionado para a tela inicial correspondente ao seu perfil.

### Regras de Validação

- Caso o e-mail da conta Google não esteja associado a nenhum usuário ativo na plataforma, exibir mensagem: _"Sua conta Google não está vinculada a nenhum usuário nesta plataforma. Entre em contato com o administrador."_
- Se o usuário estiver desativado, o login com Google também deve ser bloqueado.

### Regras de Interface

- A tela de login deve exibir um botão "Entrar com Google" visualmente destacado e separado do formulário de matrícula/e-mail e senha.
- Ao clicar no botão, o usuário é redirecionado para a tela de autenticação do Google e retorna automaticamente à plataforma após a autorização.
- Caso o login com Google falhe por qualquer motivo, exibir mensagem: _"Não foi possível autenticar com o Google. Tente novamente ou use sua matrícula e senha."_

### Requisitos Não Funcionais

- O fluxo de autenticação com Google deve ser concluído em no máximo 10 segundos (excluindo o tempo de resposta do Google).
- A comunicação com o serviço do Google deve ser realizada de forma segura.

### Pré-requisitos

- O usuário deve ter sido previamente cadastrado por um administrador com o e-mail que será usado na conta Google.
- A plataforma deve estar configurada para aceitar autenticação via Google (configuração realizada pela equipe técnica).

### Critérios de Aceitação

- [ ] Usuário ativo com e-mail Google correspondente ao cadastro consegue fazer login.
- [ ] Usuário não cadastrado recebe mensagem orientando a contatar o administrador.
- [ ] Usuário desativado não consegue acessar mesmo com conta Google válida.
- [ ] Em caso de falha no processo, o usuário é orientado a usar o login tradicional.

---

## US-03 — Criação de senha via link de convite

**Como** usuário que acabou de ter minha conta criada pelo administrador,
**quero** receber um link de convite para criar minha própria senha antes de acessar a plataforma,
**para que** minha conta fique protegida com uma senha que só eu conheço desde o primeiro acesso.

### Regras de Negócio

- Ao cadastrar um novo usuário, o sistema gera automaticamente um link de convite único e o envia para o e-mail institucional do usuário.
- O link de convite é de uso único — expira **somente após o primeiro acesso**, ou seja, após o usuário criar sua senha com sucesso.
- Enquanto o usuário não usar o link, ele permanece válido indefinidamente — não há prazo de expiração por tempo.
- Ao clicar no link, o usuário é direcionado para uma tela onde cria sua própria senha. O sistema nunca define uma senha pelo usuário.
- Após criar a senha, o link é invalidado automaticamente e o usuário é redirecionado para a tela inicial do seu perfil.
- Caso o usuário perca o e-mail de convite ou o link já tenha sido utilizado, ele pode acessar a plataforma pela opção "Esqueci minha senha" informando sua matrícula ou e-mail — o fluxo de recuperação funciona normalmente (ver US-06).
- Este fluxo se aplica apenas a usuários com login por matrícula e senha; usuários que acessam exclusivamente via Google não precisam criar senha.

### Regras de Validação

- A nova senha deve ter no mínimo 8 caracteres.
- A nova senha deve conter ao menos uma letra maiúscula, uma minúscula e um número.
- O usuário deve digitar a nova senha duas vezes para confirmação; as duas entradas devem ser idênticas.
- Caso as senhas não coincidam, exibir: _"As senhas não conferem. Por favor, digite novamente."_
- Ao acessar um link de convite já utilizado, exibir: _"Este link de convite já foi usado. Caso precise acessar a plataforma, use a opção 'Esqueci minha senha' na tela de login."_

### Regras de Interface

- O e-mail de convite deve conter o nome do usuário, o nome da plataforma e um botão ou link com o texto "Criar minha senha".
- A tela de criação de senha deve deixar claro o contexto: _"Bem-vindo! Crie uma senha para acessar a plataforma."_
- Devem existir dois campos: "Nova senha" e "Confirmar nova senha", ambos com opção de visualizar o conteúdo.
- O botão de confirmar deve estar desabilitado até que os requisitos mínimos sejam atendidos.

### Requisitos Não Funcionais

- A senha criada deve ser armazenada de forma protegida, nunca em formato legível.
- O e-mail de convite deve ser enviado em no máximo 2 minutos após o cadastro.

### Pré-requisitos

- O usuário deve ter sido cadastrado por um administrador com um e-mail institucional válido.
- O usuário deve ter acesso ao e-mail informado no cadastro.

### Critérios de Aceitação

- [ ] Ao ser cadastrado, o usuário recebe um e-mail com o link de convite.
- [ ] O link permanece válido até ser utilizado — não expira por tempo.
- [ ] Ao clicar no link, o usuário é direcionado para a tela de criação de senha.
- [ ] Senha que não atende aos requisitos mínimos é rejeitada com mensagem explicativa.
- [ ] Após criar a senha, o link é invalidado e o usuário acessa a plataforma normalmente.
- [ ] Ao tentar usar um link já utilizado, o usuário recebe mensagem orientando a usar "Esqueci minha senha".
- [ ] O fluxo "Esqueci minha senha" funciona normalmente como alternativa para quem perdeu o convite ou já utilizou o link.

---

## US-05 — Encerramento de sessão

**Como** usuário autenticado,
**quero** poder encerrar minha sessão a qualquer momento e ter minha sessão encerrada automaticamente após inatividade,
**para que** minha conta fique protegida caso eu esqueça de sair ou use um dispositivo compartilhado.

### Regras de Negócio

- O usuário pode encerrar sua sessão voluntariamente a qualquer momento clicando em "Sair".
- A sessão expira automaticamente após um período configurável de inatividade (definido pelo administrador da plataforma).
- Após o encerramento ou expiração, o usuário é redirecionado para a tela de login.
- Sessões expiradas não permitem continuar usando a plataforma sem novo login.

### Regras de Validação

- Ao tentar realizar qualquer ação com sessão expirada, o sistema redireciona para o login exibindo: _"Sua sessão expirou. Por favor, faça login novamente."_

### Regras de Interface

- A opção "Sair" deve estar sempre visível e acessível no menu ou cabeçalho da plataforma.
- Antes de confirmar o logout, não é necessário exibir confirmação — a ação é imediata.
- Após o logout, o botão "voltar" do navegador não deve permitir retornar à área autenticada.

### Requisitos Não Funcionais

- O encerramento de sessão deve ser processado imediatamente.

### Pré-requisitos

- O usuário deve estar autenticado.

### Critérios de Aceitação

- [ ] Clicar em "Sair" encerra a sessão imediatamente e redireciona para o login.
- [ ] Sessão inativa por tempo configurado expira automaticamente.
- [ ] Após expiração, qualquer ação redireciona para o login com mensagem informativa.
- [ ] Não é possível retornar à área logada pelo botão "voltar" do navegador após logout.
