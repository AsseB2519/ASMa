import random
import numpy as np
import jsonpickle
from spade.behaviour import CyclicBehaviour
from spade.message import Message

from Classes.Purchase import Purchase

class ReceiveStockAndPurchase_Behav(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=10)  # wait for a message for 10 seconds
        if msg:
            performative = msg.get_metadata("performative")
            if performative == "inform":
                inform = jsonpickle.decode(msg.body)

                #self.agent.productsAvailable = inform

                # Randomly select 5 products and choose random quantity for each
                selected_products = random.sample(inform, 5)
                lista_compras = []
                for product in selected_products:
                    selected_quantity = random.randint(1, product.get_quantity())
                    lista_compras.append((product, selected_quantity))
                
                # Parâmetro que controla o decaimento da probabilidade
                decay_rate = 0.5

                # Número máximo de itens
                max_quantity = 10

                # Gerar os pesos
                pesos = [1 / ((i+1) ** decay_rate) for i in range(max_quantity)]

                # Normalizar os pesos para que a soma seja 1
                pesos = np.array(pesos) / np.sum(pesos)

                for product in selected_products:
                    # Escolhe uma quantidade baseada nos pesos
                    selected_quantity = random.choices(range(1, product.get_quantity() + 1), weights=[1 / ((i+1) ** decay_rate) for i in range(product.get_quantity())])[0]
                    lista_compras.append((product, selected_quantity))

                # Print selected products and quantities saved in tuples
                print("Selected Products with Quantity:")
                for product, quantity in lista_compras:
                    print(f"Product: {product.get_product_id()}, Quantity: {quantity}")

                #for produto in inform: 
                #    quantidade = random.choices(range(11), weights=[50, 15, 10, 8, 7, 6, 5, 4, 3, 2, 1])[0]
                #    if quantidade != 0 :
                #        lista_compras.append(Product(produto, quantidade))
                #        if produto in self.agent.productsBought:
                #            self.agent.productsBought[produto] += quantidade
                #        else:
                #            self.agent.productsBought[produto] = quantidade

                purchase = Purchase(str(self.agent.jid), self.agent.position, lista_compras)

                msg = Message(to=self.agent.get("service_contact"))             
                msg.body = jsonpickle.encode("")                               
                msg.set_metadata("performative", "request")

                print("Agent {}:".format(str(self.agent.jid)) + " Client Agent Purchase Product(s) -> Manager Agent {}".format(str(self.agent.get("service_contact"))))
                await self.send(msg)

            else: print("Error3")