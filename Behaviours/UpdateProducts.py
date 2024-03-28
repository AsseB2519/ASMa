import datetime
import getpass
import jsonpickle
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
from spade.message import Message

class Update_Behav(PeriodicBehaviour):
    async def run(self):
        # print(f"Running at {datetime.datetime.now().time()}: {self.counter}")

        products = [(product, quantity) for product, quantity in self.products.items() if quantity > 0]

        msg = Message(to=self.get("service_contact"))  
        msg.body = jsonpickle.encode(products)  
        msg.set_metadata("performative", "inform")                    
        await self.send(msg)
