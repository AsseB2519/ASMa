import random 
from spade import agent
from Behaviours.RegisterDelivery import RegisterDelivery_Behav
from Behaviours.Transport import Transport_Behav
from Classes.Position import Position
import config

class DeliverymanAgent(agent.Agent):
    available = True

    async def setup(self):
        print(f"Agent {self.jid} starting...")

        self.deliveries = []
        self.position = Position(int(config.WAREHOUSE_X), int(config.WAREHOUSE_Y), config.random_node_selection(config.FILE_PATH))
        
        categories = ["Bike", "Moto", "Car"]
        probabilities_cat = [0.33, 0.33, 0.34]
        self.vehicle_type = random.choices(categories, weights=probabilities_cat)[0]

        self.actions = initialize_deliverymen(config.DELIVERYMAN)
        self.type = self.actions[0]  # Assign the first action type to this agent

        self.add_behaviour(RegisterDelivery_Behav())
        self.add_behaviour(Transport_Behav())

def initialize_deliverymen(total_deliverymen):
    if total_deliverymen < 2:
        raise ValueError("At least two deliverymen are required to ensure one of each type.")
    
    categories = ["Purchase", "Return"]
    types = ["Purchase", "Return"]  # Ensures one of each type initially
    additional_types = random.choices(categories, k=total_deliverymen - 2)
    types.extend(additional_types)
    random.shuffle(types)  # Shuffle to distribute types randomly
    return types
