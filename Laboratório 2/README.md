# Laboratório 2

## Atividade 1

Foi escolhido o **estilo arquitetural** em camadas composto de 4 componentes para a **arquitetura de software** da aplicação. Esses componentes estão separados nos 4 arquivos python desse repositório. As funcionalidades de cada um deles estão a seguir:

### Cliente
- É a interface de interação com o usuário. Cria um socket do cliente e inicia a interação com o servidor. 
- Recebe um comando do usuário, que pode ser consultar uma chave existente no dicionário, escrever um novo par chave, valor no dicionário ou finalizar a aplicação.
- Verifica se o par chave, valor do usuário está no formato esperado ("chave: valor").
- Passa para a camada do servidor o tipo de comando que o usuário digitou, juntamente com o dado passado, podendo ser uma chave, no caso de uma consulta ou o par chave, valor para uma inserção.
- Se o usuário digitar "fim", finaliza o cliente.

### Servidor
- É a camada que se comunica com o cliente e recebe as requisições. Inicia o socket do servidor e aceita a conexão com um ou mais clientes.
- Carrega o dicionário da camada de processamento assim que o servidor é iniciado.
- Cria uma thread para cada cliente e armazena os clientes que estão ativos.
- Atende as requisições dos clientes, enviando para a camada de processamento a mensagem que foi recebida do cliente e enviando para o cliente a resposta obtida da camada de processamento.
- Aceita comandos do administrador, como finalizar o servidor, que esperará todos os clientes ativos no momento finalizarem para encerrar. Também aceita a opção de remover uma chave do dicionário, solicitando à camada de processamento essa operação e retornando um erro caso a chave não exista.

### Processamento
- Carrega ou armazena o dicionário da camada de dados.
- Recebe as mensagens do servidor e decodifica, separando o que é o comando e o que é o dado de fato. De acordo com o número do comando, realiza a consulta ou a inserção.
- Na consulta, retorna a lista de valores encontrados em ordem alfabética ou uma lista vazia, se não foi encontrada aquela chave.
- Na inserção, adiciona um novo valor à chave, caso ela exista e caso contràrio, cria uma nova lista de valores com o valor passado para a chave.
- Remove uma chave do dicionário e retorna uma mensagem de sucesso à camada do servidor e se a chave não existir, retorna um erro.

### Dados
- É o componente que realiza duas operações: carrega o dicionário do disco e retorna para a camada de processamento ou armazena o dicionário recebido da camada de processamento no disco.

## Atividade 2

O lado **cliente** ficará com o componente de cliente, enquanto o lado **servidor** ficará com os outros 3 componentes (servidor, processamento e dados).

### Mensagens
1. O cliente primeiramente envia o tamanho da mensagem que será passada para o servidor.
2. O cliente envia as mensagens para o servidor no formato `tipo_comando#dado`, o tipo do comando pode ser 1 para consulta ou 2 para escrita. 
3. O servidor recebe o tamanho da mensagem e realiza um loop com recv até toda a mensagem ser recebida. Em caso de erro, a operação é abortada. Após isso, é realizado um tratamento na mensagem, separando as duas informações. 
4. Na resposta, o servidor realiza o mesmo procedimento que o cliente realizou de enviar primeiramente o tamanho da resposta.
5. Se o comando enviado pelo cliente for um comando de consulta, retorna a lista de valores ou uma lista vazia, dependendendo da existência ou não da chave. Se for um comando de escrita, retorna a mensagem dizendo se a entrada foi inserida ou atualizada para o cliente.
6. O cliente recebe primeiro o tamanho da mensagem e realiza um loop até receber a mensagem completa ou abortar a operação, caso ocorra um erro.
7. A mensagem final que chega para o cliente já está pronta para ser mostrada ao usuário.

## Decisões de projeto
- Para armazenar o dicionário, foi utilizado a biblioteca `json`, apenas por uma questão de facilidade ao visualizar o arquivo.
- Se o dicionário não existir, cria um novo no diretório atual.
- É aceito chave e valor com qualquer caractere que não seja dois pontos (:). Exemplos de entradas aceitas: chave:valor, chave: valor, chave : valor, chave 1 : valor 1.
- A chave para consulta é tratada para retirar os espaços do input, então mesmo que o usuário dê alguns espaços, apenas a palavra passada é lida.
- Foi utilizado threads e não processos.
- Para a leitura completa de mensagens com `recv`, foi utilizada a abordagem de enviar primeiramente o tamanho da mensagem para fazer uma leitura com repetição até alcançar esse tamanho. Se não a mensagem não for lida completamente, a operação é abortada. Também foi utilizado `sendall`.
