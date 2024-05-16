import random 
from spade import agent

from Behaviours.RegisterDelivery import RegisterDelivery_Behav
from Behaviours.Transport import Transport_Behav
from Classes.Position import Position
import config

class DeliverymanAgent(agent.Agent):

    available = True

    async def setup(self):
        # print("Agent {}".format(str(self.jid)) + " starting...")

        self.deliveries = []

        # self.position = Position(random.randint(1, 100), random.randint(1, 100))
        self.position = Position(int(config.WAREHOUSE_X), int(config.WAREHOUSE_Y), config.random_node_selection(config.FILE_PATH))
        
        categories = ["Bike", "Moto", "Car"]  # List of possible vehicle categories
        # probabilities_cat = [0, 0.45, 0.55]
        probabilities_cat = [1, 0, 0]
        self.vehicle_type = random.choices(categories, weights=probabilities_cat)[0]

        actions = ["Purchase", "Return"]
        probabilities = [1, 0] 
        self.type = random.choices(actions, weights=probabilities)[0]
        
        a = RegisterDelivery_Behav()
        self.add_behaviour(a)
        b = Transport_Behav()
        self.add_behaviour(b)
        