import random
import jsonpickle

from spade.behaviour import OneShotBehaviour
from spade.message import Message

from Classes.Position import Position
from Classes.Purchase_or_Return import Purchase_or_Return
from Classes.Product import Product

class Purchase_Behav (OneShotBehaviour): # Ou periodic?
    async def run(self):
        init = Position(random.randint(1, 100), random.randint(1, 100))

        lista_compras = []
        for produto in self.agent.products:
            quantidade = random.choices(range(11), weights=[50, 15, 10, 8, 7, 6, 5, 4, 3, 2, 1])[0]
            if quantidade != 0 :
                lista_compras.append(Product(produto,quantidade))

        purchase = True
        # create Request class instance
        mr = Purchase_or_Return(str(self.agent.jid), init, lista_compras, purchase)
        print("Agent {}:".format(str(self.agent.jid)) + " Client Agent initialized with Request {}".format(mr.toString()))

        msg = Message(to=self.agent.get("service_contact"))             # Instantiate the message
        msg.body = jsonpickle.encode(mr)                                # Set the message content (serialized object)
        msg.set_metadata("performative", "request")                     # Set the message performative

        print("Agent {}:".format(str(self.agent.jid)) + " Client Agent requested Product(s) to Manager Agent {}".format(str(self.agent.get("service_contact"))))
        await self.send(msg)

