import jsonpickle
from spade.behaviour import CyclicBehaviour
from spade.message import Message

class StockProcessing_Behav(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=10)  # wait for a message for 10 seconds
        if msg:
            # Message Threatment based on different Message performatives
            performative = msg.get_metadata("performative")
            if performative == "request":
                # print("Agent {}:".format(str(self.agent.jid)) + " Client Agent {} requested Product(s)!".format(str(msg.sender)))
                stock_request = jsonpickle.decode(msg.body)

                products = stock_request.getProducts()
                
                flag = True
                for p in products:
                    if p.name in self.agent.products:
                        if self.agent.products[p.name] > p.number:
                            print("Available Stock of Product" + p.name)
                            # Continuar Compra
                        else:
                            print("Not available Stock of Product" + p.name)
                            # Informar Cliente que não existe Stock
                    else: 
                        print("Error Product " + p.name + " does not exists")
                        
                        
                # print(self.agent.products)

            self.kill()  # kill the ReplyBehav

        else:
            print("Agent {}:".format(str(self.agent.jid)) + "Did not received any message after 10 seconds")

    async def on_end(self):  # on ReplyStockBehav end, kill the respective Customer Agent
        await self.agent.stop()

