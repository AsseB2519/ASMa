from Graph_Aux import Grafo
from Node_Aux import Node
import Location_Aux
import cProfile
from prettytable import PrettyTable
import pstats
import re
import os
from time import sleep


def main():
    print("""
    ----------------------------
    --- Algorithm Comparison ---
    ----------------------------
    """)

    location = "Braga, Portugal" 
    neigh, edges, nodes = Location_Aux.run(location)
    grafoAtual = Grafo(nodes, neigh, edges)
    start = grafoAtual.get_node_by_id(8321237017)
    end = grafoAtual.get_node_by_id(1675798722)
    print("---------------------------------------------\n" +
          "-----Algoritmos de Procura Não Informada-----\n" +
          "---------------------------------------------\n")

    print("---DFS---")

    profilerDFS = cProfile.Profile()
    profilerDFS.enable()
    pathDFS = grafoAtual.procura_DFS(start, end)
    profilerDFS.disable()
    if len(pathDFS[0]) > 0:
        print("\n[SYS] Caminho Encontrado: ")
        print(grafoAtual.converte_caminho(pathDFS[0]))
        print("\n[SYS] Custo: ")
        print(pathDFS[1])
        print("\n")
    else: print("\n[SYS] Caminho não encontrado!")
    
    print("---BFS---")

    profilerBFS = cProfile.Profile()
    profilerBFS.enable()
    pathBFS = grafoAtual.procura_BFS(start, end)
    profilerBFS.disable()
    if len(pathBFS[0]) > 0:
        print("\n[SYS] Caminho Encontrado: ")
        print(grafoAtual.converte_caminho(pathBFS[0]))
        print("\n[SYS] Custo: ")
        print(pathBFS[1])
        print("\n")
    else: print("\n[SYS] Caminho não encontrado!")
    
    print("---Bidirecional---")

    profilerBidirecional = cProfile.Profile()
    profilerBidirecional.enable()
    pathBidirecional = grafoAtual.procura_bidirecional(start, end)
    profilerBidirecional.disable()
    if len(pathBidirecional[0]) > 0:
        print("\n[SYS] Caminho Encontrado: ")
        print(grafoAtual.converte_caminho(pathBidirecional[0]))
        print("\n[SYS] Custo: ")
        print(pathBidirecional[1])
        print("\n")
    else: print("\n[SYS] Caminho não encontrado!")

    print("---Custo Uniforme---")

    profilerCustoUniforme = cProfile.Profile()
    profilerCustoUniforme.enable()
    pathCustoUniforme = grafoAtual.procura_custo_uniforme(start, end)
    profilerCustoUniforme.disable()
    if len(pathCustoUniforme[0]) > 0:
        print("\n[SYS] Caminho Encontrado: ")
        print(grafoAtual.converte_caminho(pathCustoUniforme[0]))
        print("\n[SYS] Custo: ")
        print(pathCustoUniforme[1])
        print("\n")
    else: print("\n[SYS] Caminho não encontrado!")

    print("---Procura Iterativa---")
    profilerProcuraIterativa = cProfile.Profile()
    profilerProcuraIterativa.enable()
    pathProcuraIterativa = grafoAtual.procura_iterativa(start, end)
    profilerProcuraIterativa.disable()
    if len(pathProcuraIterativa[0]) > 0:
        print("\n[SYS] Caminho Encontrado: ")
        print(grafoAtual.converte_caminho(pathProcuraIterativa[0]))
        print("\n[SYS] Custo: ")
        print(pathProcuraIterativa[1])
        print("\n")
    else: print("\n[SYS] Caminho não encontrado!")


    print("-----------------------------------------\n" +
          "-----Algoritmos de Procura Informada-----\n" +
          "-----------------------------------------\n")
    grafoAtual.calcula_heuristica_global(end)

    
    print("---Procura A*---")
    profilerAstar = cProfile.Profile()
    profilerAstar.enable()
    pathAstar = grafoAtual.procura_aStar(start, end)
    print(pathAstar)
    profilerAstar.disable()
    if len(pathAstar[0]) > 0:
        print("\n[SYS] Caminho Encontrado: ")
        print(grafoAtual.converte_caminho(pathAstar[0]))
        print("\n[SYS] Custo: ")
        print(pathAstar[1])
        print("\n")
    else: print("\n[SYS] Caminho não encontrado!")

    print("---Greedy---")
    profilerGreedy = cProfile.Profile()
    profilerGreedy.enable()
    pathGreedy = grafoAtual.greedy(start, end)
    profilerGreedy.disable()
    if len(pathGreedy[0]) > 0:
        print("\n[SYS] Caminho Encontrado: ")
        print(grafoAtual.converte_caminho(pathGreedy[0]))
        print("\n[SYS] Custo: ")
        print(pathGreedy[1])
        print("\n")
    else:
        print("\n[SYS] Caminho não encontrado!")

    performance_algoritmos(pathDFS, pathBFS, pathBidirecional, pathCustoUniforme, pathProcuraIterativa, pathGreedy, pathAstar, [profilerDFS, profilerBFS, profilerBidirecional, profilerCustoUniforme, profilerProcuraIterativa, profilerGreedy, profilerAstar])

