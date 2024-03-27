import random
import jsonpickle

from spade.behaviour import OneShotBehaviour
from spade.message import Message

from Classes.Position import Position
from Classes.Purchase import Return
from Classes.Product import Product

class Return_Behav (OneShotBehaviour): # Ou periodic?
    async def run(self):

        produtos_devolver = {}

        # Determine the maximum number of products to return
        max_products_to_return = min(len(self.productsBought), 5)  # Assuming you want to return up to 5 products

        # Randomly select products and their quantities to return
        for _ in range(max_products_to_return):
            # Randomly select a product from self.productsBought
            product = random.choice(list(self.productsBought.keys()))
            # Determine the quantity to return for the selected product
            quantity_to_return = random.randint(1, self.productsBought[product])  # Random quantity up to the bought quantity
            # Add the selected product and quantity to the produtos_devolver dictionary
            produtos_devolver[product] = quantity_to_return

            # Update self.productsBought to reflect the returned quantity
            self.productsBought[product] -= quantity_to_return

            # If the quantity of the product to return becomes 0, remove it from self.productsBought
            if self.productsBought[product] == 0:
                del self.productsBought[product]

        print("Products to return:", produtos_devolver)

        # create Request class instance
        mr = Return(str(self.agent.jid), self.agent.position, produtos_devolver)
        print("Agent {}:".format(str(self.agent.jid)) + " Client Agent initialized with Return Request {}".format(mr.toString()))

        msg = Message(to=self.agent.get("service_contact"))             # Instantiate the message
        msg.body = jsonpickle.encode(mr)                                # Set the message content (serialized object)
        msg.set_metadata("performative", "request")                     # Set the message performative

        print("Agent {}:".format(str(self.agent.jid)) + " Client Agent requested refund of Product(s) to Manager Agent {}".format(str(self.agent.get("service_contact"))))
        await self.send(msg)

