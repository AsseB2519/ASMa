# class ClientProducts:
#     def __init__(self, client_jid: str, product_managers: list):
#         self.client_jid = client_jid
#         self.product_managers = product_managers

#     def get_client_jid(self) -> str:
#         return self.client_jid

#     def set_client_jid(self, client_jid: str) -> None:
#         self.client_jid = client_jid

#     def get_product_managers(self) -> list:
#         return self.product_managers

#     def set_product_managers(self, product_managers: list) -> None:
#         self.product_managers = product_managers

#     def toString(self) -> str:
#         return f"Client JID: {self.client_jid}, Products: {[product_manager.toString() for product_manager in self.product_managers]}"        

from typing import List

from Classes.Product_Manager import Product_Manager

class ClientProducts:
    def __init__(self, client_jid: str, product_managers: List['Product_Manager']):
        self.client_jid = client_jid
        self.product_managers = product_managers

    def get_client_jid(self) -> str:
        return self.client_jid

    def set_client_jid(self, client_jid: str) -> None:
        self.client_jid = client_jid

    def get_product_managers(self) -> List['Product_Manager']:
        return self.product_managers

    def set_product_managers(self, product_managers: List['Product_Manager']) -> None:
        self.product_managers = product_managers

    def toString(self) -> str:
        return f"Client JID: {self.client_jid}, Products: {[product_manager.toString() for product_manager in self.product_managers]}" 