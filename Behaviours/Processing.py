from ast import Return
import jsonpickle
from spade.behaviour import CyclicBehaviour
from spade.message import Message

from Classes.Purchase import Purchase

class Processing_Behav(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=10) 
        if msg:
            # Message Threatment based on different Message performatives
            performative = msg.get_metadata("performative")
            if performative == "request":
                if msg.body == "Request Products Available":

                    msg = Message(to=self.agent.get("stock_contact"))             
                    msg.body = "Request Products Available"               
                    msg.set_metadata("performative", "request")           
            
                    print("Agent {}:".format(str(self.agent.jid)) + " Manager Agent requesting Product(s) to StockManager Agent {}".format(str(self.agent.get("stock_contact"))))
                    await self.send(msg)

                else :
                    request = jsonpickle.decode(msg.body)
                    
                    if isinstance(request, Purchase):
                        # Mandar para StockManager
                        msg = Message(to=self.agent.get("stock_contact"))             
                        msg.body = jsonpickle.encode(request)                         
                        msg.set_metadata("performative", "request")                   
            
                        print("Agent {}:".format(str(self.agent.jid)) + " Manager Agent requesting Product(s) to StockManager Agent {}".format(str(self.agent.get("stock_contact"))))
                        await self.send(msg)

                    elif isinstance(request, Return):
                        # Mandar para DeliverymanManager IGNORAR POR AGORA
                        msg = Message(to=self.agent.get("deliveryman_contact"))       
                        msg.body = jsonpickle.encode(request)                         
                        msg.set_metadata("performative", "request")                   
            
                        print("Agent {}:".format(str(self.agent.jid)) + " Manager Agent requesting Product(s) Stock to DeliverymanManager Agent {}".format(str(self.agent.get("deliveryman_contact"))))
                        await self.send(msg)
                        
                    else: print("Error")

            elif performative == "inform":
                inform = jsonpickle.decode(msg.body)
                self.agent.productsAvailable = inform

                products = [(product, quantity) for product, quantity in self.agent.productsAvailable.items() if quantity > 0]

                client = "client1@laptop-ci4qet97"
                msg = Message(to=client)             
                msg.body = jsonpickle.encode(products)                         
                msg.set_metadata("performative", "inform") 

                # print(self.agent.productsAvailable)

                print("Agent {}:".format(str(self.agent.jid)) + " Manager Agent informed Product(s) Available to Client Agent {}".format(client))
                await self.send(msg)

            # self.kill()  # kill the Processing_Behav 
        else:
            print("Agent {}:".format(str(self.agent.jid)) + "Did not received any message after 10 seconds")

    async def on_end(self): 
        await self.agent.stop()

