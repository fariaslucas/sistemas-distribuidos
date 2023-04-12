import socket

HOST = ''  
PORTA = 5000  

sock = socket.socket() 

sock.bind((HOST, PORTA))

sock.listen(5) 

print("Esperando conexões...")

novoSock, endereco = sock.accept()
print ('Conectado com: ', endereco)

while True:
	msg = novoSock.recv(1024) 
	if not msg: break 
	print(str(msg,  encoding='utf-8'))
	novoSock.send(msg) #envia mensagem de volta

novoSock.close() 
sock.close()