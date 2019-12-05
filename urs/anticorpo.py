import random
from copy import copy

class Anticorpo(object):
    (
        INDICE,
        KEY
    ) = range(2)

    def __init__(self):
        self._afinidade = 0
        self._receptores = [] # lista de tuplas
        self._afinidade_normalizada = 0

    def hipermuta(self, alfa):
        for e, i in enumerate(copy(self._receptores)):
            if random.random() <= alfa:
                self._receptores[e] = (i[self.INDICE], random.uniform(0,1)) 
        self._receptores.sort(key=lambda x: -x[self.KEY])
            
    def gera_aleatorio(self, chaves):
        self._receptores = [(i, random.uniform(0,1)) for i in chaves]
        self._receptores.sort(key=lambda x: -x[self.KEY])

    def avalia(self, funcao):
        self._afinidade = funcao(self._receptores)

    @property
    def afinidade_normalizada(self):
        return self._afinidade_normalizada
    
    @afinidade_normalizada.setter
    def afinidade_normalizada(self, valor):
        self._afinidade_normalizada = valor

    @property
    def afinidade(self):
        return self._afinidade