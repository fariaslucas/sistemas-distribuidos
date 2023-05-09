import socket
import re
import struct

HOST = 'localhost'
PORT = 5000

CONSULTAR = 1
ESCREVER = 2 

OPCAO_CONSULTAR = 'consultar'
OPCAO_ESCREVER = 'escrever'
OPCAO_FIM = 'fim'

def valida_entrada_correta(entrada):
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

def inicia_cliente():
    '''Cria um socket de cliente e conecta-se ao servidor.
    
	:return: socket criado'''

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Internet (IPv4 + TCP) 
	# conecta-se com o servidor
    sock.connect((HOST, PORT))
    return sock

def faz_requisicoes(sock, dado, tipo_comando):
	'''Faz requisicoes ao servidor e exibe o resultado.

	:param sock: socket conectado ao servidor
	:param dado: dado que será passado na requisição
	:param tipo_comando: tipo de comando'''

	# junta o tipo de comando com o dado em uma mensagem só, separados por '#'
	mensagem = f"{tipo_comando}#{dado}"

	# envia primeiro o tamanho da mensagem e depois a mensagem
	sock.sendall(len(mensagem).to_bytes(4, 'big'))
	sock.sendall(mensagem.encode('utf-8'))

	# recebe primeiro o tamanho da mensagem e depois a mensagem
	tamanho_resposta = int.from_bytes(sock.recv(4), 'big')
	try:
		resposta = recebe_completo(sock, tamanho_resposta).decode('utf-8')
	except Exception as e:
		print(e.args[0])
		return

	if tipo_comando == CONSULTAR:
		print(f"Valores: {resposta}\n")
	elif tipo_comando == ESCREVER:
		print(f"{resposta}\n")

def recebe_completo(sock, tamanho_mensagem):
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

def mostra_menu():
	'''Mostra o menu com opções para o usuário.'''

	menu = ("Bem vindo(a)! Escolha uma opção.\n"
	 		"1. Digite 'consultar' para buscar uma entrada\n"
			"2. Digite 'escrever para adicionar uma nova entrada\n"
			"3. Digite 'fim' para encerrar")
	print(menu)

def consultar(sock):
	'''Lê o dado do usuário e faz a requisição de consulta.'''

	print("Digite a chave a ser consultada: ")
	dado = input()
	faz_requisicoes(sock, dado, CONSULTAR)

def escrever(sock):
	'''Lê o dado do usuário e faz a requisição de consulta.'''

	# fica em um loop até o usuário passar o padrão de chave:valor correto
	while True:
		print("Digite uma chave e um valor a serem inseridos separados por ':':")
		dado = input()

		if valida_entrada_correta(dado):
			faz_requisicoes(sock, dado, ESCREVER)
			break

		print("Erro: Entrada inválida. Tente novamente.\n")
		
	
def main():
	'''Funcao principal do cliente'''

	sock = inicia_cliente()

	# lê as mensagens do usuário até ele digitar 'fim'
	while True:
		mostra_menu()
		comando = input().strip()

		if comando == OPCAO_CONSULTAR:
			consultar(sock)

		elif comando == OPCAO_ESCREVER:
			escrever(sock)

		elif comando == OPCAO_FIM:
			break

		else:
			print("Erro: Comando inválido. Tente novamente.\n")

	sock.close()

main()