import socket
import select
import sys
import threading
from processamento import Processamento

HOST = '' # vazio indica que podera receber requisicoes a partir de qq interface de rede da maquina
PORT = 5000

class Servidor:
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Internet( IPv4 + TCP)
		self.entradas = [sys.stdin]
		self.clientes = []
		self.processamento = Processamento()

	def inicia_servidor(self):
		'''Coloca o socket de servidor em modo de espera por conexoes.
		
		:return: o socket criado'''

		# vincula a localizacao do servidor
		self.sock.bind((HOST, PORT))

		# coloca-se em modo de espera por conexoes
		self.sock.listen(5) 

		# configura o socket para o modo nao-bloqueante
		self.sock.setblocking(False)

		# inclui o socket principal na lista de entradas de interesse
		self.entradas.append(self.sock)

	def aceita_conexao(self):
		'''Aceita o pedido de conexao de um cliente
		
		:param sock: o socket do servidor
		:return: o endereco do cliente'''

		# estabelece conexao com o proximo cliente
		cliente_sock, cliente_endr = self.sock.accept()

		# cria nova thread para o cliente
		cliente = threading.Thread(target=self.atende_requisicoes, args=(cliente_sock, cliente_endr))
		cliente.start()
		self.clientes.append(cliente)
		return cliente_endr

	def atende_requisicoes(self, cliente_sock, cliente_endr):
		'''Recebe os dados e realiza uma consulta ou escrita, de acordo com o comando passado, até 
		o cliente finalizar. Retorna a resposta da operação feita para o cliente.

		:param cliente_sock: socket da conexao
		:param cliente_endr: o endereço do cliente'''

		while True:
			# recebe primeiro o tamanho da mensagem e depois a mensagem
			tamanho_mensagem = int.from_bytes(cliente_sock.recv(4), 'big')
			try:
				mensagem = self.recebe_completo(cliente_sock, tamanho_mensagem)
			except Exception as e:
				print(e.args[0])
				return

			if not mensagem: # mensagem vazia: cliente encerrou
				print(str(cliente_endr) + '-> encerrou')
				cliente_sock.close()
				return

			resposta = self.processamento.trata_mensagens(mensagem.decode('utf-8'))

			# envia o tamanho da resposta e em seguida a resposta
			cliente_sock.sendall(len(resposta).to_bytes(4, 'big'))
			cliente_sock.sendall(resposta.encode("utf-8"))

	def recebe_completo(self, sock, tamanho_mensagem):
		'''Realiza um loop até receber todos os dados enviados pelo cliente.

		:param sock: o socket por onde a mensagem é recebida
		:param tamanho_mensagem: o tamanho da mensagem para saber quando parar de receber
		:return: a mensagem completa recebida
		:raises Exception: lança uma exception caso não tenha recebido nada dentro do loop'''

		mensagem = b''
		while len(mensagem) < tamanho_mensagem:
			pacote = sock.recv(tamanho_mensagem - len(mensagem)) # recebe a quantidade de bytes restantes
			if not pacote:
				raise Exception("Erro: A mensagem não foi recebida completamente")
			mensagem += pacote
		return mensagem


	def remove_chave(self, chave):
		'''Remove a chave do dicionário e retorna o resultado ou um erro.

		:param chave: chave que será removida'''

		try:
			resultado = self.processamento.remove_chave(chave)
			print(resultado)
		except KeyError as e:
			print(f"Erro: {e.args[0]}")


	def main(self):
		'''Inicializa e implementa o loop principal (infinito) do servidor'''

		self.inicia_servidor()
		print("Pronto para receber conexoes...")

		while True:
			leitura, _, _ = select.select(self.entradas, [], [])
			for pronto in leitura:
				if pronto == self.sock:  #pedido novo de conexao
					cliente_endr = self.aceita_conexao()
					print ('Conectado com: ', cliente_endr)

				elif pronto == sys.stdin: #entrada padrao
					cmd = input().strip()
					if cmd == 'fim': #solicitacao de finalizacao do servidor
						for c in self.clientes: #aguarda todas as threads terminarem
							c.join()
						self.processamento.armazena_dicionario()
						self.sock.close()
						sys.exit()

					elif cmd == 'remover': #comando para remover uma entrada do dicionário
						print("Digite a chave que deseja remover:")
						chave = input().rstrip()
						self.remove_chave(chave)

if __name__ == '__main__':
	servidor = Servidor(HOST, PORT)
	servidor.main()