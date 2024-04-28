import random 
from spade import agent

from Behaviours.RegisterDelivery import RegisterDelivery_Behav
from Behaviours.Transport import Transport_Behav
from Classes.Position import Position
import config

class DeliverymanAgent(agent.Agent):

    available = True

    async def setup(self):
        self.deliveries = []

        # self.position = Position(random.randint(1, 100), random.randint(1, 100))
        self.position = Position(int(config.WAREHOUSE_X), int(config.WAREHOUSE_Y))
        
        categories = ["bike", "car", "truck"]  # List of possible vehicle categories
        probabilities_cat = [0.5, 0.3, 0.2]
        self.vehicle_type = random.choices(categories, weights=probabilities_cat)[0]

        actions = ["Purchase", "Return"]
        probabilities = [0.75, 0.25] 
        self.type = random.choices(actions, weights=probabilities)[0]
        
        print("Agent {}".format(str(self.jid)) + " starting...")

        a = RegisterDelivery_Behav()
        self.add_behaviour(a)
        b = Transport_Behav()
        self.add_behaviour(b)
        