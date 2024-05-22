from flask import Blueprint, request, jsonify
from models import db, Product, Customer, CartItem, Order, OrderItem

api = Blueprint('api', __name__)

@api.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

@api.route('/products', methods=['POST'])
def add_product():
    data = request.json
    new_product = Product(name=data['name'], price=data['price'], description=data.get('description'))
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201

@api.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([customer.to_dict() for customer in customers])

@api.route('/customers', methods=['POST'])
def add_customer():
    data = request.json
    new_customer = Customer(name=data['name'], email=data['email'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify(new_customer.to_dict()), 201

@api.route('/customers/<int:customer_id>/cart', methods=['POST'])
def add_to_cart(customer_id):
    data = request.json
    cart_item = CartItem(customer_id=customer_id, product_id=data['product_id'], quantity=data['quantity'])
    db.session.add(cart_item)
    db.session.commit()
    return jsonify(cart_item.to_dict()), 201

@api.route('/customers/<int:customer_id>/cart', methods=['GET'])
def view_cart(customer_id):
    cart_items = CartItem.query.filter_by(customer_id=customer_id).all()
    return jsonify([item.to_dict() for item in cart_items])

@api.route('/customers/<int:customer_id>/checkout', methods=['POST'])
def checkout(customer_id):
    cart_items = CartItem.query.filter_by(customer_id=customer_id).all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    new_order = Order(customer_id=customer_id, total_price=total_price)
    db.session.add(new_order)
    db.session.flush()
    
    for item in cart_items:
        order_item = OrderItem(order_id=new_order.id, product_id=item.product_id, quantity=item.quantity, price=item.product.price)
        db.session.add(order_item)
        db.session.delete(item)
    
    db.session.commit()
    return jsonify(new_order.to_dict()), 201

@api.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([order.to_dict() for order in orders])

def register_routes(app):
    app.register_blueprint(api, url_prefix='/api')
