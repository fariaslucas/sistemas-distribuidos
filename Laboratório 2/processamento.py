import dados
import threading

dicionario = {}
lock = threading.Lock()

ENTRADA_INSERIDA = "Chave {} inserida com o valor {}."
ENTRADA_ATUALIZADA = "Valor {} acrescentado na chave {}."
CHAVE_REMOVIDA = "Chave {} removida com sucesso"
CHAVE_NAO_ENCONTRADA = "A chave {} não existe."

CONSULTAR = 1
ESCREVER = 2

def carrega_dicionario():
    '''Carrega o dicionário do disco e salva na variável global.'''
    global dicionario 
    dicionario = dados.carrega_dicionario()
    
def armazena_dicionario():
    '''Armazena o dicionário em disco.'''
    dados.armazena_dicionario(dicionario)

def decodifica_mensagem(mensagem):
    '''Separa a mensagem em comando e dado.

    :param mensagem: a mensagem que vai ser separada
    :return: o comando que representa a operação a ser feita e o dado que será inserido ou consultado'''

    mensagem = mensagem.split("#")
    comando = int(mensagem[0])
    dado = mensagem[1]
    return comando, dado

def trata_dado(dado):
    '''Separa o dado em palavras. Esse tratamento é para o caso onde o usuário passa uma palavra só e com espaços.
        - Se houver uma palavra só, retorna essa palavra, agora sem espaços
        - Se houver mais de uma palavra, não faz nada com o dado
    
    :param dado: o dado que será tratado
    :return: o dado se houver mais de uma palavra ou o mesmo dado sem espaços, caso tenha uma palavra só'''

    palavras_dado = dado.split()
    return dado if len(palavras_dado) > 1 else palavras_dado[0]

def separa_dado(dado):
    '''Separa o dado que será inserido em chave e valor.

    :param dado: o dado que será separado
    :return: o par chave e valor'''

    chave, valor = dado.split(":")
    chave = chave.rstrip()
    valor = valor.lstrip()
    return chave, valor

def trata_mensagens(mensagem):
    '''Realiza o processamento da mensagem recebida e faz a operação desejada

    :param mensagem: a mensagem enviada pelo cliente
    :return: a resposta da operação, podendo ser uma mensagem ou a lista de valores'''

    comando, dado = decodifica_mensagem(mensagem)

    if comando == CONSULTAR:
        resposta = retorna_valores_ordenados(trata_dado(dado))
        return str(resposta)
    elif comando == ESCREVER:
        chave, valor = separa_dado(dado)
        lock.acquire()
        resposta = insere(chave, valor)
        lock.release()
        return resposta

def insere(chave, valor):
    '''Insere um par chave e valor no dicionário.

    :param chave: a chave que será modificada
    :param valor: o valor que será inserido na chave
    :return: mensagem informando se a foi inserida uma nova chave ou atualizada uma chave já existente'''

    if chave in dicionario:
        dicionario[chave].append(valor)
        return ENTRADA_ATUALIZADA.format(valor, chave)
    else:
        dicionario[chave] = [valor]
        return ENTRADA_INSERIDA.format(chave, valor)

def retorna_valores_ordenados(chave):
    '''Retorna todos os valores de uma chave do dicionário.

    :param chave: a chave que terá os valores retornados
    :return: os valores da chave ordenados em ordem alfabética, caso essa chave exista, ou uma lista vazia, caso contrário'''

    return sorted(dicionario[chave]) if chave in dicionario else []

def remove_chave(chave):
    '''Remove uma chave do dicionário.

    :param chave: a chave que será removida
    :return: Mensagem informando que a chave foi removida
    :raises KeyError: retorna essa exceção se a chave não existir'''

    try:
        lock.acquire()
        del dicionario[chave]
        lock.release()
        return CHAVE_REMOVIDA.format(chave)
    except KeyError:
        raise KeyError(CHAVE_NAO_ENCONTRADA.format(chave))