from domain.product import Product
from repository.product_repo import ProductRepository
from repository.order_repo import OrderRepository
from services.order_service import OrderService


def main():
    # Initialize repositories
    product_repo = ProductRepository()
    order_repo = OrderRepository()

    # Initialize service
    order_service = OrderService(product_repo, order_repo)

    # Add products
    product_repo.add(Product(1, "Mug", 12.50))
    product_repo.add(Product(2, "Scarf", 25.00))

    # Create order via service
    order = order_service.create_order([
        (1,2),
        (2,1)
    ])

    # Display order
    order.display()

if __name__ == "__main__":
    main()
