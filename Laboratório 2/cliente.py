import socket
import re

HOST = 'localhost'
PORT = 5000

CONSULTAR = 1
ESCREVER = 2 

OPCAO_CONSULTAR = 'consultar'
OPCAO_ESCREVER = 'escrever'
OPCAO_FIM = 'fim'

class Cliente:
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Internet (IPv4 + TCP)

	def valida_entrada_correta(self, entrada):
		'''Verifica se uma entrada está na forma chave:valor.
		Uma entrada correta é definida como uma string que contém:
			- Uma ou mais palavras (com ou sem espaços) seguidas de dois pontos (:)
			- Uma ou mais palavras (com ou sem espaços) depois dos dois pontos (:)
		
		:param entrada: a palavra que será verificada
		:return: True se correspondeu ao padrão passado ou False, caso contrário'''

		# o padrão consiste de um conjunto de duas palavras separadas por dois pontos
		padrao = r'^[^:]+:[^:]+$'
		verificacao = re.match(padrao, entrada)
		return bool(verificacao)
		
	def faz_requisicoes(self, dado, tipo_comando):
		'''Faz requisicoes ao servidor e exibe o resultado.

		:param sock: socket conectado ao servidor
		:param dado: dado que será passado na requisição
		:param tipo_comando: tipo de comando'''

		# junta o tipo de comando com o dado em uma mensagem só, separados por '#'
		mensagem = f"{tipo_comando}#{dado}"

		# envia primeiro o tamanho da mensagem e depois a mensagem
		self.sock.sendall(len(mensagem).to_bytes(4, 'big'))
		self.sock.sendall(mensagem.encode('utf-8'))

		# recebe primeiro o tamanho da mensagem e depois a mensagem
		tamanho_resposta = int.from_bytes(self.sock.recv(4), 'big')
		try:
			resposta = self.recebe_completo(tamanho_resposta).decode('utf-8')
		except Exception as e:
			print(e.args[0])
			return

		if tipo_comando == CONSULTAR:
			print(f"Valores: {resposta}\n")
		elif tipo_comando == ESCREVER:
			print(f"{resposta}\n")

	def recebe_completo(self, tamanho_mensagem):
		'''Realiza um loop até receber todos os dados enviados pelo cliente.

		:param sock: o socket por onde a mensagem é recebida
		:param tamanho_mensagem: o tamanho da mensagem para saber quando parar de receber
		:return: a mensagem completa recebida
		:raises Exception: lança uma exception caso não tenha recebido nada dentro do loop'''

		mensagem = b''
		while len(mensagem) < tamanho_mensagem:
			pacote = self.sock.recv(tamanho_mensagem - len(mensagem)) # recebe a quantidade de bytes restantes
			if not pacote:
				raise Exception("Erro: A mensagem não foi recebida completamente")
			mensagem += pacote
		return mensagem

	def mostra_menu(self):
		'''Mostra o menu com opções para o usuário.'''

		menu = ("Bem vindo(a)! Escolha uma opção.\n"
				"1. Digite 'consultar' para buscar uma entrada\n"
				"2. Digite 'escrever para adicionar uma nova entrada\n"
				"3. Digite 'fim' para encerrar")
		print(menu)

	def consultar(self):
		'''Lê o dado do usuário e faz a requisição de consulta.'''

		print("Digite a chave a ser consultada: ")
		dado = input()
		self.faz_requisicoes(dado, CONSULTAR)

	def escrever(self):
		'''Lê o dado do usuário e faz a requisição de consulta.'''

		# fica em um loop até o usuário passar o padrão de chave:valor correto
		while True:
			print("Digite uma chave e um valor a serem inseridos separados por ':':")
			dado = input()

			if self.valida_entrada_correta(dado):
				self.faz_requisicoes(dado, ESCREVER)
				break

			print("Erro: Entrada inválida. Tente novamente.\n")
			
	def main(self):
		'''Funcao principal do cliente'''

		self.sock.connect((HOST, PORT))

		# lê as mensagens do usuário até ele digitar 'fim'
		while True:
			self.mostra_menu()
			comando = input().strip()

			if comando == OPCAO_CONSULTAR:
				self.consultar()

			elif comando == OPCAO_ESCREVER:
				self.escrever()

			elif comando == OPCAO_FIM:
				break

			else:
				print("Erro: Comando inválido. Tente novamente.\n")

		self.sock.close()

if __name__ == '__main__':
	cliente = Cliente(HOST, PORT)
	cliente.main()