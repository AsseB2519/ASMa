from spade.behaviour import OneShotBehaviour
from spade.message import Message

class RequestProducts_Behav (OneShotBehaviour):
    async def run(self):
        msg = Message(to=self.agent.get('stockmanager_contact'))   
        msg.body = "Request Products Available"               
        msg.set_metadata("performative", "request")           
        
        print("Agent {}:".format(str(self.agent.jid)) + " Client Agent requested Product(s) Available to StockManager Agent {}".format(str(self.agent.get("stockmanager_contact"))))
        await self.send(msg)                                  
        
        
