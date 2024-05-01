from Graph import Grafo
from Node import Node


class FileToGraph:
    def __init__(self, file_path):
        self.file_path = file_path
        self.node_id_counter = 1  # Inicia o contador de id em 1

    def create_graph_from_file(self):
        with open(self.file_path, 'r') as file:
            lines = file.readlines()

        graph = Grafo()

        for line in lines:
            parts = line.split('[')
            if len(parts) < 2:
                continue

            # Extrair nome
            name = parts[0].strip()

            # Extrair os vizinhos como uma lista de tuplos (vizinho, custo)
            neighbors_part = parts[1].split(']')[0]
            neighbors = [tuple(pair.strip().lstrip('(').rstrip(')').split(',')) for pair in neighbors_part.split(')(')]

            # Extrair o tamanho da rua de origem (último número na linha)
            street_length = int(line.split()[-1])

            # Corrigir os custos para não aparecerem entre aspas
            neighbors = [(neighbor, int(cost.strip("'"))) for neighbor, cost in neighbors]

            # Adicionar o nodo e suas arestas ao grafo
            graph.add_edge(self.node_id_counter, name.strip('"'), neighbors, street_length)

            # Incrementar o contador de ID
            self.node_id_counter += 1

        return graph
    