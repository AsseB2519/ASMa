import csv
from spade import agent
from Behaviours.ProcessingStock import ProcessingStock_Behav

from Behaviours.RequestSupply import RequestSupply_Behav
from Classes.Product_Manager import Product_Manager

class StockManagerAgent(agent.Agent):

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")
        
        # Initialize an empty list to store products
        self.products = []

        # Read the products from the CSV file
        with open('stock_products.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                product_id = int(row['ID'])
                name = row['Name']
                category = row['Category']
                quantity = int(row['Quantity'])
                price = float(row['Price'])
                
                # Create a Product object and append it to the products list
                self.products.append(Product_Manager(product_id, name, category, quantity, price))

        a = ProcessingStock_Behav()
        self.add_behaviour(a)

        # duas listas de products fazer a comparação e quando uma vir que esta a 75% por exemplo dispara o behaviour
        # b = RequestSupply_Behav()
        # self.add_behaviour(b)
