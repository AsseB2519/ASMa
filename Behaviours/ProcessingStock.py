import random
import jsonpickle
from spade.behaviour import CyclicBehaviour
from spade.message import Message

from Classes.Product import Product
from Classes.Product_Manager import Product_Manager
from Classes.Purchase import Purchase
from Classes.Return import Return

class ProcessingStock_Behav(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=20) 
        if msg:
            # Message Threatment based on different Message performatives
            performative = msg.get_metadata("performative")
            client = str(msg.sender)
            if performative == "request":
                if msg.body == "Request Products Available":
                   
                    new_products = []
                    for p in self.agent.products:
                        quantidade = p.get_quantity()
                        if quantidade > 0:
                            new_products.append(p)

                    # Construct a list of dictionaries containing information for each available product
                    message_body = []
                    for product in new_products:
                        produto = Product(product.get_product_id(), product.get_name(), product.get_category(), product.get_price())
                        message_body.append(produto)
                    
                    msg = Message(to=client) # msg.make_reply()
                    msg.body = jsonpickle.encode(message_body) # self.agent.products
                    msg.set_metadata("performative", "inform")           
            
                    # print("Agent {}:".format(str(self.agent.jid)) + " StockManager Agent informed Product(s) Available to Client Agent {}".format(client))
                    print("StockManager {}".format(str(self.agent.jid)) + " informs product(s) available to Client {}".format(client))
                    await self.send(msg)

            elif performative == "purchase":
                request = jsonpickle.decode(msg.body)

                lista_compras = request.getProducts()

                # Dictionary to store the proposed quantities
                proposed_products = []
                can_fulfill_order = True

                preco = 0
                tamanho = 0
                for product_id, requested_quantity in lista_compras:
                    found = False
                    for product in self.agent.products:
                        if product.get_product_id() == product_id:
                            found = True
                            available_quantity = product.get_quantity()
                            if available_quantity < requested_quantity:
                                can_fulfill_order = False
                                # Não há stock suficiente, propor quantidade disponível
                                preco += available_quantity * product.get_price()
                                tamanho += available_quantity                                
                                proposed_product = Product_Manager(product.get_product_id(), product.get_name(), product.get_category(), available_quantity, product.get_price(), product.get_max_quantity())
                                proposed_products.append(proposed_product)
                    if not found:
                        print(f"Product {product_id} not found")
            
                if not can_fulfill_order:
                    negotiation_msg = Message(to=client)
                    negotiation_msg.body = jsonpickle.encode(proposed_products)
                    negotiation_msg.set_metadata("performative", "propose")

                    print(f"StockManager {self.agent.jid} propose {tamanho} product(s) paying {preco:.2f}€ to Client Agent {client}")
                    # print("StockManager {}".format(str(self.agent.jid)) + "  Agent propose Client Agent {}".format(client))
                    await self.send(negotiation_msg)

                else:
                    # If all items can be supplied, decrement the stock and confirm the order
                    for product_id, decrement in lista_compras:
                        for product in self.agent.products:
                            if product.get_product_id() == product_id:
                                new_quantity = product.get_quantity() - decrement
                                product.set_quantity(new_quantity)

                    for product_id, quantity in lista_compras:
                        if product_id in self.agent.productsBought:
                            # If the product ID already exists, add the quantity
                            self.agent.productsBought[product_id] += quantity
                        else:
                            # If the product ID does not exist, create a new entry with this quantity
                            self.agent.productsBought[product_id] = quantity

                    # Send confirmation to the delivery manager
                    confirmation_msg = Message(to=self.agent.get("deliveryman_contact"))
                    confirmation_msg.body = jsonpickle.encode(request)
                    confirmation_msg.set_metadata("performative", "purchase")

                    # print("Agent {}:".format(str(self.agent.jid)) + " StockManager Agent informed purchase delivery details to DeliverymanManager Agent {}".format(str(self.agent.get("deliveryman_contact"))))
                    await self.send(confirmation_msg)
                
            elif performative == "return":
                    request = jsonpickle.decode(msg.body)

                    msg = Message(to=self.agent.get("deliveryman_contact"))       
                    msg.body = jsonpickle.encode(request)                         
                    msg.set_metadata("performative", "return")                   
        
                    # print("Agent {}:".format(str(self.agent.jid)) + " StockManager Agent informed return delivery details to DeliverymanManager Agent {}".format(str(self.agent.get("deliveryman_contact"))))
                    await self.send(msg)
                    
            elif performative == "accept_proposal":
                accept_proposal = jsonpickle.decode(msg.body)
                lista_compras = accept_proposal.getProducts()

                for product_id, decrement in lista_compras:
                    for product in self.agent.products:
                        if product.get_product_id() == product_id:
                            new_quantity = product.get_quantity() - decrement
                            product.set_quantity(new_quantity)

                for product_id, quantity in lista_compras:
                    if product_id in self.agent.productsBought:
                        # If the product ID already exists, add the quantity
                        self.agent.productsBought[product_id] += quantity
                    else:
                        # If the product ID does not exist, create a new entry with this quantity
                        self.agent.productsBought[product_id] = quantity

                msg = Message(to=self.agent.get("deliveryman_contact"))       
                msg.body = jsonpickle.encode(accept_proposal)                         
                msg.set_metadata("performative", "purchase") 

                # print("Agent {}:".format(str(self.agent.jid)) + " StockManager Agent requesting PurchaseDeliveryman after Negociation to DeliverymanManager Agent {}".format(str(self.agent.get("deliveryman_contact"))))
                await self.send(msg)
            
            elif performative == "confirmation_refund":
                ret = jsonpickle.decode(msg.body)

                for r in ret: 
                    client_jid = r.getAgent()
                    loc = r.getInit()
                    products = r.getProducts()

                    for product_id, quantity in products:
                        # Decrease the quantity of bought products
                        if product_id in self.agent.productsBought:
                            self.agent.productsBought[product_id] -= quantity
                            # Check if the remaining quantity is zero or less; if so, delete the key
                            if self.agent.productsBought[product_id] <= 0:
                                del self.agent.productsBought[product_id]

                        # Add to productsReturned
                        if product_id in self.agent.productsReturned:
                            self.agent.productsReturned[product_id] += quantity
                        else:
                            self.agent.productsReturned[product_id] = quantity

                    # Define the probability for each category
                    category_probabilities = {
                        "Clothing": 0.8,  # 80% probability
                        "Fitness Gear": 0.8, # 80% probability
                        "Health": 0.5,  # 50% probability
                        "Supplements": 0.5, # 50% probability
                        "Food": 0.2,  # 20% probability
                        "Drinks": 0.2 # 20% probability
                    }

                    # Modify the loop to include probability checking
                    for product_id, quantity in products:
                        for product in self.agent.products:
                            if product.get_product_id() == product_id:
                                # Get the category of the product
                                category = product.get_category()
                                # Get the probability for the category
                                probability = category_probabilities.get(category, 0.5)  # Default to medium probability if category not listed
                                # Decide whether to add the product based on the category probability
                                if random.random() < probability:
                                    q = product.get_quantity()
                                    product.set_quantity(q + quantity)                            

            elif performative == "supply":
                supply = jsonpickle.decode(msg.body)

                for p in supply:
                    quantiy = p.get_quantity()
                    for product in self.agent.products:
                        if p.get_product_id() == product.get_product_id():
                            product.set_quantity(quantiy)

                print("StockManager {}".format(str(self.agent.jid)) + " updated the stock of product(s) supplied by Supplier " + str(msg.sender))

            else:
                print(f"Agent {self.agent.jid}: Message not understood!")     
        # else:
        #     print("Agent {}:".format(str(self.agent.jid)) + "Did not received any message after 10 seconds")


