from spade import agent

from Behaviours.ProcessingDelivery import ProcessingDelivery_Behav

class DeliverymanManagerAgent(agent.Agent):

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")

        # products_to_be_delivered = {}

        # products_delivered = {}^

        a = ProcessingDelivery_Behav()
        self.add_behaviour(a)