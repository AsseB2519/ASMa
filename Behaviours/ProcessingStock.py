import jsonpickle
from spade.behaviour import CyclicBehaviour
from spade.message import Message

from Classes.ClientProducts import ClientProducts

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

                # stock_request = jsonpickle.decode(msg.body)

                # products = stock_request.getProducts()
                
                # flag = True
                # for p in products:
                #     if p.name in self.agent.products:
                #         if self.agent.products[p.name] < p.number:
                #             flag = False
                #             # Continuar Compra
                #         # else:
                #         #     print("Not available Stock of Product" + p.name)
                #         #     # Informar Cliente que não existe Stock
                #     else: 
                #         print("Error Product " + p.name + " does not exists")
                        
                        
                # # print(self.agent.products)

            # self.kill()  # kill the ReplyBehav
            if performative == "inform":
                print("A remover do meu Stock")
                

        else:
            print("Agent {}:".format(str(self.agent.jid)) + "Did not received any message after 10 seconds")

    async def on_end(self):  # on ReplyStockBehav end, kill the respective Customer Agent
        await self.agent.stop()

