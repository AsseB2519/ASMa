import random
import numpy as np
import jsonpickle
from spade.behaviour import CyclicBehaviour
from spade.message import Message

from Classes.Purchase import Purchase

class ReceiveStockAndPurchase_Behav(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=100)  
        if msg:
            performative = msg.get_metadata("performative")
            if performative == "inform":
                inform = jsonpickle.decode(msg.body)

                length = len(inform)

                # Função para gerar pesos com decaimento exponencial para decidir quantos produtos selecionar
                def generate_count_weights(n):
                    decay_factor = 0.4  # Ajuste para controlar a rapidez do decaimento
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
                    decay_factor = 0.4  # Ajuste conforme necessário
                    weights = [np.exp(-decay_factor * i) for i in range(1, max_quantity + 1)]
                    return weights / np.sum(weights)

                preco = 0
                tamanho = 0
                for product in selected_products:
                    # print(product.toString())
                    # max_quantity = 100
                    # max_quantity = product.get_quantity()
                    max_quantity = random.randint(2, 125)
                    quantity_weights = generate_quantity_weights(max_quantity)
                    selected_quantity = random.choices(range(1, max_quantity + 1), weights=quantity_weights)[0]
                    preco += selected_quantity * product.get_price()
                    tamanho += selected_quantity
                    lista_compras.append((product.get_product_id(), selected_quantity))

                self.agent.productsBought_notDelivered.append(lista_compras)

                purchase = Purchase(str(self.agent.jid), self.agent.position, lista_compras)

                msg = Message(to=self.agent.get("stockmanager_contact"))             
                msg.body = jsonpickle.encode(purchase)                               
                msg.set_metadata("performative", "purchase")

                # print("Agent {}:".format(str(self.agent.jid)) + " Client Agent Purchase Product(s) to StockManager Agent {}".format(str(self.agent.get("stockmanager_contact"))))
                print(f"Client {self.agent.jid} purchase {tamanho} product(s) paying {preco:.2f}€ to StockManager {self.agent.get('stockmanager_contact')}")
                await self.send(msg)

            elif performative == "propose":
                    propose = jsonpickle.decode(msg.body)
                    # products = propose.getProducts()
                    
                    # Randomly decide to accept or deny the proposal
                    actions = ["accept_proposal", "reject_proposal"]
                    probabilities = [0.75, 0.25]  
                    decision = random.choices(actions, weights=probabilities)[0]

                    lista_compras_neg = []

                    for p in propose:
                        lista_compras_neg.append((p.get_product_id(), p.get_quantity()))

                    purchase = Purchase(str(self.agent.jid), self.agent.position, lista_compras_neg)
                    
                    msg = Message(to=self.agent.get("stockmanager_contact"))             
                    msg.body = jsonpickle.encode(purchase)                               
                    msg.set_metadata("performative", decision)

                    if decision == "accept_proposal":
                        print(f"Client {str(self.agent.jid)} accepts proposal from StockManager {str(self.agent.get('stockmanager_contact'))}")
                    else:
                        print(f"Client {str(self.agent.jid)} rejects proposal from StockManager {str(self.agent.get('stockmanager_contact'))}")

                    await self.send(msg)

            elif performative == "delivery": 
                print("Agent {}:".format(str(self.agent.jid)) + " Client Agent received the package from Deliveryman Agent {}".format(str(msg.sender)))

                lista_compras = self.agent.productsBought_notDelivered[0] 

                for product, quantity in lista_compras:
                    if product in self.agent.productsBought:
                        self.agent.productsBought[product] += quantity
                    else:
                        self.agent.productsBought[product] = quantity

                self.agent.productsBought_notDelivered.pop(0)

            elif performative == "refund": 
                print("Client {}".format(str(self.agent.jid)) + " handed over the refund products to Deliveryman {}".format(str(msg.sender)))    

            else:
                print(f"Agent {self.agent.jid}: Message not understood!")   