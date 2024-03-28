import datetime
from spade import agent
from Behaviours.UpdateProducts import Update_Behav

class StockManagerAgent(agent.Agent):

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")
        # print(f"PeriodicSenderAgent started at {datetime.datetime.now().time()}")
        
        self.products = {
                'Apple': 20,
                'Banana': 20,
                'Grapefruit': 20,
                'Orange': 20,
                'Pear': 20,
                'Melon': 20,
                'Strawberry': 20
            }
        
        start_at = datetime.datetime.now() + datetime.timedelta(seconds=5)
        a = Update_Behav(period=2, start_at=start_at)
        self.add_behaviour(a)

        # a = StockProcessing_Behav()
        # self.add_behaviour(a)
