import jsonpickle
from spade.behaviour import CyclicBehaviour
from spade.message import Message

from Classes.ClientProducts import ClientProducts
from Classes.Product_Manager import Product_Manager

class ProcessingStock_Behav(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=10)  # wait for a message for 10 seconds
        if msg:
            # Message Threatment based on different Message performatives
            performative = msg.get_metadata("performative")
            if performative == "request":
                parts = msg.body.split(":")
                if len(parts) == 2:
                    client = parts[0].replace('"', '')  
                    message = parts[1].replace('"', '')  

                    if message.strip() == "Request Products Available":
                        # string = str(client) + ":" + str(self.agent.products) 

                        enviar = ClientProducts(str(client), self.agent.products)

                        # Stock Available mandar para o Managers
                        msg = Message(to=self.get("service_contact"))  
                        msg.body = jsonpickle.encode(enviar)
                        msg.set_metadata("performative", "inform")                    
                        
                        print("Agent {}:".format(str(self.agent.jid)) + " Stock Manager Agent informed Product(s) Available to Manager Agent {}".format(str(self.agent.get("service_contact"))))
                        await self.send(msg)

            if performative == "inform":
                request = jsonpickle.decode(msg.body)

                lista_compras = request.getProducts()

                # for p in lista_compras:
                    # print(p)

                # Iterating over the list of tuples (product_id, decrement)
                for product_id, decrement in lista_compras:
                    # Searching for the product in self.products by product_id
                    found = False

                    for product in self.agent.products:
                        if product.get_product_id() == product_id:
                            found = True
                            # Checking if there's enough quantity to decrement
                            if product.get_quantity() >= decrement:
                                new_quantity = product.get_quantity() - decrement
                                product.set_quantity(new_quantity)
                                # print(f"Quantity of product {product.name} updated. New quantity: {product.quantity}")
                            else:
                                print("Not enough stock to decrement")
                                # É preciso ver quando o Stock acaba
                                # Negociação aqui
                            break
                    if not found:
                        print("Product not found")

        else:
            print("Agent {}:".format(str(self.agent.jid)) + "Did not received any message after 10 seconds")

    async def on_end(self):  
        await self.agent.stop()

