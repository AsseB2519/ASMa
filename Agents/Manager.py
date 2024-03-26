from spade import agent
from Behaviours.Reply import ReplyBehav

class ManagerAgent(agent.Agent):

    taxis_subscribed = []

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")
        a = ReplyBehav()
        self.add_behaviour(a)