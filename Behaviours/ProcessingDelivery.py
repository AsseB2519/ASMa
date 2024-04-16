import jsonpickle
from spade.behaviour import CyclicBehaviour
from spade.message import Message

class ProcessingDelivery_Behav(CyclicBehaviour):
    async def run(self):
        print("A fazer")
