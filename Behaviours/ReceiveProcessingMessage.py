import jsonpickle
from spade.behaviour import OneShotBehaviour

class ReceiveProcessingMessage_Behav(OneShotBehaviour): # Ou periodic?
    async def run(self):
        msg = await self.receive(timeout=10)  # wait for a message for 10 seconds
        if msg:
            # Message Treatment based on different Message performatives
            performative = msg.get_metadata("performative")
            if performative == "inform":
                if msg.body == "Request to be Processed":
                    # Process the inform message
                    print("Agent {}:".format(str(self.agent.jid)) + " Client Agent Received a message with content :", msg.body)
                else: 
                    request = jsonpickle.decode(msg.body)
                    self.agent.productsAvailable = request
                    print("Agent {}:".format(str(self.agent.jid)) + " Client Agent Received Products Available")
            else: print("Error")