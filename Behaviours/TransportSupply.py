import random
import jsonpickle
import config
import time
import math
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from Classes import Graph
from Classes import Location

class TransportSupply_Behav(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=100) 
        if msg:
            performative = msg.get_metadata("performative")
            stockmanager = str(msg.sender)
            if performative == "supply":
                supply = jsonpickle.decode(msg.body)

                x_dest = config.SUPPLIER_X
                y_dest = config.SUPPLIER_Y
                node_dest = config.SUPPLIER

                x_ori = self.agent.position.getX()
                y_ori = self.agent.position.getY()
                node_origem = self.agent.position.getNode()

                print("Calculating the path to SupplierWarehouse...")
                start_time = time.time()

                start = config.GRAPH.get_node_by_id(node_origem)
                dest = config.GRAPH.get_node_by_id(node_dest)
                config.GRAPH.calcula_heuristica_global(dest)
                pathAstar = config.GRAPH.procura_aStar(start, dest, "car")
                caminhoCarroMota = config.GRAPH.converte_caminho(pathAstar[0])
                distancia = pathAstar[1][0]
                tempo = pathAstar[2][2]

                elapsed_time = time.time() - start_time
                if not caminhoCarroMota:
                    print("Same Destination")
                    time.sleep(2)
                else:  
                    # print("elapsed_time " + str(elapsed_time))
                    minutes = int(tempo // 60)
                    seconds = tempo % 60
                    print("Time: {} minutes {:.0f} seconds".format(minutes, seconds))
                    distance_km = distancia / 1000
                    print("Distance: {:.2f} kilometers".format(distance_km))
                    print("Supplier Trip: Warehouse ----> " + " ----> ".join(caminhoCarroMota) + " -----> SupplierWarehouse")
                    dormir = tempo - elapsed_time
                    # print("dormir " + str(dormir))

                    if dormir > 0:
                        time.sleep(2)
                    else:
                        time.sleep(2)

                self.agent.position.setX(config.SUPPLIER_X)
                self.agent.position.setY(config.SUPPLIER_Y)
                self.agent.position.setNode(config.SUPPLIER)

                bool = True
                for p in supply:
                    current_quantity = p.get_quantity()
                    max_quantity = p.get_max_quantity()
                    
                    # Decide whether to set to max quantity with a higher probability
                    if random.random() < 0.80:  # 80% chance to set to max quantity
                        new_quantity = max_quantity
                    else:
                        # 20% chance to set to a random quantity between current and max
                        bool = False
                        new_quantity = random.randint(current_quantity, max_quantity)

                    p.set_quantity(new_quantity)
                    
                if bool == False:
                    msg = Message(to=stockmanager)
                    msg.body = jsonpickle.encode(supply)
                    msg.set_metadata("performative", "supplier_propose")

                    print("Supplier {}".format(str(self.agent.jid)) + " proposed different Stock to StockManager " + str(stockmanager))
                    await self.send(msg)
                
                else: 
                    x_ori = self.agent.position.getX()
                    y_ori = self.agent.position.getY()
                    node_origem = self.agent.position.getNode()

                    x_dest = config.WAREHOUSE_X
                    y_dest = config.WAREHOUSE_Y
                    node_dest = config.WAREHOUSE
                    
                    caminhoCarroMota2 = None
                    print("Calculating the path to Warehouse...")
                    start_time = time.time()
                    start = config.GRAPH.get_node_by_id(node_origem)
                    dest = config.GRAPH.get_node_by_id(node_dest)
                    config.GRAPH.calcula_heuristica_global(dest)
                    pathAstar = config.GRAPH.procura_aStar(start, dest, "car")
                    caminhoCarroMota2 = config.GRAPH.converte_caminho(pathAstar[0])
                    distancia = pathAstar[1][0]
                    tempo = pathAstar[2][2]

                    elapsed_time = time.time() - start_time
                    if not caminhoCarroMota2:
                        print("Same Destination")
                        time.sleep(2)
                    else:  
                        # print("elapsed_time " + str(elapsed_time))
                        minutes = int(tempo // 60)
                        seconds = tempo % 60
                        print("Time: {} minutes {:.0f} seconds".format(minutes, seconds))
                        distance_km = distancia / 1000
                        print("Distance: {:.2f} kilometers".format(distance_km))
                        print("Supplier Trip: SupplierWarehouse ----> " + " ----> ".join(caminhoCarroMota2) + " -----> Warehouse")
                        dormir = tempo - elapsed_time
                        # print("dormir " + str(dormir))

                        if dormir > 0:
                            time.sleep(2)
                        else:
                            time.sleep(2)
                                    
                    self.agent.position.setX(config.WAREHOUSE_X)
                    self.agent.position.setY(config.WAREHOUSE_Y)
                    self.agent.position.setNode(config.WAREHOUSE)

                    msg = Message(to=str(stockmanager))
                    msg.body = jsonpickle.encode(supply)          
                    msg.set_metadata("performative", "supply")

                    # print("Supplier {}".format(str(self.agent.jid)) + " supplied stock to StockManager " + str(stockmanager))
                    await self.send(msg)

            elif performative == "accept_proposal":
                supply = jsonpickle.decode(msg.body)

                x_ori = self.agent.position.getX()
                y_ori = self.agent.position.getY()
                node_origem = self.agent.position.getNode()

                x_dest = config.WAREHOUSE_X
                y_dest = config.WAREHOUSE_Y
                node_dest = config.WAREHOUSE

                caminhoCarroMota3 = None
                print("Calculating the path to Warehouse...")
                start_time = time.time()
                start = config.GRAPH.get_node_by_id(node_origem)
                dest = config.GRAPH.get_node_by_id(node_dest)
                config.GRAPH.calcula_heuristica_global(dest)
                pathAstar = config.GRAPH.procura_aStar(start, dest, "car")
                caminhoCarroMota3 = config.GRAPH.converte_caminho(pathAstar[0])
                distancia = pathAstar[1][0]
                tempo = pathAstar[2][2]

                elapsed_time = time.time() - start_time
                if not caminhoCarroMota3:
                    print("Same Destination")
                    time.sleep(2)
                else:  
                    # print("elapsed_time " + str(elapsed_time))
                    minutes = int(tempo // 60)
                    seconds = tempo % 60
                    print("Time: {} minutes {:.0f} seconds".format(minutes, seconds))
                    distance_km = distancia / 1000
                    print("Distance: {:.2f} kilometers".format(distance_km))
                    print("Supplier Trip: SupplierWarehouse ----> " + " ----> ".join(caminhoCarroMota3) + " -----> Warehouse")
                    dormir = tempo - elapsed_time
                    # print("dormir " + str(dormir))

                    if dormir > 0:
                        time.sleep(2)
                    else:
                        time.sleep(2)

                self.agent.position.setX(config.WAREHOUSE_X)
                self.agent.position.setY(config.WAREHOUSE_Y)
                self.agent.position.setNode(config.WAREHOUSE)

                msg = Message(to=str(stockmanager))
                msg.body = jsonpickle.encode(supply)          
                msg.set_metadata("performative", "supply")

                # print("Supplier {}".format(str(self.agent.jid)) + " supplied stock to StockManager " + str(stockmanager))
                await self.send(msg)

            elif performative == "reject_proposal":
                x_ori = self.agent.position.getX()
                y_ori = self.agent.position.getY()
                node_origem = self.agent.position.getNode()

                x_dest = config.WAREHOUSE_X
                y_dest = config.WAREHOUSE_Y
                node_dest = config.WAREHOUSE

                caminhoCarroMota4 = None
                print("Calculating the path to Warehouse...")
                start_time = time.time()
                start = config.GRAPH.get_node_by_id(node_origem)
                dest = config.GRAPH.get_node_by_id(node_dest)
                config.GRAPH.calcula_heuristica_global(dest)
                pathAstar = config.GRAPH.procura_aStar(start, dest, "car")
                caminhoCarroMota4 = config.GRAPH.converte_caminho(pathAstar[0])
                distancia = pathAstar[1][0]
                tempo = pathAstar[2][2]

                elapsed_time = time.time() - start_time
                if not caminhoCarroMota4:
                    print("Same Destination")
                    time.sleep(2)
                else:  
                    # print("elapsed_time " + str(elapsed_time))
                    minutes = int(tempo // 60)
                    seconds = tempo % 60
                    print("Time: {} minutes {:.0f} seconds".format(minutes, seconds))
                    distance_km = distancia / 1000
                    print("Distance: {:.2f} kilometers".format(distance_km))
                    print("Supplier Trip: SupplierWarehouse ----> " + " ----> ".join(caminhoCarroMota4) + " -----> Warehouse")
                    dormir = tempo - elapsed_time
                    # print("dormir " + str(dormir))

                    if dormir > 0:
                        time.sleep(2)
                    else:
                        time.sleep(2)

                self.agent.position.setX(config.WAREHOUSE_X)
                self.agent.position.setY(config.WAREHOUSE_Y)
                self.agent.position.setNode(config.WAREHOUSE)

                print("Supplier {}".format(str(self.agent.jid)) + " is back to the Warehouse without Products")
            else:
                print(f"Agent {self.agent.jid}: Message not understood!")                       