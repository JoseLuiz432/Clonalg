from copy import deepcopy
from math import exp
from random import random
from urs.anticorpo import Anticorpo

class Populacao(object):
    def inicia_populacao(self, tamanho, chaves):
        """
            Gerar populacao inicial de anti-corpos
            de maneira aleatoria
        """
        populacao = []
        self._chaves_solucao = chaves
        for _ in range(tamanho):
            anticorpo = Anticorpo()
            anticorpo.gera_aleatorio(chaves)
            populacao.append(anticorpo)
        
        return populacao

    def avalia(self, populacao, funcao_avaliacao):
        """
            avalia a afinidade da 
            populacao utilizando a funcao de avaliacao passada

        """
        for anticorpo in populacao:
            anticorpo.avalia(funcao_avaliacao)

    def normaliza(self, anticorpos):
        """
            normaliza as afinidades
        """
        media = sum([x.afinidade for x in anticorpos]) /  len(anticorpos)
        soma = 0
        for anticorpo in anticorpos:
            soma += (anticorpo.afinidade - media)**2
        if soma == 0:
            desvio = 0.0000001    
        else:
            desvio = (soma / len(anticorpos))**(1/2)
        
        for anticorpo in anticorpos:
            anticorpo.afinidade_normalizada = (anticorpo.afinidade - media) / desvio

    def seleciona(self, anticorpos, n_selecao):
        """
            seleciona os anticorpos para clonagem
        """
        return anticorpos[:n_selecao]

    def hipermuta(self, clones, itensidade_hipermutacao):
        """
            hipermuta os clones gerados
        """
        for clone in clones:
            # alfa = clone.afinidade / (itensidade_hipermutacao * 100)     
            alfa = exp(-itensidade_hipermutacao * clone.afinidade_normalizada)
            clone.hipermuta(alfa)
    
    def substitui_populacao(self, anticorpos, clones, tamanho_pop, n_aleatorios, funcao_avaliacao, n_selecao, chaves_solucao):
        """
            seleciona os n_selecao anticorpos com menor afinidade e
            substitui pelos melhores clones gerados
            ordena e 
            seleciona os n_aleatorios anticorpos com menor afinidade
            e gera n_aleatorios anticorpos novos no lugar
        """
        anticorpos[tamanho_pop-n_selecao:] = clones[:n_selecao]
        aleatorios = []
        for _ in range(n_aleatorios):
            anticorpo = Anticorpo()
            anticorpo.gera_aleatorio(chaves_solucao)
            anticorpo.avalia(funcao_avaliacao)
            aleatorios.append(anticorpo)
            
        
        anticorpos += aleatorios
        
        return sorted(anticorpos, key=lambda x:-x.afinidade)[:tamanho_pop]


    def clona(self, selecionados, numero_clones, n):
        """
            clona os anticorpos selecionados 
        """
        clones = []
        for anticorpo in selecionados:
            n_copy = round((numero_clones * n)/ (selecionados.index(anticorpo)+1))
            for i in range(n_copy):
                clones.append(deepcopy(anticorpo))
        
        return clones

