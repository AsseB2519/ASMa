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
        msg = await self.receive(timeout=20) 
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

                # location = "Braga"  
                # neigh, edges, nodes, neighb, edgesb, nodesb = Location.run(location)
                print("Calculating the path...")
                grafoAtual = Graph.Grafo(config.NODES, config.NEIGH, config.EDGES)
                # grafoAtual = Graph.Grafo(nodes, neigh, edges)
                grafoAtualb = Graph.Grafo(config.NODESB, config.NEIGHB, config.EDGESB)
                # grafoAtualb = Graph.Grafo(nodesb, neighb, edgesb)
                start = grafoAtual.get_node_by_id(node_origem)
                dest = grafoAtual.get_node_by_id(node_dest)
                grafoAtual.calcula_heuristica_global(dest)
                pathAstar = grafoAtual.procura_aStar(start, dest, "car")
                caminhoCarroMota = grafoAtual.converte_caminho(pathAstar[0])
                custoCarro = pathAstar[1][2]
                # custoMota = pathAstar[1][1]
                # print(caminhoCarroMota)
                # print(custoCarro)
                # print(custoMota)

                print("Supplier Trip: Warehouse ----> " + " ----> ".join(caminhoCarroMota) + " ----> SupplyWarehouse")
                time.sleep(1)

                # Modify the quantity with a higher probability of being the maximum
                for p in supply:
                    current_quantity = p.get_quantity()
                    max_quantity = p.get_max_quantity()
                    
                    # Decide whether to set to max quantity with a higher probability
                    if random.random() < 0.8:  # 80% chance to set to max quantity
                        new_quantity = max_quantity
                    else:
                        # 20% chance to set to a random quantity between current and max
                        new_quantity = random.randint(current_quantity, max_quantity)
                    
                    p.set_quantity(new_quantity)
                    # print(current_quantity)
                    # print(new_quantity)

                x_dest = config.WAREHOUSE_X
                y_dest = config.WAREHOUSE_Y
                node_dest = config.WAREHOUSE

                self.agent.position.setX(config.SUPPLIER_X)
                self.agent.position.setY(config.SUPPLIER_Y)
                self.agent.position.setNode(config.SUPPLIER)

                print("Calculating the path...")
                start = grafoAtual.get_node_by_id(self.agent.position.getNode())
                dest = grafoAtual.get_node_by_id(node_dest)
                grafoAtual.calcula_heuristica_global(dest)
                pathAstar = grafoAtual.procura_aStar(start, dest, "car")
                caminhoCarroMota = grafoAtual.converte_caminho(pathAstar[0])
                custoCarro = pathAstar[1][2]
                # custoMota = pathAstar[1][1]
                # print(caminhoCarroMota)
                # print(custoCarro)
                # print(custoMota)
                                
                print("Supplier Trip: SupplyWarehouse  ----> " + " ----> ".join(caminhoCarroMota) + " -----> Warehouse")   
                time.sleep(1)

                msg = Message(to=str(stockmanager))
                msg.body = jsonpickle.encode(supply)          
                msg.set_metadata("performative", "supply")

                # print("Supplier {}".format(str(self.agent.jid)) + " supplied stock to StockManager " + str(stockmanager))
                await self.send(msg)
            
            else:
                print(f"Agent {self.agent.jid}: Message not understood!")                       