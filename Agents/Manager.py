from spade import agent
from Behaviours.Processing import Processing_Behav

class ManagerAgent(agent.Agent):

    # taxis_subscribed = []

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")
        a = Processing_Behav()
        self.add_behaviour(a)