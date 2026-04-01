class Order:
    def __init__(self, order_id):
        self.id = order_id
        self.items = []

    def add_item(self, order_item):
        self.items.append(order_item)

    def total(self):
        return sum(item.subtotal() for item in self.items)

    def display(self):
        for item in self.items:
            print(f"Item: {item.product.name} x{item.quantity} = ${item.subtotal():.2f}")
        print(f"Total = ${self.total():.2f}")