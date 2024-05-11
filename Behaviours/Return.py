import random
import numpy as np
import jsonpickle

from spade.behaviour import PeriodicBehaviour
from spade.message import Message

from Classes.Return import Return

class Return_Behav (PeriodicBehaviour): 
    def generate_exponential_decay_weights(self, n, decay_factor=0.4):
        """Generate weights with exponential decay."""
        weights = np.exp(-decay_factor * np.arange(n))
        return weights / np.sum(weights)

    def select_products_to_return(self, products_bought, count_weights):
        """Select a random number of product types to return based on weights."""
        number_of_products_to_return = random.choices(range(1, len(products_bought) + 1), weights=count_weights, k=1)[0]
        return random.sample(list(products_bought.items()), k=number_of_products_to_return)

    def determine_return_quantities(self, products_to_return, quantity_decay_factor=0.4):
        """Determine quantities for each selected product to return using exponential decay weights."""
        return_list = []
        for product_id, bought_quantity in products_to_return:
            if bought_quantity > 1:
                quantity_weights = self.generate_exponential_decay_weights(bought_quantity, decay_factor=quantity_decay_factor)
                quantity_to_return = random.choices(range(1, bought_quantity + 1), weights=quantity_weights, k=1)[0]
            else:
                quantity_to_return = 1  # If only one was bought, return it
            return_list.append((product_id, quantity_to_return))
        return return_list

    async def run(self):
        if self.agent.productsBought:
            count_weights = self.generate_exponential_decay_weights(len(self.agent.productsBought))
            selected_products = self.select_products_to_return(self.agent.productsBought, count_weights)
            return_list = self.determine_return_quantities(selected_products)

            tamanho = 0
            # Update the agent's productsBought dictionary
            for product_id, return_quantity in return_list:
                tamanho += return_quantity
                if product_id in self.agent.productsBought:
                    self.agent.productsBought[product_id] -= return_quantity
                    # Optionally, check if quantity goes to zero and remove or handle differently
                    if self.agent.productsBought[product_id] <= 0:
                        del self.agent.productsBought[product_id]

            returns = Return(str(self.agent.jid), self.agent.position, return_list)
        
            msg = Message(to=self.agent.get("stockmanager_contact"))            
            msg.body = jsonpickle.encode(returns)                                
            msg.set_metadata("performative", "return")                     

            print("Client {}".format(str(self.agent.jid)) + " return " + {str(tamanho)} + " product(s) to StockManager {}".format(str(self.agent.get("stockmanager_contact"))))
            await self.send(msg)

            # print(f"Products returned: {return_list}")
        # else:
        #     print("No products to return.")


        

