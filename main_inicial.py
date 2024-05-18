import time
import config
from Classes import Graph
from spade import quit_spade
from Classes import Location
from MainPage import main_menu

from Agents.Client import ClientAgent
from Agents.Deliveryman import DeliverymanAgent
from Agents.StockManager import StockManagerAgent
from Agents.DeliverymanManager import DeliverymanManagerAgent
from Agents.Supplier import SupplierAgent

import tkinter as tk
import streamlit as st

XMPP_SERVER = 'laptop-ci4qet97'
PASSWORD = 'NOPASSWORD'

if __name__ == '__main__':

    # main_menu()
    # config.LOCATION = config.get_string_input("Enter the Location: ")

    config.LOCATION = "Sabrosa"
    config.CLIENTS = 1
    config.DELIVERYMAN = 2
    MAX_CLIENTS = config.CLIENTS
    MAX_DELIVERYMAN = config.DELIVERYMAN

    print("Calculating the Graph...")
    neigh, edges, nodes, neighb, edgesb, nodesb = Location.run(config.LOCATION)

    config.NEIGH = neigh
    config.EDGES = edges
    config.NODES = nodes
    config.NEIGHB = neighb
    config.EDGESB = edgesb
    config.NODESB = nodesb

    config.GRAPH = Graph.Grafo(config.NODES, config.NEIGH, config.EDGES)
    config.GRAPH_BIKE = Graph.Grafo(config.NODESB, config.NEIGHB, config.EDGESB)

    config.SUPPLIER = config.random_node_selection(config.FILE_PATH)
    config.WAREHOUSE = config.random_node_selection(config.FILE_PATH)

    deliverymanmanager_jid = 'deliverymanmanager@' + XMPP_SERVER
    deliverymanmanager_agent = DeliverymanManagerAgent(deliverymanmanager_jid, PASSWORD)

    res_deliverymanmanager = deliverymanmanager_agent.start(auto_register=True)
    res_deliverymanmanager.result()

    supplier_jid = 'supplier@' + XMPP_SERVER
    supplier_agent = SupplierAgent(supplier_jid, PASSWORD)

    res_supplier = supplier_agent.start(auto_register=True)
    res_supplier.result()

    stockmanager_jid = 'stockmanager@' + XMPP_SERVER
    stockmanager_agent = StockManagerAgent(stockmanager_jid, PASSWORD)

    stockmanager_agent.set('deliveryman_contact', deliverymanmanager_jid)
    stockmanager_agent.set('supplier_contact', supplier_jid)

    res_stockmanager = stockmanager_agent.start(auto_register=True)
    res_stockmanager.result() 

    deliverymanmanager_agent.set('stock_contact', stockmanager_jid)

    client_list = []
    deliveryman_list = []

    time.sleep(1)

    for i in range(1, MAX_DELIVERYMAN + 1):
        deliveryman_jid = 'deliveryman{}@'.format(str(i)) + XMPP_SERVER
        deliveryman_agent = DeliverymanAgent(deliveryman_jid, PASSWORD)

        deliveryman_agent.set('deliveryman_contact', deliverymanmanager_jid)

        res_deliveryman = deliveryman_agent.start(auto_register=True)
        res_deliveryman.result()
        deliveryman_list.append(deliveryman_agent)

    time.sleep(1)

    for i in range(1, MAX_CLIENTS + 1):

        # Sleep 1 second for each x=10 Client agents added
        # if i % 10 == 0:
            # time.sleep(1)

        client_jid = 'client{}@'.format(str(i)) + XMPP_SERVER
        client_agent = ClientAgent(client_jid, PASSWORD)

        client_agent.set('stockmanager_contact', stockmanager_jid)

        res_client = client_agent.start(auto_register=True)
        res_client.result()
        client_list.append(client_agent)

    while stockmanager_agent.is_alive() and deliveryman_agent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            for client_agent in client_list:
                client_agent.stop()

            for deliveryman_agent in deliveryman_list:
                deliveryman_agent.stop()
            break
    print('Agents finished')

    quit_spade()