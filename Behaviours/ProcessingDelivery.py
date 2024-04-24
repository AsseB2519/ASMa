import random
import jsonpickle
from spade.behaviour import CyclicBehaviour
from spade.message import Message

from Classes.Purchase import Purchase
from Classes.Delivery import Delivery

class ProcessingDelivery_Behav(CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=10) 
        if msg:
            # Message Threatment based on different Message performatives
            performative = msg.get_metadata("performative")
            if performative == "request":
                request = jsonpickle.decode(msg.body)

                if isinstance(request, Purchase):
                    client_jid = request.getAgent()
                    loc = request.getInit()
                    products = request.getProducts()

                    # Initialize the total weight of the order
                    total_weight = 0

                    # Calculate the total weight of the order
                    for product_id, quantity in products:
                        if product_id in self.agent.products:
                            weight = self.agent.products[product_id]
                            total_weight += weight * quantity
                        else:
                            print(f"Product ID {product_id} not found in the products list.")

                    # print(f"Total weight of the order is: {total_weight} kg")

                    delivery = Delivery(client_jid, loc, weight)
                    
                    # Filtrar os entregadores disponíveis
                    entregadores_disponiveis = [entregador for entregador in self.agent.deliveryman_subscribed if entregador.isAvailable() == True]

                    # Selecionar aleatoriamente um entregador disponível
                    if entregadores_disponiveis:
                        deliveryman = random.choice(entregadores_disponiveis).getAgent()
                     
                        msg = Message(to=deliveryman)             
                        msg.body = jsonpickle.encode(delivery)                               
                        msg.set_metadata("performative", "inform")

                        print(f"Agent {str(self.agent.jid)}: DeliverymanManager Agent inform Deliveryman Agent {str(deliveryman)}")
                        await self.send(msg)
                    
                    else:
                        # Lidar com o caso em que não há entregadores disponíveis
                        print("No deliveryman available.")
                        deliveryman = None  # Ou qualquer outra ação que você queira tomar

            elif performative == "subscribe":
                deliveryman_register = jsonpickle.decode(msg.body)
                self.agent.deliveryman_subscribed.append(deliveryman_register)

                print("Agent {}:".format(str(self.agent.jid)) + " DeliverymanManager Agent subscribed Deliveryman Agent {}".format(str(msg.sender)))
