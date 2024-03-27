import jsonpickle
from spade.behaviour import CyclicBehaviour
from spade.message import Message

class Processing_Behav(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=10)  # wait for a message for 10 seconds
        if msg:
            # Message Threatment based on different Message performatives
            performative = msg.get_metadata("performative")
            if performative == "request":
                print("Agent {}:".format(str(self.agent.jid)) + " Client Agent {} requested Product(s)!".format(str(msg.sender)))
                request = jsonpickle.decode(msg.body)
                client = str(msg.sender)
                purchase = request.getPurchase()

                if purchase:
                    # Mandar para Cliente - Pedido a ser Processado
                    # print("Pedido a ser Processado")
                    inform_msg = Message(to=client)                              # Instantiate the inform message
                    inform_msg.body = "Request to be Processed"                  # Set the message content
                    inform_msg.set_metadata("performative", "inform")            # Set the message performative
                    await self.send(inform_msg)                                 # Send the inform message

                    print("Agent {}:".format(str(self.agent.jid)) + " Manager Agent informed Product Processing to Client Agent {}".format(client))

                    # Mandar para StockManager
                    # print("Purchase")
                    # print("Agent {}:".format(str(self.agent.jid)) + " Client Agent initialized with Request {}".format(request.toString()))
                    
                    msg = Message(to=self.agent.get("stock_contact"))             # Instantiate the message
                    msg.body = jsonpickle.encode(request)                         # Set the message content (serialized object)
                    msg.set_metadata("performative", "request")                   # Set the message performative
        
                    print("Agent {}:".format(str(self.agent.jid)) + " Manager Agent requesting Product(s) Stock to StockManager Agent {}".format(str(self.agent.get("stock_contact"))))
                    await self.send(msg)
                else: 
                    print("Devolução")

            self.kill()  # kill the ReplyBehav

        else:
            print("Agent {}:".format(str(self.agent.jid)) + "Did not received any message after 10 seconds")

    async def on_end(self):  # on ReplyBehav end, kill the respective Customer Agent
        await self.agent.stop()

