import jsonpickle
from spade.behaviour import CyclicBehaviour
from spade.message import Message

from Classes.Purchase import Purchase

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

                    # Optionally, handle what to do with the total weight, e.g., send a message or log it
                    print(f"Total weight of the order is: {total_weight} kg")