def seleciona_origem_destino(graph):
    testO1, testO2, testD1, testD2 = str(), str(), str(), str()
    
    print("[SYS] Os pontos de origem e destino são nodos que são representados pela interseção de duas ou mais ruas")
    print("[SYS] O processo de seleção de origem e destino é o seguinte: ")
    print("[SYS] -> Indicar uma rua")
    print("[SYS] -> Indicar outra rua que faça interseção com a original")

    while isinstance(testO1, str):
        ruaOrigem1 = input("[SYS] Indique a rua de origem principal: ")
        testO1 = graph.get_edge_by_name(ruaOrigem1)
        print("\n")
        print(testO1)
        print("\n")

    while isinstance(testO2, str):
        ruaOrigem2  = input("[SYS] Indique a rua que faça interceção com a original de origem: ")
        testO2 = graph.get_edge_by_name(ruaOrigem2)
        print("\n")
        print(testO2)
        print("\n")
    
    intersectionOrigem = graph.get_intersection_node(testO1, testO2)

    while isinstance(testD1, str):
        ruaDestino1 = input("[SYS] Indique a rua de destino principal: ")
        testD1 = graph.get_edge_by_name(ruaDestino1)
        print("\n")
        print(testD1)
        print("\n")

    while isinstance(testD2, str):
        ruaDestino2 = input("[SYS] Indique a rua que faça interceção com a original de destino: ")
        testD2 = graph.get_edge_by_name(ruaDestino2)
        print("\n")
        print(testD2)
        print("\n")

    sleep(2)
    intersectionDetino = graph.get_intersection_node(testD1, testD2)
    os.system('cls')
    start = graph.get_node_by_id(intersectionOrigem)
    end = graph.get_node_by_id(intersectionDetino)
    return start, end

def performance_algoritmos(pathDFS, pathBFS, pathBidirecional, pathCustoUniforme, pathProcuraIterativa, pathAstar, pathGreedy, profiles):
    table = PrettyTable()
    dicionario = dict()
    algoritmos = ['DFS', 'BFS', 'Bidirecional', 'Custo Uniforme', 'Procura Iterativa', 'Greedy', 'A*']
    
    dicionario['Algoritmo'] = algoritmos
    dicionario['Tempo de Execução'] = []
    dicionario['Número de Chamadas de Funções'] = []
    dicionario['Tamanho do Path'] = []
    dicionario['Distância'] = []
    dicionario['Tempo'] = []
    dicionario['Número de Nós Explorados'] = []

    for profile in profiles:
        stats = pstats.Stats(profile)
        tempo = round(stats.total_tt, 2)
        num_calls = stats.total_calls
        dicionario['Tempo de Execução'].append(tempo)
        dicionario['Número de Chamadas de Funções'].append(num_calls)
    
    dicionario['Tamanho do Path'].append(len(pathDFS[0]))
    dicionario['Tamanho do Path'].append(len(pathBFS[0]))
    dicionario['Tamanho do Path'].append(len(pathBidirecional[0]))
    dicionario['Tamanho do Path'].append(len(pathCustoUniforme[0]))
    dicionario['Tamanho do Path'].append(len(pathProcuraIterativa[0]))
    dicionario['Tamanho do Path'].append(len(pathAstar[0]))
    dicionario['Tamanho do Path'].append(len(pathGreedy[0]))

    dicionario['Distância'].append(round(pathDFS[1], 2))
    dicionario['Distância'].append(round(pathBFS[1], 2))
    dicionario['Distância'].append(round(pathBidirecional[1], 2))
    dicionario['Distância'].append(round(pathCustoUniforme[1], 2))
    dicionario['Distância'].append(round(pathProcuraIterativa[1], 2))
    dicionario['Distância'].append(round(pathAstar[1], 2))
    dicionario['Distância'].append(round(pathGreedy[1], 2))

    dicionario['Tempo'].append(round(pathDFS[1]/13.8889, 2))
    dicionario['Tempo'].append(round(pathBFS[1]/13.8889, 2))
    dicionario['Tempo'].append(round(pathBidirecional[1]/13.8889, 2))
    dicionario['Tempo'].append(round(pathCustoUniforme[1]/13.8889, 2))
    dicionario['Tempo'].append(round(pathProcuraIterativa[1]/13.8889, 2))
    dicionario['Tempo'].append(round(pathAstar[1]/13.8889, 2))
    dicionario['Tempo'].append(round(pathGreedy[1]/13.8889, 2))

    dicionario['Número de Nós Explorados'].append(pathDFS[2])
    dicionario['Número de Nós Explorados'].append(pathBFS[2])
    dicionario['Número de Nós Explorados'].append(pathBidirecional[2])
    dicionario['Número de Nós Explorados'].append(pathCustoUniforme[2])
    dicionario['Número de Nós Explorados'].append(pathProcuraIterativa[2])
    dicionario['Número de Nós Explorados'].append(pathAstar[2])
    dicionario['Número de Nós Explorados'].append(pathGreedy[2])
    
    table.field_names = ['Algoritmo', 'Tempo de Execução (s)', 'Número de Chamadas de Funções', 'Tamanho do Path', 'Distância (m)', 'Tempo (s)', 'Número de Nós Explorados']
    for i in range(len(dicionario['Algoritmo'])):
        row = [
            dicionario['Algoritmo'][i],
            dicionario['Tempo de Execução'][i],
            dicionario['Número de Chamadas de Funções'][i],
            dicionario['Tamanho do Path'][i],
            dicionario['Distância'][i],
            dicionario['Tempo'][i],
            dicionario['Número de Nós Explorados'][i]
        ]
        table.add_row(row)  

    print(table) 

    yes = r'(?i)\b(?:yes|y)\b'
    no = r'(?i)\b(?:no|n)\b'
    i = 0
    r = input("Quer ver informação com mais detalhe? (yes/no): ")
    if re.match(yes, r):
        for profile in profiles:
            print(f'---{algoritmos[i]}---')
            profile.print_stats(sort='cumulative')
            i += 1
    elif re.match(no, r): 
        return


if __name__ == "__main__":
    main()

