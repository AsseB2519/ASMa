import os
from time import sleep
import re
import os
import cProfile
from prettytable import PrettyTable
from Produto import Produto

from Graph import Grafo
from Node import Node
import Location
from HealthPlanet import HealthPlanet



def main():
    #print("-----Health Planet-----")


    # # start, end = seleciona_origem_destino(grafoAtual)
    # start = grafoAtualb.get_node_by_id(8321237017)
    # end = grafoAtualb.get_node_by_id(1675798722)
    # grafoAtualb.calcula_heuristica_global(end)
    # print("---Procura A*---")
    # pathAstar = grafoAtualb.procura_aStar(start, end,"bike")
    # if len(pathAstar[0]) > 0:
    #     print("\n[SYS] Caminho Encontrado: ")
    #     print(grafoAtualb.converte_caminho(pathAstar[0]))
    #     print("\n[SYS] Custo: ")
    #     print(pathAstar[1])
    #     print("\n")
    # else:
    #     print("\n[SYS] Caminho não encontrado!")

    # location = "Braga"  # Deixar assim para teste
    # neigh, edges, nodes, neighb, edgesb, nodesb = Location.run(location)
    # grafoAtual = Grafo(nodes, neigh, edges)
    # grafoAtualb = Grafo(nodesb, neighb, edgesb)
    health_planet = HealthPlanet()
    # health_planet.adicionar_grafo("Braga", grafoAtual, grafoAtualb)
    health_planet.adicionar_cliente("sys","sys")
    # health_planet.adicionar_encomenda("a", "Braga", 35, [Produto("b",10),Produto("c",20),Produto("d",5),], grafoAtual.get_node_by_id(8321237017),grafoAtual.get_node_by_id(1675798722),
    #                                   "imediata")
    #
    # health_planet.adicionar_encomenda("b", "Braga", 5, [Produto("h", 1), Produto("j", 1), Produto("l", 3), ],
    #                                   grafoAtual.get_node_by_id(8321237017), grafoAtual.get_node_by_id(5578780754),
    #                                   "imediata")
    health_planet.dafault_estafetas()
    cliente_logado = None  # Variável para rastrear o usuário logado

    while True:
        if cliente_logado is None:
            print("\n=========================================== Health Planet ===============================================")
            print("HealthPlanet.help> 'registo [username] [password]' - Registar um novo utilizador")
            print("HealthPlanet.help> 'login [username] [password]'    - Login de um Utilizador já existente")
            print("=========================================================================================================")

            escolha = input("HealthPlanet.help> ")

            if escolha.startswith('registo'):
                # Processo de registro
                parametros = escolha.split(' ')
                if len(parametros) == 3:
                    nome_usuario = parametros[1]
                    senha = parametros[2]
                    health_planet.adicionar_cliente(nome_usuario, senha)
                else:
                    print("[SYS] Erro: Registo incorreto. Digite 'register [username] [password]'.")

            elif escolha.startswith('login'):
                # Processo de login
                parametros = escolha.split(' ')
                if len(parametros) == 3:
                    nome_usuario = parametros[1]
                    senha = parametros[2]
                    if nome_usuario in health_planet.users and health_planet.users[nome_usuario].password == senha:
                        cliente_logado = nome_usuario
                        print("[SYS] Login bem-sucedido!")
                    else:
                        print("[SYS] Erro: Nome de usuário ou senha incorretos.")
                else:
                    print("[SYS] Erro: Login incorreto. Digite 'login [username] [password]'.")

            else:
                print("[SYS] Erro: Comando inválido.")
        elif cliente_logado == "sys":

                # Menu para o usuário "sys" (sistema)
                print("\n=========================================== Health Planet (System) ======================================")
                print("HealthPlanet.sys_menu> 'gerir_encomendas' - Gerenciar encomendas do sistema")
                print("HealthPlanet.sys_menu> 'logout'            - Logout e voltar ao menu principal")
                print("=============================================================================================================")
                escolha = input("HealthPlanet.sys_menu> ")

                if escolha == 'gerir_encomendas':
                    # Processo de gerenciamento de encomendas pelo sistema
                    while True:
                        print("[SYS] Opções de gerenciamento de encomendas do sistema:")
                        print("1. Visualizar todas as encomendas")
                        print("2. Realizar Simulação de Entregas")

                        opcao = input("[SYS] Escolha uma opção ('exit' para sair): ")

                        if opcao == 'exit':
                            print("[SYS] Gerenciamento de Encomendas Encerrado.")
                            break

                        if opcao == '1':
                            # Visualizar todas as encomendas do sistema
                            todas_encomendas = health_planet.get_todas_encomendas()
                            i=1
                            for encomenda in todas_encomendas:
                                print_encomendas(encomenda, i)
                                i+=1

                        elif opcao == '2':
                            # Atualizar status de todas as encomendas
                            health_planet.gerar_encomendas()

                        else:
                            print("[SYS] Erro: Opção inválida.")

                elif escolha == 'logout':
                    print("[SYS] Logout realizado com sucesso!")
                    cliente_logado = None  # Volta ao estado de nenhum usuário logado

                else:
                    print("[SYS] Erro: Comando inválido.")
        else:
            ents = health_planet.get_entregas_por_avaliar(cliente_logado)
            if len(ents) > 0:
                i = 0
                print("\n=========================================== Health Planet ===============================================")
                for ent in ents:
                    print(f"\n============================================= Entrega {i} =============================================")
                    print("\n")
                    print(f"Id: {ent.getId()}")
                    print(f"Estafeta: {ent.getWorker()}")
                    print(f"Preço: {ent.getPrice()}")
                    print(f"Veículo : {ent.getVehicle()}")
                    print("Lista de Produtos:\n")
                    print("====================================")
                    for produto in ent.getProducts():
                        print(f"\nNome do Produto: {produto.getName()}")
                        print(f"Peso do Produto: {produto.getPeso()}")
                        print(f"Estado da Entrega: {produto.getEstado()}\n")
                    i+=1

                    rating = input("Por favor, introduza uma avaliação desta última entrega entre 0-5 (float): ")
                    cliente = health_planet.users[cliente_logado]
                    health_planet.finalizar_entrega(cliente, ent, rating)
                    health_planet.rating_needed.remove(ent.getId())
            print("=============================================================================================================")

            print("\n=========================================== Health Planet ===============================================")
            print("HealthPlanet.menu> 'nova_encomenda'             - Criar uma nova encomenda")
            print("HealthPlanet.menu> 'ver_encomendas'             - Ver suas encomendas")
            print("HealthPlanet.menu> 'logout'                     - Logout e voltar ao menu principal")
            print("=============================================================================================================")

            escolha = input("HealthPlanet.menu> ")

            if escolha == 'nova_encomenda':
                # Processo de criação de nova encomenda

                localizacao = input("[SYS] Selecione uma cidade (formato: Cidade, País): ")
                if not health_planet.check_if_graph_exists(localizacao):
                    neigh, edges, nodes, neighb, edgesb, nodesb = Location.run(localizacao)
                    grafoAtual = Grafo(nodes, neigh, edges)
                    grafoAtualb = Grafo(nodesb,neighb,edgesb)
                    health_planet.adicionar_grafo(localizacao,grafoAtual,grafoAtualb)

                while True:
                    try:
                        numero_produtos = int(input("[SYS] Digite o número de produtos: "))
                        break  # Saímos do loop se a entrada for um número inteiro
                    except ValueError:
                        print("[SYS] Erro: Digite um número inteiro válido.")

                detalhes_produtos = []
                peso_total = 0
                for _ in range(numero_produtos):
                    nome_produto = input("[SYS] Digite o nome do produto: ")
                    peso_produto = float(input("[SYS] Digite o peso do produto: "))
                    p = Produto(nome_produto,peso_produto,0)
                    peso_total += peso_produto
                    detalhes_produtos.append(p)
                    print("\n")

                urgencia_entrega = "imediata"

                origem, destino = seleciona_origem_destino(grafoAtual)
                print(f"Origem: {origem}")
                print(f"Destino: {destino}")

                if urgencia_entrega not in ['imediata', 'urgente', 'normal', 'irrelevante']:
                    print("[SYS] Erro: Escolha de urgência inválida.")
                else:
                    health_planet.adicionar_encomenda(cliente_logado,localizacao,peso_total,detalhes_produtos,origem,destino,urgencia_entrega)
                    print("[SYS] Encomenda criada com sucesso!")

            elif escolha == 'ver_encomendas':
                encomendas_cliente = health_planet.get_encomendas_cliente(cliente_logado)
                if encomendas_cliente:
                    print("=================================== Escolha uma opção ================================================")
                    print("HealthPlanet.menu.ver_encomendas> 'nao_entregues'        - Ver encomendas ainda não entregues")
                    print("HealthPlanet.menu.ver_encomendas> 'entregues'            - Ver encomendas já entregues")
                    print("======================================================================================================")

                    escolhaEntrega = input("HealthPlanet.menu.ver_encomendas> ")
                    if escolhaEntrega == 'nao_entregues':
                        encs = health_planet.get_encomendas_por_entregar(cliente_logado)
                        i=0
                        if(len(encs)==0):
                            print("Não existem encomendas por entregar!")
                        else:
                            for enc in encs:
                                print_encomendas(enc, i)
                                i+=1
                    elif escolhaEntrega == 'entregues':
                        encs = health_planet.get_encomendas_entregues(cliente_logado)
                        i=0
                        if (len(encs) == 0):
                            print("Nenhuma encomenda foi entregue!")
                        else:
                            for enc in encs:
                                print_encomendas(enc, i)
                                i+=1
                    else:
                        print("[SYS] Erro: Comando inválido.")

                else:
                    print("[SYS] O cliente ainda não possui encomendas.")

            elif escolha == 'logout':
                print("[SYS] Logout realizado com sucesso!")
                cliente_logado = None  # Volta ao estado de nenhum usuário logado

            else:
                print("[SYS] Erro: Comando inválido.")


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
        ruaOrigem2 = input("[SYS] Indique a rua que faça interceção com a original de origem: ")
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
    intersectionDestino = graph.get_intersection_node(testD1, testD2)
    os.system('cls')
    start = graph.get_node_by_id(intersectionOrigem)
    end = graph.get_node_by_id(intersectionDestino)
    return start, end

def print_encomendas(encomenda, i):
    print(f"\n=========================================== Encomenda {i} ===========================================")
    print(f"Id: {encomenda.id}")
    print(f"Cliente: {encomenda.client}")
    print(f"Localização: {encomenda.getLocalizacao()}")
    print(f"Destino: {encomenda.getDestino()}")
    print(f"Urgência de Entrega: {encomenda.delivery_time}")
    print(f"Peso Total: {encomenda.weight}")
    print("Lista de Produtos:")
    print("====================================")
    for produto in encomenda.getGoods():
        print(f"\nNome do Produto: {produto.name}")
        print(f"Peso do Produto: {produto.peso}")
        if(produto.entregue):
            print(f"Estado da Entrega: Entregue")
        else:
            print(f"Estado da Entrega: Em Distribuição")
    print("====================================")
    if (encomenda.entregue):
        print(f"Estado da Encomenda: Entregue")
    else:
        print(f"Estado da Encomenda: Em distribuição")
    print("=========================================================================================================")


if __name__ == "__main__":
    main()
