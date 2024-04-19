import jsonpickle
from spade.behaviour import OneShotBehaviour
from spade.message import Message

class InformProducts_Behav (OneShotBehaviour):
    async def run(self):
        msg = Message(to=self.agent.get('deliveryman_contact'))   
        msg.body = jsonpickle.encode(self.agent.products)
        msg.set_metadata("performative", "inform")           
        
        print("Agent {}:".format(str(self.agent.jid)) + " StockManager Agent informed Product(s) to DeliverymanManager Agent {}".format(str(self.agent.get("deliveryman_contact"))))
        await self.send(msg)                                  
        
        
