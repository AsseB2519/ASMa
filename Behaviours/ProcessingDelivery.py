import asyncio
import random
import jsonpickle
from spade.behaviour import CyclicBehaviour
from spade.message import Message

from Classes.Purchase import Purchase
from Classes.Delivery import Delivery

class ProcessingDelivery_Behav(CyclicBehaviour):
    
    delivery_id_counter = 0

    async def run(self):
        msg = await self.receive(timeout=10) 
        if msg:
            # Message Threatment based on different Message performatives
            performative = msg.get_metadata("performative")
            if performative == "inform":
                request = jsonpickle.decode(msg.body)

                # if isinstance(request, Purchase):
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
                self.delivery_id_counter += 1
                delivery_id = self.delivery_id_counter

                delivery = Delivery(delivery_id, client_jid, loc, total_weight)
                
                # Filtrar os entregadores disponíveis
                entregadores_disponiveis = [entregador for entregador in self.agent.deliveryman_subscribed if entregador.isAvailable() and entregador.getType() == "Purchase"]

                # Esperar até que haja entregadores disponíveis
                while not entregadores_disponiveis:
                    print("No deliveryman available. Waiting...")
                    await asyncio.sleep(5)  # Espera por 1 segundo antes de verificar novamente
                    entregadores_disponiveis = [entregador for entregador in self.agent.deliveryman_subscribed if entregador.isAvailable() and entregador.getType() == "Purchase"]

                # Selecionar aleatoriamente um entregador disponível
                deliveryman = random.choice(entregadores_disponiveis).getAgent()

                # Selecionar o primeiro entregador disponível
                # deliveryman = entregadores_disponiveis[0].getAgents()

                self.agent.products_to_be_delivered[delivery_id] = delivery

                msg = Message(to=deliveryman)             
                msg.body = jsonpickle.encode(delivery)                               
                msg.set_metadata("performative", "inform")

                print(f"Agent {str(self.agent.jid)}: DeliverymanManager Agent inform Deliveryman Agent {str(deliveryman)}")
                await self.send(msg)

            elif performative == "subscribe":
                deliveryman_register = jsonpickle.decode(msg.body)
                self.agent.deliveryman_subscribed.append(deliveryman_register)

                print("Agent {}:".format(str(self.agent.jid)) + " DeliverymanManager Agent subscribed Deliveryman Agent {}".format(str(msg.sender)))

            elif performative == "confirmation":
                # Decode the delivery information from the message body
                delivery = jsonpickle.decode(msg.body)

                # Extract relevant information from the delivery object
                id = delivery.getId()
                client_jid = delivery.getAgent()
                loc = delivery.getPosition()
                weight = delivery.getWeight()

                # Remove the delivered product from the pending deliveries list
                del self.agent.products_to_be_delivered[id]

                # Add the delivered product to the dictionary of delivered products
                self.agent.products_delivered[id] = delivery

