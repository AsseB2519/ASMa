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
            if performative == "purchase":
                purchase = jsonpickle.decode(msg.body)

                # if isinstance(request, Purchase):
                client_jid = purchase.getAgent()
                loc = purchase.getInit()
                products = purchase.getProducts()

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

                # Check and wait for available purchase deliverymen
                while True:
                    # Filter available deliverymen of type 'Purchase'
                    entregadores_disponiveis = [entregador for entregador in self.agent.deliveryman_subscribed if entregador.isAvailable() and entregador.getType() == "Purchase"]

                    if entregadores_disponiveis:
                        break  # Exit the loop if there are available deliverymen
                    else:
                        print("No purchase deliveryman available. Waiting...")
                        await asyncio.sleep(5)  # Wait for 5 seconds before checking again

                # # Filtrar os entregadores disponíveis
                # entregadores_disponiveis = [entregador for entregador in self.agent.deliveryman_subscribed if entregador.isAvailable() and entregador.getType() == "Purchase"]

                # # Esperar até que haja entregadores disponíveis
                # while not entregadores_disponiveis:
                #     print("No purchase deliveryman available. Waiting...")
                #     await asyncio.sleep(5)  # Espera por 1 segundo antes de verificar novamente
                #     entregadores_disponiveis = [entregador for entregador in self.agent.deliveryman_subscribed if entregador.isAvailable() and entregador.getType() == "Purchase"]

                # Selecionar aleatoriamente um entregador disponível
                # deliveryman = random.choice(entregadores_disponiveis).getAgent()

                # Selecionar o primeiro entregador disponível
                deliveryman = entregadores_disponiveis[0].getAgent()

                self.agent.products_to_be_delivered[delivery_id] = delivery

                msg = Message(to=deliveryman)             
                msg.body = jsonpickle.encode(delivery)                               
                msg.set_metadata("performative", "purchase")

                print(f"Agent {str(self.agent.jid)}: DeliverymanManager Agent informed purchase to Deliveryman Agent {str(deliveryman)}")
                await self.send(msg)

            elif performative == "return":
                ret = jsonpickle.decode(msg.body)

                client_jid = ret.getAgent()
                loc = ret.getInit()
                products = ret.getProducts()

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

                # Check and wait for available purchase deliverymen
                while True:
                    # Filter available deliverymen of type 'Purchase'
                    entregadores_disponiveis = [entregador for entregador in self.agent.deliveryman_subscribed if entregador.isAvailable() and entregador.getType() == "Return"]

                    if entregadores_disponiveis:
                        break  # Exit the loop if there are available deliverymen
                    else:
                        print("No purchase deliveryman available. Waiting...")
                        await asyncio.sleep(5)  # Wait for 5 seconds before checking again

                # entregadores_disponiveis = [entregador for entregador in self.agent.deliveryman_subscribed if entregador.isAvailable() and entregador.getType() == "Return"]

                # Esperar até que haja entregadores disponíveis
                # while not entregadores_disponiveis:
                    # print("No return deliveryman available. Waiting...")
                    # await asyncio.sleep(5)  
                    # entregadores_disponiveis = [entregador for entregador in self.agent.deliveryman_subscribed if entregador.isAvailable() and entregador.getType() == "Return"]

                # Selecionar aleatoriamente um entregador disponível
                # deliveryman = random.choice(entregadores_disponiveis).getAgent()

                # Selecionar o primeiro entregador disponível
                deliveryman = entregadores_disponiveis[0].getAgent()

                self.agent.products_to_be_return[delivery_id] = delivery

                msg = Message(to=deliveryman)             
                msg.body = jsonpickle.encode(delivery)                               
                msg.set_metadata("performative", "return")

                print(f"Agent {str(self.agent.jid)}: DeliverymanManager Agent informed return to Deliveryman Agent {str(deliveryman)}")
                await self.send(msg)

            elif performative == "subscribe":
                deliveryman_register = jsonpickle.decode(msg.body)
                self.agent.deliveryman_subscribed.append(deliveryman_register)

                print("Agent {}:".format(str(self.agent.jid)) + " DeliverymanManager Agent subscribed Deliveryman Agent {}".format(str(msg.sender)))

            elif performative == "confirmation_delivery":
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

            elif performative == "confirmation_refund":
                # Decode the delivery information from the message body
                delivery = jsonpickle.decode(msg.body)

                for p in delivery:
                    print(p)

                # # Extract relevant information from the delivery object
                # id = delivery.getId()
                # client_jid = delivery.getAgent()
                # loc = delivery.getPosition()
                # weight = delivery.getWeight()

                # # Remove the delivered product from the pending deliveries list
                # del self.agent.products_to_be_delivered[id]

                # # Add the delivered product to the dictionary of delivered products
                # self.agent.products_delivered[id] = delivery
            else:
                print(f"Agent {self.agent.jid}: Message not understood!")                
