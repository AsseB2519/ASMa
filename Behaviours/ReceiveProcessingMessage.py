from spade.behaviour import OneShotBehaviour

class ReceiveProcessingMessage_Behav(OneShotBehaviour): # Ou periodic?
    async def run(self):
        msg = await self.receive(timeout=10)  # wait for a message for 10 seconds
        if msg:
            # Message Treatment based on different Message performatives
            performative = msg.get_metadata("performative")
            if performative == "inform":
                # Process the inform message
                print("Agent {}:".format(str(self.agent.jid)) + " Client Agent Received a message with content :", msg.body)
                # Continue with your processing here
                # You can access message content using msg.body
                # Perform actions based on the content of the message
            else:
                print("Received a message with performative:", performative)
                print("This behaviour only handles 'inform' messages.")
