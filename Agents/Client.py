from spade import agent
# from Behaviours.send_request import SendRequest_Behav
# from Behaviours.reply import ReplyBehav

class ClientAgent(agent.Agent):

    # taxis_subscribed = []

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")
        # a = SendRequest_Behav()
        # b = ReplyBehav()
        # self.add_behaviour(a)
        # self.add_behaviour(b)