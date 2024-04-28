import math
import time
import config
import asyncio
from spade.message import Message
from spade.behaviour import CyclicBehaviour
import jsonpickle

class Transport_Behav(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=10)  # wait for a message for 10 seconds
        if msg:
            performative = msg.get_metadata("performative")
            if performative == "purchase":
                self.agent.available = False
                
                purchase = jsonpickle.decode(msg.body)

                client_jid = purchase.getAgent()
                loc = purchase.getPosition()
                x_dest = loc.getX()
                y_dest = loc.getY()

                x_ori = self.agent.position.getX()
                y_ori = self.agent.position.getY()
                distance = math.sqrt((x_dest - x_ori)**2 + (y_dest - y_ori)**2)

                print("Trip 1")
                trip = distance / 10
                time.sleep(trip)
                # await asyncio.sleep(trip) 
                
                self.agent.position.setX(x_dest)
                self.agent.position.setY(y_dest)

                msg = Message(to=client_jid)
                msg.body = "Delivery"
                msg.set_metadata("performative", "delivery")

                print("Agent {}:".format(str(self.agent.jid)) + " Deliveryman Agent delivered the package to Client Agent {}".format(str(client_jid)))
                await self.send(msg)

                msg = Message(to=self.agent.get("deliveryman_contact"))
                msg.body = jsonpickle.encode(purchase)
                msg.set_metadata("performative", "confirmation_delivery")

                print("Agent {}:".format(str(self.agent.jid)) + " Deliveryman Agent has confirmed the delivery of the package to DeliveryManager Agent {}".format(self.agent.get("deliveryman_contact")))
                await self.send(msg)    

                print("Trip 2")
                time.sleep(trip)
                # await asyncio.sleep(distance/10)

                self.agent.position.setX(int(config.WAREHOUSE_X))
                self.agent.position.setY(int(config.WAREHOUSE_Y))

                self.agent.available = True
            
            elif performative == "return":
                self.agent.available = False
                
                ret = jsonpickle.decode(msg.body)

                client_jid = ret.getAgent()
                loc = ret.getPosition()
                x_dest = loc.getX()
                y_dest = loc.getY()

                x_ori = self.agent.position.getX()
                y_ori = self.agent.position.getY()
                distance = math.sqrt((x_dest - x_ori)**2 + (y_dest - y_ori)**2)

                print("Trip 1")
                trip = distance / 10
                # time.sleep(trip)
                time.sleep(1)

                self.agent.position.setX(x_dest)
                self.agent.position.setY(y_dest)

                msg = Message(to=client_jid)
                msg.body = "Refund" 
                msg.set_metadata("performative", "refund")

                print("Agent {}:".format(str(self.agent.jid)) + " Client Agent delivered the refund products to Deliveryman Agent {}".format(str(client_jid)))
                await self.send(msg)    

                print("Trip 2")
                # time.sleep(trip)
                time.sleep(1)

                msg = Message(to=self.agent.get("deliveryman_contact"))
                msg.body = jsonpickle.encode(ret)
                msg.set_metadata("performative", "confirmation_refund")

                print("Agent {}:".format(str(self.agent.jid)) + " Deliveryman Agent has confirmed the delivery of the package to DeliverymanManager Agent {}".format(self.agent.get("deliveryman_contact")))
                await self.send(msg)   

                self.agent.position.setX(int(config.WAREHOUSE_X))
                self.agent.position.setY(int(config.WAREHOUSE_Y))

                self.agent.available = True
            else:
                print(f"Agent {self.agent.jid}: Message not understood!")

        # else:
        #     print(f"Agent {self.agent.jid}: Did not receive any message after 10 seconds")
