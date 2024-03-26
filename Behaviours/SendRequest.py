import random

from spade.behaviour import OneShotBehaviour
from spade.message import Message

from Classes.Position import Position
from Classes.MakeRequest import MakeRequest

import jsonpickle

class SendRequest_Behav (OneShotBehaviour): # Ou periodic?
    async def run(self):
        init = Position(random.randint(1, 100), random.randint(1, 100))
        product = random.choice(self.agent.products)

        # create Request class instance
        mr = MakeRequest(str(self.agent.jid), init, product)
        print("Agent {}:".format(str(self.agent.jid)) + " Client Agent initialized with Request {}".format(mr.toString()))

        msg = Message(to=self.agent.get("service_contact"))             # Instantiate the message
        msg.body = jsonpickle.encode(mr)                                # Set the message content (serialized object)
        msg.set_metadata("performative", "request")                     # Set the message performative

        print("Agent {}:".format(str(self.agent.jid)) + " Client Agent requesting Product to Manager Agent {}".format(str(self.agent.get("service_contact"))))
        await self.send(msg)

