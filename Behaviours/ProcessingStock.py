import jsonpickle
from spade.behaviour import CyclicBehaviour
from spade.message import Message

from Classes.Product import Product
from Classes.Purchase import Purchase
from Classes.Return import Return

class ProcessingStock_Behav(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=10) 
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

                    # for p in new_products:
                    #     print(p)                        

                    # Construct a list of dictionaries containing information for each available product
                    message_body = []
                    for product in new_products:
                        produto = Product(product.get_product_id(), product.get_name(), product.get_category(), product.get_price())
                        message_body.append(produto)

                    msg = Message(to=client) # msg.make_reply()
                    msg.body = jsonpickle.encode(self.agent.products) 
                    msg.set_metadata("performative", "inform")           
            
                    print("Agent {}:".format(str(self.agent.jid)) + " StockManager Agent informed Product(s) Available to Client Agent {}".format(client))
                    await self.send(msg)

                else :
                    request = jsonpickle.decode(msg.body)

                    if isinstance(request, Purchase):
                        lista_compras = request.getProducts()

                        # Dictionary to store the proposed quantities
                        proposed_quantities = {}
                        can_fulfill_order = True

                        # Check availability of each product requested
                        for product_id, requested_quantity in lista_compras:
                            found = False
                            for product in self.agent.products:
                                if product.get_product_id() == product_id:
                                    found = True
                                    available_quantity = product.get_quantity()
                                    if available_quantity < requested_quantity:
                                        # Not enough stock, propose available quantity
                                        proposed_quantities[product_id] = available_quantity
                                        can_fulfill_order = False
                                        print(f"Not enough stock for product {product_id}, available: {available_quantity}")
                                    else:
                                        # Enough stock, propose requested quantity
                                        proposed_quantities[product_id] = requested_quantity
                                    # break
                            if not found:
                                can_fulfill_order = False
                                print(f"Product {product_id} not found")

                        if not can_fulfill_order:
                            # If some items can't be fully supplied, send a negotiation proposal
                            negotiation_msg = Message(to=client) 
                            negotiation_msg.body = jsonpickle.encode(proposed_quantities)
                            negotiation_msg.set_metadata("performative", "propose")

                            print("Agent {}:".format(str(self.agent.jid)) + " StockManager Agent propose Client Agent {}".format(client))
                            await self.send(negotiation_msg)
                        else:
                            # If all items can be supplied, decrement the stock and confirm the order
                            for product_id, decrement in proposed_quantities.items():
                                for product in self.agent.products:
                                    if product.get_product_id() == product_id:
                                        new_quantity = product.get_quantity() - decrement
                                        product.set_quantity(new_quantity)
                                        # break

                            # Send confirmation to the delivery manager
                            confirmation_msg = Message(to=self.agent.get("deliveryman_contact"))
                            confirmation_msg.body = jsonpickle.encode(request)
                            confirmation_msg.set_metadata("performative", "request")

                            print("Agent {}:".format(str(self.agent.jid)) + " StockManager Agent requesting PurchaseDeliveryman to DeliverymanManager Agent {}".format(str(self.agent.get("deliveryman_contact"))))
                            await self.send(confirmation_msg)

                        # # Assume we can fulfill the delivery unless we find otherwise
                        # can_fulfill_order = True

                        # # First, check if all products can be supplied
                        # for product_id, decrement in lista_compras:
                        #     found = False
                        #     for product in self.agent.products:
                        #         if product.get_product_id() == product_id:
                        #             found = True
                        #             if product.get_quantity() < decrement:
                        #                 # Not enough stock
                        #                 can_fulfill_order = False
                        #                 print(f"Not enough stock for product {product_id}")

                        #                 NEGOCIATION HERE

                        #                 # Send the message to the deliveryman manager if the order can be fully supplied
                        #                 msg = Message(to=client)  
                        #                 msg.body = jsonpickle.encode(CHANGE)                         
                        #                 msg.set_metadata("performative", "propose")     

                        #                 print("Agent {}:".format(str(self.agent.jid)) + " StockManager Agent requesting PurchaseDeliveryman to DeliverymanManager Agent {}".format(client))
                        #                 await self.send(msg)
                        #             break
                        #     if not found:
                        #         can_fulfill_order = False
                        #         print(f"Product {product_id} not found")

                        # # Only proceed if all products can be supplied
                        # if can_fulfill_order:
                        #     # Now decrement the stock
                        #     for product_id, decrement in lista_compras:
                        #         for product in self.agent.products:
                        #             if product.get_product_id() == product_id:
                        #                 new_quantity = product.get_quantity() - decrement
                        #                 product.set_quantity(new_quantity)
                        #                 break

                        #     # PROCESSAR A MENSAGEM PARA O DELIVERY
                        #     # Send the message to the deliveryman manager if the order can be fully supplied
                        #     msg = Message(to=self.agent.get("deliveryman_contact"))  
                        #     msg.body = jsonpickle.encode(request)                         
                        #     msg.set_metadata("performative", "request")     

                        #     print("Agent {}:".format(str(self.agent.jid)) + " StockManager Agent requesting PurchaseDeliveryman to DeliverymanManager Agent {}".format(str(self.agent.get("deliveryman_contact"))))
                        #     await self.send(msg)
                        # else:
                        #     print("Unable to fulfill order due to insufficient stock or missing products.")
                    
                    elif isinstance(request, Return):

                        msg = Message(to=self.agent.get("deliveryman_contact"))       
                        msg.body = jsonpickle.encode(request)                         
                        msg.set_metadata("performative", "request")                   
            
                        print("Agent {}:".format(str(self.agent.jid)) + " StockManager Agent requesting ReturnDeliveryman to DeliverymanManager Agent {}".format(str(self.agent.get("deliveryman_contact"))))
                        await self.send(msg)
                        
                    else: print("Error2")

            elif performative == "accept_proposal":
                print("accept_proposal")
            
            elif performative == "reject_proposal":
                print("reject_proposal")

            # self.kill()  # kill the Processing_Behav 
        else:
            print("Agent {}:".format(str(self.agent.jid)) + "Did not received any message after 10 seconds")

    async def on_end(self): 
        await self.agent.stop()

