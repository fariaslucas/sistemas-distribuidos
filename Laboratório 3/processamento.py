from dados import Dados

ENTRADA_INSERIDA = "Chave {} inserida com o valor {}."
ENTRADA_ATUALIZADA = "Valor {} acrescentado na chave {}."
CHAVE_REMOVIDA = "Chave {} removida com sucesso"
CHAVE_NAO_ENCONTRADA = "A chave {} não existe."

class Processamento:
    def __init__(self):
        self.dados = Dados()
        self.dicionario = {}

    def insere(self, chave, valor):
        '''Insere um par chave e valor no dicionário.

        :param chave: a chave que será modificada
        :param valor: o valor que será inserido na chave
        :return: mensagem informando se a foi inserida uma nova chave ou atualizada uma chave já existente'''

        self.dicionario = self.dados.carrega_dicionario()

        if chave in self.dicionario:
            self.dicionario[chave].append(valor)
            self.dados.armazena_dicionario(self.dicionario)
            return ENTRADA_ATUALIZADA.format(valor, chave)
        else:
            self.dicionario[chave] = [valor]
            self.dados.armazena_dicionario(self.dicionario)
            return ENTRADA_INSERIDA.format(chave, valor)

    def retorna_valores_ordenados(self, chave):
        '''Retorna todos os valores de uma chave do dicionário.

        :param chave: a chave que terá os valores retornados
        :return: os valores da chave ordenados em ordem alfabética, caso essa chave exista, ou uma lista vazia, caso contrário'''

        self.dicionario = self.dados.carrega_dicionario()

        return sorted(self.dicionario[chave]) if chave in self.dicionario else []

    def remove_chave(self, chave):
        '''Remove uma chave do dicionário.

        :param chave: a chave que será removida
        :return: Mensagem informando que a chave foi removida
        :raises KeyError: retorna essa exceção se a chave não existir'''

        self.dicionario = self.dados.carrega_dicionario()

        try:
            del self.dicionario[chave]
            self.dados.armazena_dicionario(self.dicionario)
            return CHAVE_REMOVIDA.format(chave)
        except KeyError:
            return CHAVE_NAO_ENCONTRADA.format(chave)