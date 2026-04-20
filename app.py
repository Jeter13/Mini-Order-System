from flask import Flask, request, jsonify, render_template
from flask_cors import CORS


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
CORS(app)

# API endpoint
@app.route("/orders", methods=["GET"])
def list_orders():
    orders = order_repo.list_all()
    return jsonify([{"id": o.id} for o in orders])

@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    order = order_repo.get(order_id)

    if order is None:
        return jsonify({"error": "Order not found"}), 404

    return jsonify({
        "order_id": order.id,
        "items": [
            {
                "product": item.product.name,
                "quantity": item.quantity,
                "subtotal": item.subtotal()
            }
            for item in order.items
        ],
        "total": order.total()
    })

@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    items = data.get("items", [])

    order = order_service.create_order(items)

    return jsonify({"message": "Order created", "order_id": order.id})

@app.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()

    product = Product(data["id"], data["name"], data["price"])
    product_repo.add(product)

    return jsonify({"message": "Product created"})

@app.route("/products", methods=["GET"])
def get_products():
    products = product_repo.list_all()
    return jsonify([
        {"id": p.id, "name": p.name, "price": p.price}
        for p in products
    ])

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
