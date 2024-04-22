import jsonpickle
import random
from spade.message import Message
from spade.behaviour import CyclicBehaviour

class Negociation_Behav(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=10)  # wait for a message for 10 seconds
        if msg:
            performative = msg.get_metadata("performative")
            if performative == "propose":
                propose = jsonpickle.decode(msg.body)

                # Randomly decide to accept or deny the proposal
                decision = random.choice(["accept_proposal", "reject_proposal"])
                
                msg = Message(to=self.agent.get("stockmanager_contact"))             
                msg.body = jsonpickle.encode(propose)                               
                msg.set_metadata("performative", decision)

                if decision == "accept_proposal":
                    print(f"Agent {str(self.agent.jid)}: Client Agent accepts proposal from StockManager Agent {str(self.agent.get('stockmanager_contact'))}")
                else:
                    print(f"Agent {str(self.agent.jid)}: Client Agent rejects proposal from StockManager Agent {str(self.agent.get('stockmanager_contact'))}")

                await self.send(msg)
