from spade import agent
from Behaviours.SendRequest import SendRequest_Behav

class ClientAgent(agent.Agent):

    # taxis_subscribed = []

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")
        self.products = ['Apple', 'Banana', 'Grapefruit', 'Orange', 'Pear', 'Melon', 'Strawberry']
        a = SendRequest_Behav()
        # b = ReplyBehav()
        self.add_behaviour(a)
        # self.add_behaviour(b)