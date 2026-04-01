from domain.product import Product
from domain.order_item import OrderItem
from domain.order import Order
from repository.product_repo import ProductRepository
from repository.order_repo import OrderRepository


def main():
    # Initialize repositories
    product_repo = ProductRepository()
    order_repo = OrderRepository()

    # Add products
    product_repo.add(Product(1, "Mug", 12.50))
    product_repo.add(Product(2, "Scarf", 25.00))

    # Retrieve products
    mug = product_repo.get(1)
    scarf = product_repo.get(2)

    # Create order
    order = Order(order_id=1)
    order.add_item(OrderItem(mug, 2))
    order.add_item(OrderItem(scarf, 1))

    # Save order
    order_repo.save(order)

    # Retrieve and display order
    saved_order = order_repo.get(1)
    saved_order.display()

if __name__ == "__main__":
    main()