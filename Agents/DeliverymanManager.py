import csv
from spade import agent

from Behaviours.ProcessingDelivery import ProcessingDelivery_Behav
from Behaviours.StatsDeliveryman import StatsDeliveryman_Behav

class DeliverymanManagerAgent(agent.Agent):
    async def setup(self):
        # print("Agent {}".format(str(self.jid)) + " starting...")

        self.deliveryman_subscribed = []

        self.products_to_be_return = []
        self.products_returned = []
        self.products_to_be_delivered = {}
        self.products_delivered = {}
        self.products = {}
        
        with open('delivery_products.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                product_id = int(row['ID'])
                weight = float(row['Weight'])
                
                # Create a Product object and append it to the products list
                self.products[product_id] = weight

        a = ProcessingDelivery_Behav()
        self.add_behaviour(a)

        b = StatsDeliveryman_Behav(period=40)
        self.add_behaviour(b)