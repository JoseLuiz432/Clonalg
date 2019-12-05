from urs.populacao import Populacao
from time import time
import sys

class Main(object):

    @staticmethod
    def main(numero_clones, itensidade_hipermutacao, tamanho_populacao, n_aleatorios, n_selecao, 
             chaves_solucao, funcao_avaliacao):
        """
        """
        populacao = Populacao()
        anticorpos = populacao.inicia_populacao(tamanho_populacao, chaves_solucao)
        populacao.avalia(anticorpos, funcao_avaliacao)
        anticorpos.sort(key= lambda x: -x.afinidade)
        for _ in range(20):
            populacao.normaliza(anticorpos)
            selecionados = populacao.seleciona(anticorpos, n_selecao)
            clones = populacao.clona(selecionados, numero_clones, len(anticorpos))
            populacao.hipermuta(clones, itensidade_hipermutacao)
            populacao.avalia(clones, funcao_avaliacao)
            clones.sort(key= lambda x: -x.afinidade)
            anticorpos = populacao.substitui_populacao(anticorpos, clones, tamanho_populacao,
                                                       n_aleatorios, funcao_avaliacao, n_selecao, chaves_solucao)
        
        return anticorpos[0]


arquivo = open(sys.argv[1], 'r')


n_vertices = 0
n_arestas = 0
arestas = []
for linha in arquivo.readlines():
    linha = linha.split()
    if linha[0] == 'c':
        continue # atualizar depois
    elif linha[0] == 'p':
        n_vertices = int(linha[2])
        n_arestas = int(linha[3])
    elif linha[0] == 'e':
        arestas.append((int(linha[1]), int(linha[2])))
arquivo.close()
# return n_vertices, n_arestas, arestas

grafo = {}
for aresta in arestas:
    if aresta[0] not in grafo.keys():
        grafo[aresta[0]] = [aresta[1]]
    elif aresta[1] not in grafo[aresta[0]]:
        grafo[aresta[0]].append(aresta[1])  

    if aresta[1] not in grafo.keys():
        grafo[aresta[1]] = [aresta[0]]
    elif aresta[0] not in grafo[aresta[1]]:
        grafo[aresta[1]].append(aresta[0])


def func(key):
    nos = []
    for i in key:
        flag = True
        for j in nos:
            if not i[0] in grafo[j]:
                flag = False
                break
        if flag:
            nos.append(i[0])
    
    return len(nos)
inicio = time()
solucao_best = Main.main(2, 0.4, 100, 30, 20, grafo.keys(), func)
fim = time()
print(solucao_best.afinidade, end='\t')
print(fim - inicio)
