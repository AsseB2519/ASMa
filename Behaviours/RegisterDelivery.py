from spade.behaviour import OneShotBehaviour
from spade.message import Message

import jsonpickle

from Classes.InformPosition import InformPosition

class RegisterDelivery_Behav(OneShotBehaviour):
    async def run(self):
        register = InformPosition(str(self.agent.jid), self.agent.position, self.agent.available, self.agent.type)

        msg = Message(to=self.agent.get("deliveryman_contact"))             
        msg.body = jsonpickle.encode(register)       
        msg.set_metadata("performative", "subscribe")                   

        if self.agent.type == "Purchase":
            print("Agent {}:".format(str(self.agent.jid)) + " PurchaseDeliveryman Agent subscribed to DeliverymanManager Agent {}".format(str(self.agent.get("deliveryman_contact"))))
        elif self.agent.type == "Return":
            print("Agent {}:".format(str(self.agent.jid)) + " ReturnDeliveryman Agent subscribed to DeliverymanManager Agent {}".format(str(self.agent.get("deliveryman_contact"))))

        await self.send(msg)