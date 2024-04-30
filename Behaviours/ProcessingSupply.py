import jsonpickle
from spade.behaviour import CyclicBehaviour
from spade.message import Message

class ProcessingSupply_Behav(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=20) 
        if msg:
            # Message Threatment based on different Message performatives
            performative = msg.get_metadata("performative")
            if performative == "supply":
                supply = jsonpickle.decode(msg.body)

                for p in supply:
                    for products in self.agent.products:
                        if p.get_product_id() == products.get_product_id():
                            quantity_new = p.get_quantity()
                            products.set_quantity(quantity_new)
