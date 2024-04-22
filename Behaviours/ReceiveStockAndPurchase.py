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

                length = len(inform)

                # Função para gerar pesos com decaimento exponencial para decidir quantos produtos selecionar
                def generate_count_weights(n):
                    decay_factor = 0.5  # Ajuste para controlar a rapidez do decaimento
                    weights = [np.exp(-decay_factor * i) for i in range(n)]
                    return weights / np.sum(weights)

                # Decidindo quantos produtos selecionar
                count_weights = generate_count_weights(length)
                number_of_products_to_select = random.choices(range(1, length + 1), weights=count_weights, k=1)[0]

                # Selecionando produtos aleatoriamente
                selected_products = random.sample(inform, k=number_of_products_to_select)

                lista_compras = []

                # Função para gerar pesos com decaimento exponencial para a seleção de quantidades
                def generate_quantity_weights(max_quantity):
                    decay_factor = 0.5  # Ajuste conforme necessário
                    weights = [np.exp(-decay_factor * i) for i in range(1, max_quantity + 1)]
                    return weights / np.sum(weights)

                for product in selected_products:
                    max_quantity = product.get_quantity()
                    quantity_weights = generate_quantity_weights(max_quantity)
                    selected_quantity = random.choices(range(1, max_quantity + 1), weights=quantity_weights)[0]
                    lista_compras.append((product.get_product_id(), selected_quantity))

                # for p in lista_compras:
                #     print(p)
                    
                for product, quantity in lista_compras:
                    if product in self.agent.productsBought:
                        self.agent.productsBought[product] += quantity
                    else:
                        self.agent.productsBought[product] = quantity

                purchase = Purchase(str(self.agent.jid), self.agent.position, lista_compras)

                msg = Message(to=self.agent.get("stockmanager_contact"))             
                msg.body = jsonpickle.encode(purchase)                               
                msg.set_metadata("performative", "request")

                print("Agent {}:".format(str(self.agent.jid)) + " Client Agent Purchase Product(s) to StockManager Agent {}".format(str(self.agent.get("stockmanager_contact"))))
                await self.send(msg)

            else: print("Error3")