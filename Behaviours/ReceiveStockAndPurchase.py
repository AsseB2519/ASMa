import random
import numpy as np
import jsonpickle
from spade.behaviour import CyclicBehaviour
from spade.message import Message

from Classes.Purchase import Purchase

class ReceiveStockAndPurchase_Behav(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=10)  # wait for a message for 10 seconds
        if msg:
            performative = msg.get_metadata("performative")
            if performative == "inform":
                inform = jsonpickle.decode(msg.body)

                #self.agent.productsAvailable = inform

                # Randomly select 5 products and choose random quantity for each
                selected_products = random.sample(inform, 5)
                lista_compras = []

                #for product in selected_products:
                #    selected_quantity = random.randint(1, product.get_quantity())
                #    lista_compras.append((product, selected_quantity))

                # Function to generate weights with exponential decay
                def generate_weights(max_quantity):
                    decay_factor = 0.5  # Adjust as needed
                    weights = [np.exp(-decay_factor * i) for i in range(1, max_quantity + 1)]
                    return weights / np.sum(weights)

                for product in selected_products:
                    max_quantity = product.get_quantity()

                    # Generate weights based on exponential decay
                    weights = generate_weights(max_quantity)

                    # Manually increase the weight for selecting 1
                    weights[0] *= 2

                    # Choose a quantity based on the weights
                    selected_quantity = random.choices(range(1, max_quantity + 1), weights=weights)[0]

                    lista_compras.append((product.get_product_id(), selected_quantity))
                
                # Print selected products and quantities saved in tuples
                # print("Selected Products with Quantity:")
                # for product, quantity in lista_compras:
                #     print(f"Product: {product}, Quantity: {quantity}")

                for product, quantity in lista_compras:
                    if product in self.agent.productsBought:
                        self.agent.productsBought[product] += quantity
                    else:
                        self.agent.productsBought[product] = quantity

                purchase = Purchase(str(self.agent.jid), self.agent.position, lista_compras)

                msg = Message(to=self.agent.get("service_contact"))             
                msg.body = jsonpickle.encode(purchase)                               
                msg.set_metadata("performative", "request")

                print("Agent {}:".format(str(self.agent.jid)) + " Client Agent Purchase Product(s) to Manager Agent {}".format(str(self.agent.get("service_contact"))))
                await self.send(msg)

            else: print("Error3")