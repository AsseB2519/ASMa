import math
import time
import config
from Classes import Location
from Classes import Node
from Classes import Graph
from Classes import Location
from spade.message import Message
from spade.behaviour import CyclicBehaviour
import jsonpickle

class Transport_Behav(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=20)
        if msg:
            performative = msg.get_metadata("performative")
            if performative == "purchase":
                purchase = jsonpickle.decode(msg.body)
                self.agent.deliveries.append(purchase)

                # Calculate the total weight of all scheduled deliveries
                total_weight = sum([d.getWeight() for d in self.agent.deliveries])
                max_capacity = {'bike': 5, 'motorbike': 10, 'car': 15}[self.agent.vehicle_type]
                threshold_weight = 0.75 * max_capacity  # 75% of the maximum capacity

                # Only proceed if the total weight reaches at least 75% of the vehicle's capacity
                if total_weight >= threshold_weight: # and total_weight < max_capacity
                    self.agent.available = False
                    for delivery in self.agent.deliveries:
                        client_jid = delivery.getAgent()
                        loc = delivery.getPosition()
                        x_dest = loc.getX()
                        y_dest = loc.getY()
                        node_dest = loc.getNode()

                        x_ori = self.agent.position.getX()
                        y_ori = self.agent.position.getY()
                        node_origem = self.agent.position.getNode()
                        
                        # print(node_origem)
                        # location = "Braga"  
                        # neigh, edges, nodes, neighb, edgesb, nodesb = Location.run(location)
                        print("Calculating the path...")
                        # grafoAtual = Graph.Grafo(config.NODES, config.NEIGH, config.EDGES)
                        # grafoAtual = Graph.Grafo(nodes, neigh, edges)
                        # grafoAtualb = Graph.Grafo(config.NODESB, config.NEIGHB, config.EDGESB)
                        # grafoAtualb = Graph.Grafo(nodesb, neighb, edgesb)
                        start = config.GRAPH.get_node_by_id(node_origem)
                        dest = config.GRAPH.get_node_by_id(node_dest)
                        config.GRAPH.calcula_heuristica_global(dest)
                        pathAstar = config.GRAPH.procura_aStar(start, dest, "car")
                        caminhoCarroMota = config.GRAPH.converte_caminho(pathAstar[0])
                        print(pathAstar)
                        # custoCarro = pathAstar[1][2]
                        # custoMota = pathAstar[1][1]
                        # tempoCarro = pathAstar[2][1]  
                        distancia=0
                        tempo=0
                        print("veiculo type" + self.agent.vehicle_type)
                        if self.agent.vehicle_type == "bike":
                            pass
                        elif self.agent.vehicle_type == "car":
                            distancia = pathAstar[1][0]
                            tempo = pathAstar[2][2]
                        elif self.agent.vehicle_type == "motorbike":
                            distancia = pathAstar[1][0]
                            tempo = pathAstar[2][1]
                            pass

                        print(tempo)
                        print(distancia)

                        # print(caminhoCarroMota)
                        # print(custoCarro)
                        # print(custoMota)
                        
                        if not caminhoCarroMota:
                            print("Same Destination")
                            time.sleep(1)
                        else:  
                            print("Trip: " + " ----> ".join(caminhoCarroMota))
                            time.sleep(1)

                        self.agent.position.setX(x_dest)
                        self.agent.position.setY(y_dest)
                        self.agent.position.setNode(node_dest)

                        msg = Message(to=client_jid)
                        msg.body = "Delivery"
                        msg.set_metadata("performative", "delivery")

                        print("Deliveryman {} delivered the package weighing {:.2f} to Client {}".format(str(self.agent.jid), delivery.getWeight(), str(client_jid)))
                        await self.send(msg)

                    # location = "Braga"  
                    # neigh, edges, nodes, neighb, edgesb, nodesb = Location.run(location)
                    print("Calculating the path...")
                    start = config.GRAPH.get_node_by_id(self.agent.position.getNode())
                    dest = config.GRAPH.get_node_by_id(config.WAREHOUSE)
                    config.GRAPH.calcula_heuristica_global(dest)
                    pathAstar = config.GRAPH.procura_aStar(start, dest, "car")
                    caminhoCarroMota = config.GRAPH.converte_caminho(pathAstar[0])
                    custoCarro = pathAstar[1][2]
                    custoMota = pathAstar[1][1]
    
                    print("Trip: " + " ----> ".join(caminhoCarroMota))
                    time.sleep(1)

                    msg = Message(to=self.agent.get("deliveryman_contact"))
                    msg.body = jsonpickle.encode(self.agent.deliveries)
                    msg.set_metadata("performative", "confirmation_delivery")

                    print("Deliveryman {}".format(str(self.agent.jid)) + " has confirmed the delivery of all the package(s) to DeliveryManager {}".format(self.agent.get("deliveryman_contact")))
                    await self.send(msg)    

                    self.agent.position.setX(int(config.WAREHOUSE_X))
                    self.agent.position.setY(int(config.WAREHOUSE_Y))
                    self.agent.position.setNode(config.WAREHOUSE)
                    self.agent.available = True
                    self.agent.deliveries.clear()

                else: print("Waiting for more purchases! Weight: {:.2f} vs Min Capacity: {:.2f}".format(total_weight, threshold_weight))

            elif performative == "return":
                ret = jsonpickle.decode(msg.body)
                self.agent.deliveries.append(ret)
                products = ret.getProducts()

                total_products = 0
                for delivery in self.agent.deliveries:
                    products = delivery.getProducts()
                    for _, quantity in products:
                        total_products += quantity

                if total_products >= 5:
                    self.agent.available = False
                    for delivery in self.agent.deliveries:
                        client_jid = delivery.getAgent()
                        loc = delivery.getPosition()
                        x_dest = loc.getX()
                        y_dest = loc.getY()
                        node_dest = loc.getNode()

                        x_ori = self.agent.position.getX()
                        y_ori = self.agent.position.getY()
                        node_origem = self.agent.position.getNode()
                        
                        # print(node_origem)
                        # location = "Braga"  
                        # neigh, edges, nodes, neighb, edgesb, nodesb = Location.run(location)
                        print("Calculating the path...")
                        # grafoAtual = Graph.Grafo(config.NODES, config.NEIGH, config.EDGES)
                        # grafoAtual = Graph.Grafo(nodes, neigh, edges)
                        # grafoAtualb = Graph.Grafo(config.NODESB, config.NEIGHB, config.EDGESB)
                        # grafoAtualb = Graph.Grafo(nodesb, neighb, edgesb)
                        start = config.GRAPH.get_node_by_id(node_origem)
                        dest = config.GRAPH.get_node_by_id(node_dest)
                        config.GRAPH.calcula_heuristica_global(dest)
                        pathAstar = config.GRAPH.procura_aStar(start, dest, "car")
                        caminhoCarroMota = config.GRAPH.converte_caminho(pathAstar[0])
                        custoCarro = pathAstar[1][2]
                        custoMota = pathAstar[1][1]
                        # print(caminhoCarroMota)
                        # print(custoCarro)
                        # print(custoMota)
                        
                        if not caminhoCarroMota:
                            print("Same Destination")
                            time.sleep(1)
                        else:  
                            print("Trip: " + " ----> ".join(caminhoCarroMota))
                            time.sleep(1)

                        self.agent.position.setX(x_dest)
                        self.agent.position.setY(y_dest)
                        self.agent.position.setNode(node_dest)

                        msg = Message(to=client_jid)
                        msg.body = "Refund" 
                        msg.set_metadata("performative", "refund")

                        # print("Agent {}:".format(str(self.agent.jid)) + " Client Agent delivered the refund products to Deliveryman Agent {}".format(str(client_jid)))
                        await self.send(msg)   

                    # location = "Braga"  
                    # neigh, edges, nodes, neighb, edgesb, nodesb = Location.run(location)
                    print("Calculating the path...")
                    start = config.GRAPH.get_node_by_id(self.agent.position.getNode())
                    dest = config.GRAPH.get_node_by_id(config.WAREHOUSE)
                    config.GRAPH.calcula_heuristica_global(dest)
                    pathAstar = config.GRAPH.procura_aStar(start, dest, "car")
                    caminhoCarroMota = config.GRAPH.converte_caminho(pathAstar[0])
                    custoCarro = pathAstar[1][2]
                    custoMota = pathAstar[1][1]

                    print("Trip: " + " ----> ".join(caminhoCarroMota))
                    time.sleep(1)

                    msg = Message(to=self.agent.get("deliveryman_contact"))
                    msg.body = jsonpickle.encode(self.agent.deliveries)
                    msg.set_metadata("performative", "confirmation_delivery")

                    print("Deliveryman {}".format(str(self.agent.jid)) + " has confirmed the return of all the package(s) to DeliveryManager {}".format(self.agent.get("deliveryman_contact")))
                    await self.send(msg)    

                    self.agent.position.setX(int(config.WAREHOUSE_X))
                    self.agent.position.setY(int(config.WAREHOUSE_Y))
                    self.agent.position.setNode(config.WAREHOUSE)
                    self.agent.available = True
                    self.agent.deliveries.clear()

                else: print("Waiting for more returns! Atual: {total_products} vs Min Capacity: 5")

            else:
                print(f"Agent {self.agent.jid}: Message not understood!")

        # else:
        #     print(f"Agent {self.agent.jid}: Did not receive any message after 10 seconds")
