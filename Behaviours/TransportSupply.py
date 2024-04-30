import random
import jsonpickle
import config
import time
import math
from spade.behaviour import CyclicBehaviour
from spade.message import Message

class TransportSupply_Behav(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=20) 
        if msg:
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
                # print("Trip 1")

                print("Agent {}:".format(str(self.agent.jid)) + " Supplier Agent got the products from SupplierWarehouse ")

                # for p in supply:
                #     quantidade_max = p.get_max_quantity()
                #     p.set_quantity(quantidade_max)

                # Modify the quantity with a higher probability of being the maximum
                for p in supply:
                    current_quantity = p.get_quantity()
                    max_quantity = p.get_max_quantity()
                    
                    # Decide whether to set to max quantity with a higher probability
                    if random.random() < 0.8:  # 80% chance to set to max quantity
                        new_quantity = max_quantity
                    else:
                        # 20% chance to set to a random quantity between current and max
                        new_quantity = random.randint(current_quantity, max_quantity)
                    
                    p.set_quantity(new_quantity)
                    print(current_quantity)
                    print(new_quantity)
                
                time.sleep(distance/10)
                # print("Trip 2")

                msg = Message(to=str(stockmanager))
                msg.body = jsonpickle.encode(supply)          
                msg.set_metadata("performative", "supply")

                # print("Agent {}:".format(str(self.agent.jid)) + " Supplier Agent supplied the stock of StockManager Agent " + str(stockmanager))
                await self.send(msg)
            
            else:
                print(f"Agent {self.agent.jid}: Message not understood!")                       