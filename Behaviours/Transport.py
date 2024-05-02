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
                threshold_weight = 0.7 * max_capacity  # 70% of the maximum capacity

                # Only proceed if the total weight reaches at least 80% of the vehicle's capacity
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
                        location = "Braga"  
                        neigh, edges, nodes, neighb, edgesb, nodesb = Location.run(location)
                        grafoAtual = Graph.Grafo(nodes, neigh, edges)
                        grafoAtualb = Graph.Grafo(nodesb, neighb, edgesb)
                        start = grafoAtual.get_node_by_id(node_origem)
                        dest = grafoAtual.get_node_by_id(node_dest)
                        grafoAtual.calcula_heuristica_global(dest)
                        pathAstar = grafoAtual.procura_aStar(start, dest, "car")
                        caminhoCarroMota = grafoAtual.converte_caminho(pathAstar[0])
                        custoCarro = pathAstar[1][2]
                        custoMota = pathAstar[1][1]
                        print(caminhoCarroMota)
                        print(custoCarro)
                        print(custoMota)

                        distance = math.sqrt((x_dest - x_ori)**2 + (y_dest - y_ori)**2)

                        trip = distance / 10
                        time.sleep(1)
                        
                        self.agent.position.setX(x_dest)
                        self.agent.position.setY(y_dest)

                        msg = Message(to=client_jid)
                        msg.body = "Delivery"
                        msg.set_metadata("performative", "delivery")

                        print("Agent {}:".format(str(self.agent.jid)) + " Deliveryman Agent delivered the package to Client Agent {}".format(str(client_jid)))
                        await self.send(msg)

                    msg = Message(to=self.agent.get("deliveryman_contact"))
                    msg.body = jsonpickle.encode(self.agent.deliveries)
                    msg.set_metadata("performative", "confirmation_delivery")

                    print("Agent {}:".format(str(self.agent.jid)) + " Deliveryman Agent has confirmed the delivery of the package to DeliveryManager Agent {}".format(self.agent.get("deliveryman_contact")))
                    await self.send(msg)    

                    # print("Trip 2")
                    time.sleep(1)

                    self.agent.position.setX(int(config.WAREHOUSE_X))
                    self.agent.position.setY(int(config.WAREHOUSE_Y))
                    self.agent.available = True
                    self.agent.deliveries.clear()

                else: print("Waiting for more purchases! Weight: " + str(total_weight) + " vs Max Capacity: " + str(max_capacity))

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

                        x_ori = self.agent.position.getX()
                        y_ori = self.agent.position.getY()
                        distance = math.sqrt((x_dest - x_ori)**2 + (y_dest - y_ori)**2)

                        trip = distance / 10
                        time.sleep(1)
                        
                        self.agent.position.setX(x_dest)
                        self.agent.position.setY(y_dest)

                        # msg = Message(to=client_jid)
                        # msg.body = "Refund" 
                        # msg.set_metadata("performative", "refund")

                        # print("Agent {}:".format(str(self.agent.jid)) + " Client Agent delivered the refund products to Deliveryman Agent {}".format(str(client_jid)))
                        # await self.send(msg)   

                    time.sleep(1)  

                    self.agent.position.setX(int(config.WAREHOUSE_X))
                    self.agent.position.setY(int(config.WAREHOUSE_Y))

                    msg = Message(to=self.agent.get("deliveryman_contact"))
                    msg.body = jsonpickle.encode(self.agent.deliveries)
                    msg.set_metadata("performative", "confirmation_refund")

                    # print("Agent {}:".format(str(self.agent.jid)) + " Deliveryman Agent has confirmed the delivery of the package to DeliverymanManager Agent {}".format(self.agent.get("deliveryman_contact")))
                    await self.send(msg)   
                
                    self.agent.available = True 

                    self.agent.deliveries.clear()
                    
                else: print("Waiting for more returns!")

            else:
                print(f"Agent {self.agent.jid}: Message not understood!")

        # else:
        #     print(f"Agent {self.agent.jid}: Did not receive any message after 10 seconds")
