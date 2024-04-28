import math
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
                # self.agent.available = False
                
                inform = jsonpickle.decode(msg.body)
                self.agent.deliveries.append(inform)

                # Calculate the total weight of all scheduled deliveries
                total_weight = sum([d.getWeight() for d in self.agent.deliveries])
                max_capacity = {'bike': 1, 'car': 3, 'truck': 5}[self.agent.vehicle_type]
                threshold_weight = 0.8 * max_capacity  # 80% of the maximum capacity

                # Only proceed if the total weight reaches at least 80% of the vehicle's capacity
                if total_weight >= threshold_weight:
                    self.agent.available = False
                    for delivery in self.agent.deliveries:
                        client_jid = delivery.getAgent()
                        loc = delivery.getPosition()
                        x_dest = loc.getX()
                        y_dest = loc.getY()

                        x_ori = self.agent.position.getX()
                        y_ori = self.agent.position.getY()
                        distance = math.sqrt((x_dest - x_ori)**2 + (y_dest - y_ori)**2)

                        # print(distance)
                        await asyncio.sleep(distance/10) 

                        self.agent.position.setX(x_dest)
                        self.agent.position.setY(y_dest)

                        msg = Message(to=client_jid)
                        msg.body = jsonpickle.encode(inform) 
                        msg.set_metadata("performative", "delivery")

                        print("Agent {}:".format(str(self.agent.jid)) + " Deliveryman Agent delivered the package to Client Agent {}".format(str(client_jid)))
                        await self.send(msg)
                        
                        msg = Message(to=self.agent.get("deliveryman_contact"))
                        msg.body = jsonpickle.encode(delivery)
                        msg.set_metadata("performative", "confirmation_delivery")

                        print("Agent {}:".format(str(self.agent.jid)) + " Deliveryman Agent has confirmed the delivery of the package to DeliveryManager Agent {}".format(str(client_jid)))
                        await self.send(msg)    

                    await asyncio.sleep(1)

                    self.agent.position.setX(int(config.WAREHOUSE_X))
                    self.agent.position.setY(int(config.WAREHOUSE_Y))

                    self.agent.available = True
                    self.agent.deliveries.clear()  # Clear the list after deliveries
                else:
                    print(f"Agent {self.agent.jid}: Current total weight {total_weight}kg does not meet the minimum threshold. Waiting for more packages.")
                    # self.agent.available = True  # Still available for receiving more packages
            
            elif performative == "return":
                # self.agent.available = False
                
                inform = jsonpickle.decode(msg.body)
                self.agent.deliveries.append(inform)

                # Calculate the total weight of all scheduled deliveries
                total_weight = sum([d.getWeight() for d in self.agent.deliveries])
                max_capacity = {'bike': 1, 'car': 3, 'truck': 5}[self.agent.vehicle_type]
                threshold_weight = 0.7 * max_capacity  # 80% of the maximum capacity

                # Only proceed if the total weight reaches at least 80% of the vehicle's capacity
                if total_weight >= threshold_weight:
                    self.agent.available = False
                    for delivery in self.agent.deliveries:
                        client_jid = delivery.getAgent()
                        loc = delivery.getPosition()
                        x_dest = loc.getX()
                        y_dest = loc.getY()

                        x_ori = self.agent.position.getX()
                        y_ori = self.agent.position.getY()
                        distance = math.sqrt((x_dest - x_ori)**2 + (y_dest - y_ori)**2)

                        # print(distance)
                        await asyncio.sleep(distance/10) 

                        self.agent.position.setX(x_dest)
                        self.agent.position.setY(y_dest)

                        msg = Message(to=client_jid)
                        msg.body = jsonpickle.encode(inform) 
                        msg.set_metadata("performative", "refund")

                        print("Agent {}:".format(str(self.agent.jid)) + " Deliveryman Agent delivered the package to Client Agent {}".format(str(client_jid)))
                        await self.send(msg)    

                    await asyncio.sleep(1)

                    msg = Message(to=self.agent.get("deliveryman_contact"))
                    msg.body = jsonpickle.encode(self.agent.deliveries)
                    msg.set_metadata("performative", "confirmation_refund")

                    print("Agent {}:".format(str(self.agent.jid)) + " Deliveryman Agent has confirmed the delivery of the package to DeliveryManager Agent {}".format(str(client_jid)))
                    
                    self.agent.position.setX(int(config.WAREHOUSE_X))
                    self.agent.position.setY(int(config.WAREHOUSE_Y))

                    self.agent.available = True
                    self.agent.deliveries.clear()  # Clear the list after deliveries
            else:
                print(f"Agent {self.agent.jid}: Message not understood!")

        # else:
        #     print(f"Agent {self.agent.jid}: Did not receive any message after 10 seconds")
