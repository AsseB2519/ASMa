from spade.behaviour import PeriodicBehaviour
from spade.message import Message

class StatsStock_Behav(PeriodicBehaviour):
    async def run(self):
        category_stats = {}  # Dictionary to hold stats by category
        total_products_bought = 0  # To track the total number of products bought across all categories
        total_products_returned = 0  # To track the total number of products returned across all categories

        # Loop through each purchased product
        for product_id, quantity in self.agent.productsBought.items():
            product = next((p for p in self.agent.products if p.get_product_id() == product_id), None)
            if product:
                category = product.get_category()
                if category not in category_stats:
                    category_stats[category] = {'total_quantity_bought': 0, 'total_price_bought': 0.0, 'total_quantity_returned': 0, 'total_price_returned': 0.0}

                # Update stats for purchases
                category_stats[category]['total_quantity_bought'] += quantity
                category_stats[category]['total_price_bought'] += product.get_price() * quantity
                total_products_bought += quantity  # Increment the total products bought counter

        # Loop through each returned product
        for product_id, quantity in self.agent.productsReturned.items():
            product = next((p for p in self.agent.products if p.get_product_id() == product_id), None)
            if product:
                category = product.get_category()
                if category not in category_stats:
                    category_stats[category] = {'total_quantity_bought': 0, 'total_price_bought': 0.0, 'total_quantity_returned': 0, 'total_price_returned': 0.0}

                # Update stats for returns
                category_stats[category]['total_quantity_returned'] += quantity
                category_stats[category]['total_price_returned'] += product.get_price() * quantity
                total_products_returned += quantity  # Increment the total products returned counter

        # Output statistics
        output = "Stats StockManager:\n"
        any_data = False  # Flag to check if there's any data to report

        # Aggregate stats by category
        for category, stats in category_stats.items():
            if stats['total_quantity_bought'] > 0 or stats['total_price_bought'] > 0 or stats['total_quantity_returned'] > 0 or stats['total_price_returned'] > 0:
                output += f"\t - Category: {category}: Bought - Total quantity: {stats['total_quantity_bought']}, Total price: ${stats['total_price_bought']:.2f}, Returned - Total quantity: {stats['total_quantity_returned']}, Total price: ${stats['total_price_returned']:.2f}\n"
                any_data = True

        # Print totals if any
        if total_products_bought > 0 or total_products_returned > 0:
            output += f"\t - Total products bought across all categories: {total_products_bought}\n"
            output += f"\t - Total products returned across all categories: {total_products_returned}\n"
            any_data = True

        # Only print if there's any data to report
        if any_data:
            print(output)