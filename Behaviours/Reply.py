import jsonpickle
from spade.behaviour import CyclicBehaviour

class ReplyBehav(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=10)  # wait for a message for 10 seconds
        if msg:
            # Message Threatment based on different Message performatives
            performative = msg.get_metadata("performative")
            if performative == "request":
                print("Agent {}:".format(str(self.agent.jid)) + " Client Agent {} requested a Product!".format(str(msg.sender)))
                # transport_request = jsonpickle.decode(msg.body)
                # print(transport_request)
            # elif performative == "refuse":
            #     print("Agent {}:".format(str(self.agent.jid)) + " No Transport available!")
            # else:
            #     print("Agent {}:".format(str(self.agent.jid)) + " Message not understood!")

            self.kill()  # kill the ReplyBehav

        else:
            print("Agent {}:".format(str(self.agent.jid)) + "Did not received any message after 10 seconds")

    async def on_end(self):  # on ReplyBehav end, kill the respective Customer Agent
        await self.agent.stop()

