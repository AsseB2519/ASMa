from spade.behaviour import PeriodicBehaviour
from collections import Counter

class StatsDeliveryman_Behav(PeriodicBehaviour):
    async def run(self):
        # Dictionary to track deliveries per client
        client_deliveries = Counter()
        client_returns = Counter()

        # Calculate the total weight of products to be delivered and count deliveries
        total_to_be_delivered = 0
        for delivery in self.agent.products_to_be_delivered.values():
            total_to_be_delivered += delivery.getWeight()

        # Calculate the total weight of products already delivered and count deliveries
        total_delivered = 0
        for delivery in self.agent.products_delivered.values():
            total_delivered += delivery.getWeight()
            client_deliveries[delivery.getAgent()] += 1

        # Calculate the total weight of products to be returned and count deliveries
        total_to_be_returned = 0
        for delivery in self.agent.products_to_be_return.values():
            total_to_be_returned += delivery.getWeight()

        # Calculate the total weight of products returned and count deliveries
        total_returned = 0
        for delivery in self.agent.products_returned.values():
            total_returned += delivery.getWeight()
            client_returns[delivery.getAgent()] += 1

        # Determine the best client (the one with the most deliveries)
        best_client, max_deliveries = client_deliveries.most_common(1)[0] if client_deliveries else ("None", 0)
        worst_client, max_returns = client_returns.most_common(1)[0] if client_returns else ("None", 0)

        # # Print statistics if there are any products handled
        # if total_to_be_delivered or total_delivered or total_to_be_returned or total_returned or max_returns or max_deliveries:
        #     print(f"Stats DeliverymanManager:\n"
        #             f"\t - Total weight of products to be delivered: {total_to_be_delivered:.2f} kg\n"
        #             f"\t - Total weight of products delivered: {total_delivered:.2f} kg\n"
        #             f"\t - Total weight of products to be returned: {total_to_be_returned:.2f} kg\n"
        #             f"\t - Total weight of products returned: {total_returned:.2f} kg\n"
        #             f"\t - Client with most deliveries: {best_client} with {max_deliveries} deliveries\n"
        #             f"\t - Client with most returns: {worst_client} with {max_returns} deliveries")

        if total_to_be_delivered or total_delivered or total_to_be_returned or total_returned or max_deliveries or max_returns:
            output = "Stats DeliverymanManager:\n"
            if total_to_be_delivered:
                output += f"\t - Total weight of products to be delivered: {total_to_be_delivered:.2f} kg\n"
            if total_delivered:
                output += f"\t - Total weight of products delivered: {total_delivered:.2f} kg\n"
            if total_to_be_returned:
                output += f"\t - Total weight of products to be returned: {total_to_be_returned:.2f} kg\n"
            if total_returned:
                output += f"\t - Total weight of products returned: {total_returned:.2f} kg\n"
            if max_deliveries > 0:  # Assumes max_deliveries is an integer count
                output += f"\t - Client with most deliveries: {best_client} with {max_deliveries} deliveries\n"
            if max_returns > 0:  # Assumes max_returns is an integer count
                output += f"\t - Client with most returns: {worst_client} with {max_returns} returns\n"

            print(output)