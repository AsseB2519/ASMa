import random
import jsonpickle

from spade.behaviour import OneShotBehaviour
from spade.message import Message

from Classes.Purchase import Purchase
from Classes.Product import Product

class Purchase_Behav (OneShotBehaviour): # Ou periodic?
    async def run(self):
        lista_compras = []
        for produto in self.agent.productsAvailable:
            quantidade = random.choices(range(11), weights=[50, 15, 10, 8, 7, 6, 5, 4, 3, 2, 1])[0]
            if quantidade != 0 :
                lista_compras.append(Product(produto,quantidade))

        # create Request class instance
        mr = Purchase(str(self.agent.jid), self.agent.position, lista_compras)
        print("Agent {}:".format(str(self.agent.jid)) + " Client Agent initialized with Purchase Request {}".format(mr.toString()))

        msg = Message(to=self.agent.get("service_contact"))             # Instantiate the message
        msg.body = jsonpickle.encode(mr)                                # Set the message content (serialized object)
        msg.set_metadata("performative", "request")                     # Set the message performative

        print("Agent {}:".format(str(self.agent.jid)) + " Client Agent requested purchase of Product(s) to Manager Agent {}".format(str(self.agent.get("service_contact"))))
        await self.send(msg)

