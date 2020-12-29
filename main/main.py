from dataclasses import dataclass

import requests
from flask import Flask, abort, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

from producer import publish

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@127.0.0.1:3307/main"
CORS(app)

db = SQLAlchemy(app)


@dataclass
class Product(db.Model):
    id: int
    title: str
    image: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))


@dataclass
class ProductUser(db.Model):
    id: int
    user_id: int
    product_id: int

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint("user_id", "product_id", name="user_product_id")


@app.route("/api/products")
def index():
    return jsonify(Product.query.all())


@app.route("/api/products/<int:id>/like", methods=["POST"])
def like(id):
    req = requests.get("http://localhost:8000/api/user")
    json = req.json()

    try:
        product_user = ProductUser(user_id=json["id"], product_id=id)
        db.session.add(product_user)
        db.session.commit()

        publish("product_liked", id)
    except:
        abort(400, "You already liked this product")

    return jsonify({"message": "sucess"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
