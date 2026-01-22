from flask import Flask, render_template, redirect, url_for, session
from config import Config
from models import db, Product, Order

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

@app.route("/")
def index():
    products = Product.query.all()
    return render_template("index.html", products=products)

@app.route("/product/<int:product_id>")
def product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template("product.html", product=product)

@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    cart = session.get("cart", {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session["cart"] = cart
    return redirect(url_for("cart"))

@app.route("/cart")
def cart():
    cart = session.get("cart", {})
    products = []
    total = 0

    for product_id, quantity in cart.items():
        product = Product.query.get(int(product_id))
        subtotal = product.price * quantity
        total += subtotal
        products.append((product, quantity, subtotal))

    return render_template("cart.html", products=products, total=total)

@app.route("/checkout")
def checkout():
    cart = session.get("cart", {})
    total = 0

    for product_id, quantity in cart.items():
        product = Product.query.get(int(product_id))
        total += product.price * quantity

    order = Order(total_amount=total)
    db.session.add(order)
    db.session.commit()

    session.pop("cart", None)
    return render_template("checkout.html", total=total)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)