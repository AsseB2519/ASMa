import math
from spade.behaviour import CyclicBehaviour
from spade.message import Message

import asyncio
import jsonpickle

class Transport_Behav(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=10)  # wait for a message for 10 seconds
        if msg:
            # Message Threatment based on different Message performatives
            performative = msg.get_metadata("performative")
            if performative == "inform":

                self.agent.available = False

                inform = jsonpickle.decode(msg.body)

                client_jid = inform.getAgent()
                loc = inform.getPosition()
                weight = inform.getWeight()

                x_dest = loc.getX()
                y_dest = loc.getY()

                x_ori = self.agent.position.getX()
                y_ori = self.agent.position.getY()

                distance = math.sqrt((x_dest - x_ori)**2 + (y_dest - y_ori)**2)

                # print("Viagem 1")
                await asyncio.sleep(1)
                # await asyncio.sleep(distance/10)

                msg = Message(to=client_jid)       
                msg.body = jsonpickle.encode("Encomenda")                         
                msg.set_metadata("performative", "delivery")                   
    
                print("Agent {}:".format(str(self.agent.jid)) + " Deliveryman Agent delivered the package to Agent {}".format(str(client_jid)))
                await self.send(msg)                

                self.agent.position.setX(x_dest)
                self.agent.position.setY(y_dest)

                # DeliveryManager ??!?!

                await asyncio.sleep(1)
                # print("Viagem 2")

                self.agent.position.setX(x_ori)
                self.agent.position.setY(y_ori)

                self.agent.available = True


            else:
                print("Agent {}:".format(str(self.agent.jid)) + " Message not understood!")

        else:
            print("Agent {}:".format(str(self.agent.jid)) + "Did not received any message after 10 seconds")