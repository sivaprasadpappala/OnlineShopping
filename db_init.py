from app import app
from models import db, Product

with app.app_context():
    db.drop_all()
    db.create_all()

    products = [
        Product(name="Laptop", price=75000, description="High performance laptop", stock=10),
        Product(name="Mobile Phone", price=25000, description="Android smartphone", stock=20),
        Product(name="Headphones", price=3000, description="Noise cancelling", stock=30),
    ]

    db.session.add_all(products)
    db.session.commit()

    print("Database initialized with sample products.")