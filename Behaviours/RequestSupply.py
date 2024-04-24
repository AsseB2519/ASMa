from spade.behaviour import OneShotBehaviour
from spade.message import Message

class RequestSupply_Behav (OneShotBehaviour):
    async def run(self):
        # Dizer que produtos pretende comprar
        
        msg = Message(to=self.agent.get('supplier_contact'))   
        msg.body = "Request Supply"               
        msg.set_metadata("performative", "request")           
        
        print("Agent {}:".format(str(self.agent.jid)) + " StockManager Agent requested Product(s) to Supplier Agent {}".format(str(self.agent.get("supplier_contact"))))
        await self.send(msg)        