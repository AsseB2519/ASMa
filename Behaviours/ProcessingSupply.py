import jsonpickle
from spade.behaviour import CyclicBehaviour
from spade.message import Message

class ProcessingStock_Behav(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=10) 
        if msg:
            # Message Threatment based on different Message performatives
            performative = msg.get_metadata("performative")
            client = str(msg.sender)
            if performative == "request":
                if msg.body == "Request Supply":
                    print("2")