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
                print(inform)

                self.agent.deliveries.append(inform)

                id = inform.getId()
                client_jid = inform.getAgent()
                loc = inform.getPosition()
                weight = inform.getWeight()

                # Check if the total weight of accumulated deliveries is within the vehicle's capacity
                total_weight = sum([d.getWeight() for d in self.agent.deliveries])
                max_capacity = {'bike': 5, 'car': 10, 'truck': 15}[self.agent.vehicle_type]

                if total_weight <= max_capacity:
                    # Process deliveries if within capacity
                    for delivery in self.agent.deliveries:
                        # Process each delivery (send confirmation, move agent, etc.)
                        # Simulate delivery (update agent state, send messages)
                        x_dest = delivery.getPosition().getX()
                        y_dest = delivery.getPosition().getY()

                        x_ori = self.agent.position.getX()
                        y_ori = self.agent.position.getY()

                        distance = math.sqrt((x_dest - x_ori)**2 + (y_dest - y_ori)**2)

                        await asyncio.sleep(1)
                        # await asyncio.sleep(distance/10)

                        self.agent.position.setX(x_dest)
                        self.agent.position.setY(y_dest)

                        msg = Message(to=client_jid)       
                        # MUDAR
                        msg.body = jsonpickle.encode("Encomenda")                          
                        msg.set_metadata("performative", "delivery")                   

                        print("Agent {}:".format(str(self.agent.jid)) + " Deliveryman Agent delivered the package to Client Agent {}".format(str(client_jid)))
                        await self.send(msg)                

                        msg = Message(to=self.agent.get("deliveryman_contact"))     
                        msg.body = jsonpickle.encode(inform)                         
                        msg.set_metadata("performative", "confirmation")  

                        print("Agent {}:".format(str(self.agent.jid)) + " Deliveryman Agent has confirmed the delivery of the package to DeliveryManager Agent {}".format(str(client_jid)))
                        await self.send(msg)                

                    await asyncio.sleep(1)
                    # await asyncio.sleep(distance/10)

                    self.agent.position.setX(x_ori)
                    self.agent.position.setY(y_ori)

                    self.agent.available = True
                    self.agent.deliveries.clear()  

            else:
                print("Agent {}:".format(str(self.agent.jid)) + " Message not understood!")

        else:
            print("Agent {}:".format(str(self.agent.jid)) + "Did not received any message after 10 seconds")