import re
import rpyc

HOST = 'localhost'
PORTA = 5000

OPCAO_CONSULTAR = 'consultar'
OPCAO_ESCREVER = 'escrever'
OPCAO_REMOVER = 'remover'
OPCAO_FIM = 'fim'

class Cliente:
	def __init__(self):
		self.conn = rpyc.connect(HOST, PORTA)

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

	def trata_dado(self, dado):
		'''Separa o dado em palavras. Esse tratamento é para o caso onde o usuário passa uma palavra só e com espaços.
			- Se houver uma palavra só, retorna essa palavra, agora sem espaços
			- Se houver mais de uma palavra, não faz nada com o dado

		:param dado: o dado que será tratado
		:return: o dado se houver mais de uma palavra ou o mesmo dado sem espaços, caso tenha uma palavra só'''

		palavras_dado = dado.split()
		return dado if len(palavras_dado) > 1 else palavras_dado[0]

	def separa_dado(self, dado):
		'''Separa o dado que será inserido em chave e valor.

		:param dado: o dado que será separado
		:return: o par chave e valor'''

		chave, valor = dado.split(":")
		chave = chave.rstrip()
		valor = valor.lstrip()
		return chave, valor

	def consultar(self):
		'''Lê o dado do usuário e faz a requisição de consulta.'''

		print("\nDigite a chave a ser consultada: ")
		dado = input()
		chave = self.trata_dado(dado)
		resposta = self.conn.root.exposed_consultar(chave)
		print(resposta)
		print()

	def escrever(self):
		'''Lê o dado do usuário e faz a requisição de consulta.'''

		print("\nDigite uma chave e um valor a serem inseridos separados por ':':")
		dado = input()
		
		if self.valida_entrada_correta(dado):
			chave, valor = self.separa_dado(dado)
			resposta = self.conn.root.exposed_escrever(chave, valor)
			print(resposta)
		else:
			print("Erro: Entrada inválida. Tente novamente.")
		print()

	def remover(self):
		'''Remove a chave que o usuário digitar.'''

		print("\nDigite a chave que deseja remover:")
		dado = input()
		chave = self.trata_dado(dado)
		resposta = self.conn.root.exposed_remover(chave)
		print(resposta)
		print()

	def mostra_menu(self):
		'''Mostra o menu com opções para o usuário.'''

		menu = ("Bem vindo(a)! Escolha uma opção.\n"
				"1. Digite 'consultar' para buscar uma entrada\n"
				"2. Digite 'escrever para adicionar uma nova entrada\n"
				"3. Digite 'remover' para remover uma entrada\n"
				"4. Digite 'fim' para encerrar")
		print(menu)
				

	def main(self):
		'''Funcao principal do cliente'''

		# lê as mensagens do usuário até ele digitar 'fim'
		while True:
			self.mostra_menu()
			comando = input().strip()

			if comando == OPCAO_CONSULTAR:
				self.consultar()

			elif comando == OPCAO_ESCREVER:
				self.escrever()
			
			elif comando == OPCAO_REMOVER:
				self.remover()

			elif comando == OPCAO_FIM:
				self.conn.close()
				break

			else:
				print("Erro: Comando inválido. Tente novamente.\n")

if __name__ == '__main__':
	cliente = Cliente()
	cliente.main()