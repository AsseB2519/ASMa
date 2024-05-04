import csv
from spade import agent

from Behaviours.ProcessingStock import ProcessingStock_Behav
from Behaviours.ProcessingSupply import ProcessingSupply_Behav
from Behaviours.RequestSupply import RequestSupply_Behav
from Behaviours.StatsStockManager import StatsStock_Behav
from Classes.Product_Manager import Product_Manager

class StockManagerAgent(agent.Agent):

    def set_gui(self, gui):
        self.gui = gui

    async def setup(self):
        # print("Agent {}".format(str(self.jid)) + " starting...")
        self.productsReturned = {}
        self.productsBought = {}

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
                max_quantity = int(row['Max_Quantity'])
                
                # Create a Product object and append it to the products list
                self.products.append(Product_Manager(product_id, name, category, quantity, price, max_quantity))

        a = ProcessingStock_Behav()
        self.add_behaviour(a)

        c = RequestSupply_Behav(period=50)
        self.add_behaviour(c)

        d = ProcessingSupply_Behav()
        self.add_behaviour(d)

        b = StatsStock_Behav(period=40)
        self.add_behaviour(b)



        
