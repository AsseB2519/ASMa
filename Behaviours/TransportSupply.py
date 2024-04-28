import jsonpickle
from spade.behaviour import CyclicBehaviour
from spade.message import Message

class TransportSupply_Behav(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=10) 
        if msg:
            # Message Threatment based on different Message performatives
            performative = msg.get_metadata("performative")
            stockmanager = str(msg.sender)
            if performative == "supply":
                supply =  jsonpickle.decode(msg.body)

                print(supply)

                # Buscar a Entrega