from spade import agent

class DeliverymanAgent(agent.Agent):

    current_location = None

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")