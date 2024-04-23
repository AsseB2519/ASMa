import random

from spade.behaviour import OneShotBehaviour
from spade.message import Message

import jsonpickle

from Classes.InformPosition import InformPosition

class Register_Behav(OneShotBehaviour):
    
    async def run(self):
        register = InformPosition(str(self.agent.jid), True)

        msg = Message(to=self.agent.get("deliveryman_contact"))             
        msg.body = jsonpickle.encode(register)       
        msg.set_metadata("performative", "subscribe")                   

        print("Agent {}:".format(str(self.agent.jid)) + " Deliveryman Agent subscribing to DeliverymanManager Agent {}".format(str(self.agent.get("deliveryman_contact"))))
        await self.send(msg)