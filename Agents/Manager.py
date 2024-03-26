from spade import agent

class ManagerAgent(agent.Agent):

    taxis_subscribed = []

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")
        # a = ReceiveRequestBehav()
        # self.add_behaviour(a)