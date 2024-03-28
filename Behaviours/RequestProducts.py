from spade.behaviour import OneShotBehaviour
from spade.message import Message

class RequestProducts_Behav (OneShotBehaviour):
    async def run(self):
        # create Request class instance

        msg = Message(to=self.agent.get('service_contact'))   # Instantiate the inform message
        msg.body = "Request Products Available"               # Set the message content
        msg.set_metadata("performative", "request")           # Set the message performative
        await self.send(msg)                                  # Send the inform message
        
        print("Agent {}:".format(str(self.agent.jid)) + " Client Agent requested Product(s) Available to Manager Agent {}".format(str(self.agent.get("service_contact"))))
        
