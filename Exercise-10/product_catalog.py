from flask import Flask, jsonify

app = Flask(__name__)

products = [
    {"id": 1, "name": "Laptop"},
    {"id": 2, "name": "Phone"},
    {"id": 3, "name": "Headphones"}
]

@app.route("/products")
def get_products():
    return jsonify(products)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
