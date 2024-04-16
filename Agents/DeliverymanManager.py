from spade import agent

class DeliverymanManagerAgent(agent.Agent):

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")

        
        # a = StockProcessing_Behav()
        # self.add_behaviour(a)
