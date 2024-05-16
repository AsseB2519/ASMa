import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import random
from Node_Aux import Node
from Node_Aux import Positions
from Ruas_Aux import Ruas
import json


def create_neighborhood_dict(graph):
    neighborhood_dict = {}

    for u, v, k, data in graph.edges(keys=True, data=True):

        if u not in neighborhood_dict.keys():
            neighborhood_dict[u] = [(v, data['length'], k)]
        elif (v, data['length'], k) not in neighborhood_dict[u]:
            neighborhood_dict[u].append((v, data['length'], k))
        """
        if not data.get('oneway', True):
            if v not in neighborhood_dict:
                neighborhood_dict[v] = [(u, data['length'], k)]
            elif (u, data['length'], k) not in neighborhood_dict[v]:  # Check if the reverse edge is already added
                neighborhood_dict[v].append((u, data['length'], k))"""

    return neighborhood_dict


def create_nodes_list(graph):
    list = []

    for node, data in graph.nodes(data=True):
        id = node
        x = data["x"]
        y = data["y"]
        pos = Positions(x, y)
        street_count = data["street_count"]

        nodo = Node(id, pos, street_count)
        if nodo not in list:
            list.append(nodo)

    return list


def randomizacao_de_cortadas_transito(name, origem, destino, oneway, highway, rotunda, ponte, tunnel, access, vel,
                                      length, ref):
    random1 = 2  # random.randint(0,9) para teste
    random2 = 2  # random.randint(0,9)

    if (random1 == 1):
        rua = Ruas(name, origem, destino, oneway, highway, rotunda, ponte, tunnel, access, vel, length, ref, True,
                   False)
    elif (random2 == 1):
        rua = Ruas(name, origem, destino, oneway, highway, rotunda, ponte, tunnel, access, vel, length, ref, False,
                   True)
    else:
        rua = Ruas(name, origem, destino, oneway, highway, rotunda, ponte, tunnel, access, vel, length, ref)
    return rua


def create_edges_list(graph):
    edges = []

    for u, v, k, data in graph.edges(keys=True, data=True):
        name = data.get('name', "")
        origem = u
        destino = v

        oneway = data.get('oneway', False)
        highway = data.get('highway', [])
        rotunda = data.get('junction', [])
        ref = data.get('ref', False)
        ponte = data.get('bridge', False)
        tunnel = 'tunnel' in data  # Não faz sentido ser aqui data.get("tunnel", False) (vai buscar o value em que tunnel é key ou se não houver põe False)
        access = data.get('access', [])
        vel = data.get('maxspeed', [])
        length = data.get('length', 0)

        if isinstance(highway, str):
            highway = [highway]

        if isinstance(vel, str):
            vel = [vel]

        rua = randomizacao_de_cortadas_transito(name, origem, destino, oneway, highway, rotunda, ponte, tunnel, access,
                                                vel, length, ref)
        edges.append(rua)

    return edges


def run(location):
    # Download the street network
    G = ox.graph_from_place(location, network_type="drive")

    # Convert the graph to a Pandas DataFrame
    edges = ox.graph_to_gdfs(G, nodes=False, edges=True)

    # Filter edges with a valid 'name' key
    G_filtered = G.copy()

    for node, data in G_filtered.nodes(data=True):
        data.pop('name', None)
        data.pop('length', None)
        data.pop('highway', None)
        data.pop('ref', None)

    for u, v, k, data in G_filtered.edges(keys=True, data=True):
        if data.get('junction') != 'roundabout' and data.get('name') is None:
            data.pop('osmid', None)
            data.pop('reversed', None)
            data.pop('geometry', None)
            # data.pop('ref', None)
            data.pop('lanes', None)
        else:
            data.pop('highway', None)
            data.pop('osmid', None)
            data.pop('reversed', None)
            data.pop('geometry', None)
            # data.pop('ref', None)
            data.pop('lanes', None)

    name_counter = {}
    for u, v, k, data in G_filtered.edges(keys=True, data=True):
        name = data.get('name')
        if name is not None:
            name_key = str(name)
            if name_key in name_counter:
                name_counter[name_key] += 1
                data['name'] = f"{name} ({name_counter[name_key]})"
            else:
                name_counter[name_key] = 1

    neighb = create_neighborhood_dict(G_filtered)
    edgesList = create_edges_list(G_filtered)
    nodeList = create_nodes_list(G_filtered)

    return neighb, edgesList, nodeList
