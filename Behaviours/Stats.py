from spade.behaviour import PeriodicBehaviour
from spade.message import Message

class Stats_Behav(PeriodicBehaviour):
    async def run(self):
        print("to be implemented")
        # threshold = 0.5  # 50% threshold
        # low_products = [product for product in self.agent.products if product.get_quantity < threshold * product.max_quantity]

        # if low_products:
        #     msg = Message(to=self.agent.get('supplier_contact'))   
        #     msg.body = "Request Supply"               
        #     msg.set_metadata("performative", "request")

        #     print("Agent {}:".format(str(self.agent.jid)) + " StockManager Agent requested stock to Supplier Agent {}".format(str(self.agent.get("supplier_contact"))))
        #     await self.send(msg)          