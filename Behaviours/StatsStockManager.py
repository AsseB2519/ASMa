from spade.behaviour import PeriodicBehaviour
from spade.message import Message

class StatsStock_Behav(PeriodicBehaviour):
    async def run(self):
        category_stats = {}  # Dictionary to hold stats by category
        total_products_bought = 0  # To track the total number of products bought across all categories

        # Loop through each purchased product
        for product_id, quantity in self.agent.productsBought.items():
            product = next((p for p in self.agent.products if p.get_product_id() == product_id), None)
            if product:
                category = product.get_category()
                if category not in category_stats:
                    category_stats[category] = {'total_quantity': 0, 'total_price': 0.0}

                # Update stats for this category
                category_stats[category]['total_quantity'] += quantity
                category_stats[category]['total_price'] += product.get_price() * quantity
                total_products_bought += quantity  # Increment the total products bought counter

        # Output statistics
        output = "Stats ProductManager:\n"
        any_data = False  # Flag to check if there's any data to report

        # Aggregate stats by category
        for category, stats in category_stats.items():
            if stats['total_quantity'] > 0 or stats['total_price'] > 0:
                output += f"\t - Category: {category}: Total quantity: {stats['total_quantity']}, Total price: ${stats['total_price']:.2f}\n"
                any_data = True

        # Print total products bought if any
        if total_products_bought > 0:
            output += f"\t - Total products bought across all categories: {total_products_bought}\n"
            any_data = True

        # Only print if there's any data to report
        if any_data:
            print(output)
