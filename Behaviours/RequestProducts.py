import time
import config
from spade.behaviour import PeriodicBehaviour
from spade.message import Message

class RequestProducts_Behav(PeriodicBehaviour):
    async def run(self):

        time.sleep(config.CLIENTS)

        numero = config.CLIENTS 
        config.CLIENTS = numero + 1 

        time.sleep(numero)

        msg = Message(to=self.agent.get('stockmanager_contact'))   
        msg.body = "Request Products Available"               
        msg.set_metadata("performative", "request")           
        
        # print("Agent {}:".format(str(self.agent.jid)) + " Client Agent requested Product(s) Available to StockManager Agent {}".format(str(self.agent.get("stockmanager_contact"))))
        print("Client {}".format(str(self.agent.jid)) + " request product(s) available to StockManager {}".format(str(self.agent.get("stockmanager_contact"))))
        await self.send(msg)   