from spade import agent
# from Behaviours.register_taxi import RegisterTaxi_Behav
# from Behaviours.execute_transport import Transport_Behav

# from Classes.informposition import InformPosition

class TaxiAgent(agent.Agent):

    current_location = None

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")
        # a = RegisterTaxi_Behav()
        # b = Transport_Behav()
        # self.add_behaviour(a)
        # self.add_behaviour(b)