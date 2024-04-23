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

                print("Cheguei")

                # self.agent.current_location.setAvailable(False)

                # # Taxi takes 1 second per transportation
                # await asyncio.sleep(3)

                # # Update current position and make Taxi available
                # make_request = jsonpickle.decode(msg.body)
                # self.agent.current_location.setPosition(make_request.getDest())
                # self.agent.current_location.setAvailable(True)

                # # Send Confirm Message to Client and Manager
                # msg_to_manager = Message(to=str(msg.sender))  # Instantiate the message
                # msg_to_manager.body = jsonpickle.encode(
                #     self.agent.current_location)  # Set the message content (serialized object)
                # msg_to_manager.set_metadata("performative", "confirm")  # Set the message performative

                # msg_to_client = Message(to=make_request.getAgent())  # Instantiate the message
                # msg_to_client.body = jsonpickle.encode(
                #     self.agent.current_location)  # Set the message content (serialized object)
                # msg_to_client.set_metadata("performative", "confirm")  # Set the message performative

                # await self.send(msg_to_manager)
                # await self.send(msg_to_client)

            else:
                print("Agent {}:".format(str(self.agent.jid)) + " Message not understood!")

        else:
            print("Agent {}:".format(str(self.agent.jid)) + "Did not received any message after 10 seconds")