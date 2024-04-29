import jsonpickle
import config
import time
import math
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
                supply = jsonpickle.decode(msg.body)

                x_dest = config.WAREHOUSE_X
                y_dest = config.WAREHOUSE_Y

                x_ori = self.agent.position.getX()
                y_ori = self.agent.position.getY()

                distance = math.sqrt((x_dest - x_ori)**2 + (y_dest - y_ori)**2)

                time.sleep(distance/10)
                print("Trip 1")

                print("Agent {}:".format(str(self.agent.jid)) + " Supplier Agent got the products from SupplierWarehouse ")
                
                time.sleep(distance/10)
                print("Trip 2")

                msg = Message(to=str(msg.make_reply)) # stockmanager
                msg.body = jsonpickle.encode(supply)          
                msg.set_metadata("performative", "supply")
            
            else:
                print(f"Agent {self.agent.jid}: Message not understood!")                       