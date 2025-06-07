# Tutor/backend/appication/socket
O socket é o que permite estabelecer uma conexão persistente e assíncrona entre cliente e servidor, permitindo que ambos se comuniquem de forma bidirecional e em tempo real, e sem depender de requisições HTTP convencionais.

## Eventos
Os eventos são "gatilhos" usados para executar determinadas ações no servidor.

Em requisições HTTP convencionais, esses gatilhos seriam as próprias requisições em si. Ao enviar uma requisição em um determinado endpoint, uma ação é executada por baixo dos panos, e então a resposta é devolvida para o cliente ao final do processo.

Com sockets, não precisamos estabelecer novas conexões com o servidor a cada requisição. Por termos uma conexão persistente e assíncrona, podemos enviar e receber dados em tempo real, por meio de eventos emitidos tanto pelo cliente quanto pelo servidor.

É como se tanto o cliente quanto o servidor estivessem sempre "ouvindo" atentamente o que está acontecendo, e então realizassem ações específicas de acordo com os eventos emitidos por eles.

## Handlers
Os handlers são funções chamadas para executar determinadas ações no servidor quando eventos são recebidos.

Por exemplo, quando um aluno envia uma mensagem numa conversa com a IA, um evento com nome "mensagem_enviada" é emitido no front-end, e o back-end, que está "ouvindo" atentamente a tudo o que acontece, recebe esse evento e chama uma função que executa uma série de ações para processar a mensagem corretamente e devolver uma resposta, como:
1. Receber a mensagem do aluno
2. Salvar a mensagem no banco de dados
3. Passar a mensagem para o modelo de IA
4. Gerar uma mensagem de resposta com o modelo de IA
5. Salvar essa outra mensagem no banco de dados
6. Enviar essa resposta para o aluno

Ao enviar a resposta gerada pela IA, o back-end emite um evento com nome "mensagem_respondida" para o front-end, que também executa uma série de ações para exibir a resposta gerada pela IA na conversa, como:
1. Receber a resposta gerada pela IA
2. Atualizar o estado de `mensagens` para incluir essa nova resposta
3. Renderizar a nova mensagem na conversa