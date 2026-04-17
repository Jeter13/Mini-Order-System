from flask import Flask, jsonify
from domain.product import Product
from repository.product_repo import ProductRepository
from repository.order_repo import OrderRepository
from services.order_service import OrderService

# Initialize repositories
product_repo = ProductRepository()
order_repo = OrderRepository()

# Initialize service
order_service = OrderService(product_repo, order_repo)

# Add products
product_repo.add(Product(1, "Mug", 12.50))
product_repo.add(Product(2, "Scarf", 25.00))

# Create order via service
order_service.create_order([
    (1,2),
    (2,1)
])

app = Flask(__name__)

# API endpoint
@app.route('/products', methods=['GET'])
def get_products():
    products = product_repo.list_all()

    result = []
    for p in products:
        result.append({
            "id": p.id,
            "name": p.name,
            "price": p.price
        })

    return jsonify(result)


@app.route('/order/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = order_repo.get(order_id)

    if order is None:
        return jsonify({'message': 'Order not found'})

    items = []
    for item in order.items:
        items.append({
            "product": item.product.name,
            "quantity": item.quantity,
            "subtotal": item.subtotal()
        })

    response = {
        "order_id": order.id,
        "items": items,
        "total": order.total()
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
