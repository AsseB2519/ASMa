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

                print(request)
                
                if isinstance(request, Purchase):
                    products = request.getProducts()
                    for p in products:
                        print(p)


