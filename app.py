from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# FakeStore API endpoints
API_BASE_URL = "https://fakestoreapi.com"
PRODUCTS_URL = f"{API_BASE_URL}/products"
CATEGORIES_URL = f"{PRODUCTS_URL}/categories"

def get_products(category=None):
    url = PRODUCTS_URL
    if category:
        url = f"{PRODUCTS_URL}/category/{category}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else []

def get_product(product_id):
    url = f"{PRODUCTS_URL}/{product_id}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

def get_categories():
    response = requests.get(CATEGORIES_URL)
    return response.json() if response.status_code == 200 else []

def initialize_cart():
    if 'cart' not in session:
        session['cart'] = []

@app.route('/')
def home():
    products = get_products()
    categories = get_categories()
    return render_template('index.html', products=products, categories=categories)

@app.route('/category/<category_name>')
def category(category_name):
    products = get_products(category_name)
    categories = get_categories()
    return render_template('category.html', 
                         products=products, 
                         categories=categories,
                         current_category=category_name)

@app.route('/product/<int:product_id>')
def product(product_id):
    product = get_product(product_id)
    return render_template('product.html', product=product)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    initialize_cart()
    product_id = int(request.form.get('product_id'))
    quantity = int(request.form.get('quantity', 1))
    
    # Check if product already in cart
    for item in session['cart']:
        if item['product_id'] == product_id:
            item['quantity'] += quantity
            break
    else:
        product = get_product(product_id)
        if product:
            cart_item = {
                'product_id': product_id,
                'title': product['title'],
                'price': product['price'],
                'image': product['image'],
                'quantity': quantity
            }
            session['cart'].append(cart_item)
    
    session.modified = True
    return redirect(url_for('view_cart'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    initialize_cart()
    session['cart'] = [item for item in session['cart'] if item['product_id'] != product_id]
    session.modified = True
    return redirect(url_for('view_cart'))

@app.route('/update_cart', methods=['POST'])
def update_cart():
    initialize_cart()
    product_id = int(request.form.get('product_id'))
    quantity = int(request.form.get('quantity', 1))
    
    for item in session['cart']:
        if item['product_id'] == product_id:
            if quantity > 0:
                item['quantity'] = quantity
            else:
                session['cart'].remove(item)
            break
    
    session.modified = True
    return redirect(url_for('view_cart'))

@app.route('/cart')
def view_cart():
    initialize_cart()
    total = sum(item['price'] * item['quantity'] for item in session['cart'])
    return render_template('cart.html', cart=session['cart'], total=total)

if __name__ == '__main__':
    app.run(debug=True)