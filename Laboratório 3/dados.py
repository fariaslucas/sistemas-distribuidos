import json
import os

class Dados:
    def __init__(self):
        self.dicionario = {}

    def carrega_dicionario(self):
        '''Carrega o dicionário do disco através de um arquivo json.

        :return: O dicionário armazenado'''

        # junta o caminho do diretório desse arquivo com o nome do json para encontrar o arquivo
        caminho = os.path.join(os.getcwd(), 'dicionario.json')

        if os.path.exists(caminho):
            with open('dicionario.json', 'r') as arquivo:
                self.dicionario = json.load(arquivo)
        return self.dicionario

    def armazena_dicionario(self, dicionario):
        '''Armazena o dicionário no disco utilizando um arquivo json.

        :param dicionario: o dicionário a ser armazenado'''

        with open('dicionario.json', 'w') as arquivo:
            json.dump(dicionario, arquivo)