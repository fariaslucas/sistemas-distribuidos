import rpyc
from processamento import Processamento
from rpyc.utils.server import ThreadedServer

PORTA = 5000

class Servidor(rpyc.Service):
	def __init__(self):
		self.processamento = Processamento()

	def on_connect(self, conn):
		cliente_endr = conn._channel.stream.sock.getpeername()
		print("Conectado com:", cliente_endr)

	def on_disconnect(self, conn):
		print("Cliente desconectado")
	
	def exposed_escrever(self, chave, valor):
		return self.processamento.insere(chave, valor)
	
	def exposed_consultar(self, chave):
		return str(self.processamento.retorna_valores_ordenados(chave))
	
	def exposed_remover(self, chave):
		return self.processamento.remove_chave(chave)

if __name__ == '__main__':
	servidor = ThreadedServer(Servidor, port = PORTA)
	servidor.start()