from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'replace_this_with_a_random_secret_key'

# Hardcoded users (username -> hashed password)
users = {
    "MW": generate_password_hash("Aspire5536")
}

# Sample data: product -> list of supplier info
products_data = {
    "Galaxy A56": [
        {
            "supplier": "Herweck",
            "article": "378507",
            "price": 266.0,
            "shipping": 5.0,
            "colors": ["Schwarz", "Weiß"]
        },
        {
            "supplier": "Mobilezone",
            "article": "100014813",
            "price": 479.95,
            "shipping": 10.0,
            "colors": ["Schwarz"]
        },
        {
            "supplier": "SupplierA",
            "article": "A56-111",
            "price": 300.0,
            "shipping": 7.5,
            "colors": ["Blau", "Grün"]
        },
        {
            "supplier": "SupplierB",
            "article": "A56-222",
            "price": 290.0,
            "shipping": 5.5,
            "colors": ["Schwarz", "Orange"]
        }
    ],
    "Galaxy A55": [
        {
            "supplier": "Herweck",
            "article": "378508",
            "price": 255.0,
            "shipping": 5.0,
            "colors": ["Schwarz"]
        },
        {
            "supplier": "Mobilezone",
            "article": "100014814",
            "price": 470.0,
            "shipping": 10.0,
            "colors": ["Schwarz"]
        }
    ],
    "iPhone 16": [
        {
            "supplier": "Herweck",
            "article": "389846",
            "price": 645.0,
            "shipping": 5.0,
            "colors": ["Ultramarin"]
        },
        {
            "supplier": "Mobilezone",
            "article": "100015905",
            "price": 749.95,
            "shipping": 10.0,
            "colors": ["Ultramarin"]
        }
    ],
}


@app.route('/')
def index():
    return redirect(url_for('search'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            return redirect(url_for('search'))
        else:
            error = "Ungültige Anmeldedaten"
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('search'))


@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/results')
def results():
    query = request.args.get('query', '').strip()
    if not query:
        return redirect(url_for('search'))
    # find product data case-insensitive
    key = None
    for product in products_data.keys():
        if product.lower() == query.lower():
            key = product
            break
    products = []
    cheapest = None
    if key:
        for item in products_data[key]:
            total = item['price'] + item['shipping']
            item_data = {
                "supplier": item['supplier'],
                "article": item['article'],
                "price": item['price'],
                "shipping": item['shipping'],
                "colors": item['colors'],
                "total_price": total
            }
            products.append(item_data)
            if cheapest is None or total < cheapest:
                cheapest = total
    return render_template('results.html', query=query, products=products, cheapest=cheapest)


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_name = request.form['product_name']
    supplier = request.form['supplier']
    price = float(request.form['price'])
    shipping = float(request.form['shipping'])
    article = request.form['article']
    item = {
        "product_name": product_name,
        "supplier": supplier,
        "price": price,
        "shipping": shipping,
        "article": article
    }
    if 'cart' not in session:
        session['cart'] = []
    cart = session['cart']
    cart.append(item)
    session['cart'] = cart
    return redirect(url_for('cart'))


@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    total = sum(item['price'] + item['shipping'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)


if __name__ == '__main__':
    # Use debug=False in production
    app.run(debug=True)
