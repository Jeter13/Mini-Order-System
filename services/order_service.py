import sys
from domain.order import Order
from domain.order_item import OrderItem


class OrderService:
    def __init__(self, product_repo, order_repo):
        self.product_repo = product_repo
        self.order_repo = order_repo
        self._next_order_id = 1  # simple ID generator

    def create_order(self, items_data):
        """
        items_data: list of (product_id, quantity)
        """

        # Rule 3: Order must have at least one item
        if not items_data:
            print("Order must contain at least one item.")
            sys.exit()

        order = Order(order_id=self._next_order_id)

        for product_id, quantity in items_data:

            # Rule 2: Quantity must be > 0
            if quantity <= 0:
                print(f"Invalid quantity ({quantity}) for product {product_id}.")
                sys.exit()

            # Rule 1: Product must exist
            product = self.product_repo.get(product_id)
            if product is None:
               print(f"Product with id {product_id} does not exist.")
               sys.exit()

            order.add_item(OrderItem(product, quantity))

        # Save order
        self.order_repo.save(order)
        self._next_order_id += 1

        return order

    def get_order(self, order_id):
        order = self.order_repo.get(order_id)
        if order is None:
            print(f"Order with id {order_id} not found.")
            sys.exit()
        return order

    def get_order_total(self, order_id):
        order = self.get_order(order_id)  # reuse logic + error handling
        return order.total()