import socket

HOST = 'localhost'
PORTA = 5000        

sock = socket.socket() 

sock.connect((HOST, PORTA)) 

# loop para receber e enviar várias mensagens
while True:
    msg = input("Mensagem enviada: ")
    if not msg or msg == 'fim': break

    # envia msg
    sock.send(bytes(msg, encoding='utf-8'))

    # recebe a mensagem enviada e imprime
    msg_recebida = sock.recv(1024)
    print("Mensagem recebida:", str(msg_recebida, encoding='utf-8'))

sock.close() 