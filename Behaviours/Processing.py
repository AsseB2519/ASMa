from ast import Return
import jsonpickle
from spade.behaviour import CyclicBehaviour
from spade.message import Message

from Classes.Product import Product
from Classes.Purchase import Purchase
from Classes.Product_Manager import Product_Manager

class Processing_Behav(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=10) 
        if msg:
            # Message Threatment based on different Message performatives
            performative = msg.get_metadata("performative")
            if performative == "request":
                if msg.body == "Request Products Available":
                    client = msg.sender
                    string = str(client) + ":Request Products Available" 

                    msg = Message(to=self.agent.get("stock_contact"))
                    msg.body = jsonpickle.encode(string) 
                    msg.set_metadata("performative", "request")           
            
                    print("Agent {}:".format(str(self.agent.jid)) + " Manager Agent requesting Product(s) to StockManager Agent {}".format(str(self.agent.get("stock_contact"))))
                    await self.send(msg)

                else :
                    request = jsonpickle.decode(msg.body)
                    if isinstance(request, Purchase):
                        # Fazer tratamento da infornação
                        # Stock - ProdutosComprados lista de tuplos (id, quantidade)
                        # DeliveryMan - tudo
                        inform = request

                        # Mandar para StockManager
                        msg = Message(to=self.agent.get("stock_contact"))             
                        msg.body = jsonpickle.encode(inform)                         
                        msg.set_metadata("performative", "inform")                   
            
                        print("Agent {}:".format(str(self.agent.jid)) + " Manager Agent informed the Product(s) purchase to StockManager Agent {}".format(str(self.agent.get("stock_contact"))))
                        await self.send(msg)

                        # Mandar para DeliverymanManager 
                        msg2 = Message(to=self.agent.get("deliveryman_contact"))  
                        msg2.body = jsonpickle.encode(request)                         
                        msg2.set_metadata("performative", "request")                   
            
                        print("Agent {}:".format(str(self.agent.jid)) + " Manager Agent requesting Deliveryman to DeliverymanManager Agent {}".format(str(self.agent.get("deliveryman_contact"))))
                        await self.send(msg2)

                    elif isinstance(request, Return):
                        # Mandar para DeliverymanManager IGNORAR POR AGORA
                        msg = Message(to=self.agent.get("deliveryman_contact"))       
                        msg.body = jsonpickle.encode(request)                         
                        msg.set_metadata("performative", "request")                   
            
                        print("Agent {}:".format(str(self.agent.jid)) + " Manager Agent requesting Product(s) Stock to DeliverymanManager Agent {}".format(str(self.agent.get("deliveryman_contact"))))
                        await self.send(msg)
                        
                    else: print("Error2")

            elif performative == "inform":
                inform = jsonpickle.decode(msg.body)

                client = inform.get_client_jid()
                products = inform.get_product_managers()

                # self.agent.productsAvailable = products

                new_products = []
                for p in products:
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

                # for p in message_body:
                    # print(p)

                msg = Message(to=client)             
                msg.body = jsonpickle.encode(products)                         
                msg.set_metadata("performative", "inform") 

                print("Agent {}:".format(str(self.agent.jid)) + " Manager Agent informed Product(s) Available to Client Agent {}".format(client))
                await self.send(msg)

            # self.kill()  # kill the Processing_Behav 
        else:
            print("Agent {}:".format(str(self.agent.jid)) + "Did not received any message after 10 seconds")

    async def on_end(self): 
        await self.agent.stop()

