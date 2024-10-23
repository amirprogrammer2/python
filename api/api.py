from flask import Flask, request, jsonify
from flasgger import Swagger
import sqlite3

app = Flask(__name__)
swagger = Swagger(app)

def get_db():
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS category (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS product (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT,
            price INTEGER,
            category_id INTEGER,
            FOREIGN KEY (category_id) REFERENCES category (id)
        )
    """)
    
    return con, cur

@app.route("/category", methods=["GET"])
def category_get():
    """
    Get all categories.
    ---
    responses:
      200:
        description: A list of categories
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              category:
                type: string
    """
    con, cur = get_db()
    cur.execute("SELECT * FROM category")
    categories = cur.fetchall()
    con.close()
    return jsonify(categories)

@app.route("/product", methods=["GET"])
def product_get():
    """
    Get all products.
    ---
    responses:
      200:
        description: A list of products
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              product:
                type: string
              price:
                type: integer
              category_id:
                type: integer
    """
    con, cur = get_db()
    cur.execute("SELECT * FROM product")
    products = cur.fetchall()
    con.close()
    return jsonify(products)

@app.route("/product/new", methods=["POST"])
def show_product():
    """
    Add a new product.
    ---
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - category
            - product
            - price
          properties:
            category:
              type: string
            product:
              type: string
            price:
              type: integer
    responses:
      201:
        description: Product added successfully
      400:
        description: Bad request, missing fields or invalid data
      500:
        description: Internal server error
    """
    con, cur = get_db()
    try:
        category_name = request.json.get("category")
        product_name = request.json.get("product")
        price = request.json.get("price")

        if not category_name or not product_name or price is None:
            return jsonify({"error": "category, product, and price are required"}), 400

        cur.execute("SELECT id FROM category WHERE category = ?", (category_name,))
        category_row = cur.fetchone()
        if category_row is None:
            return jsonify({"error": "Category not found"}), 404

        category_id = category_row[0]
        cur.execute("INSERT INTO product (product, price, category_id) VALUES (?, ?, ?)", (product_name, price, category_id))
        con.commit()

        return jsonify({"message": "Product added successfully"}), 201

    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        con.close()

@app.route("/category/new", methods=["POST"])
def show_category():
    """
    Add a new category.
    ---
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - category
          properties:
            category:
              type: string
    responses:
      201:
        description: Category added successfully
    """
    con, cur = get_db()
    try:
        category_name = request.json["category"]
        cur.execute("INSERT INTO category (category) VALUES (?)", (category_name,))
        con.commit()
        return jsonify({"message": "success"}), 201

    finally:
        con.close()

@app.route("/category/update", methods=["PUT"])
def update_category():
    """
    Update an existing category.
    ---
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - old_name
            - new_name
          properties:
            old_name:
              type: string
            new_name:
              type: string
    responses:
      200:
        description: Category updated successfully
      404:
        description: Category not found
    """
    con, cur = get_db()
    try:
        old_name = request.json["old_name"]
        new_name = request.json["new_name"]

        cur.execute("SELECT * FROM category WHERE category = ?", (old_name,))
        existing_category = cur.fetchone()

        if not existing_category:
            return jsonify({"error": "Category not found"}), 404

        cur.execute("UPDATE category SET category = ? WHERE category = ?", (new_name, old_name))
        con.commit()
        return jsonify({"message": "Category updated successfully"}), 200

    finally:
        con.close()

@app.route("/product/update", methods=["PUT"])
def update_product():
    """
    Update an existing product.
    ---
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - old_product
          properties:
            old_product:
              type: string
            new_product:
              type: string
            new_category:
              type: string
            new_price:
              type: integer
    responses:
      200:
        description: Product updated successfully
      404:
        description: Product not found
      400:
        description: Old product name is required
      500:
        description: Internal server error
    """
    con, cur = get_db()
    try:
        old_product = request.json.get("old_product")
        if not old_product:
            return jsonify({"error": "Old product name is required"}), 400

        new_product = request.json.get("new_product")
        new_category = request.json.get("new_category")
        new_price = request.json.get("new_price")

        cur.execute("SELECT * FROM product WHERE product = ?", (old_product,))
        existing_product = cur.fetchone()

        if not existing_product:
            return jsonify({"error": "Product not found"}), 404

        if new_product:
            cur.execute("UPDATE product SET product = ? WHERE product = ?", (new_product, old_product))
        if new_category:
            cur.execute("UPDATE product SET category_id = (SELECT id FROM category WHERE category = ?) WHERE product = ?",
                        (new_category, old_product))
        if new_price is not None:
            cur.execute("UPDATE product SET price = ? WHERE product = ?", (new_price, old_product))

        con.commit()
        return jsonify({"message": "Product updated successfully"}), 200

    finally:
        con.close()

@app.route("/get/category/<string:category>", methods=['GET'])
def get_product_by_categorie(category):
    """
    Get products by category.
    ---
    parameters:
      - in: path
        name: category
        type: string
        required: true
        description: The category to filter products
    responses:
      200:
        description: A list of products for the specified category
        schema:
          type: array
          items:
            type: object
            properties:
              product:
                type: string
              price:
                type: integer
      404:
        description: Category not found
    """
    con, cur = get_db()
    try:
        cur.execute("SELECT id FROM category WHERE category = ?", (category,))
        category_row = cur.fetchone()

        if not category_row:
            return jsonify({"error": "Category not found"}), 404

        category_id = category_row[0]
        cur.execute("SELECT product, price FROM product WHERE category_id = ?", (category_id,))
        products = cur.fetchall()

        if not products:
            return jsonify({"message": "No products found for this category."}), 200

        product_list = [{"product": product[0], "price": product[1]} for product in products]
        return jsonify(product_list)

    finally:
        con.close()

if __name__ == "__main__":
    app.run(port=8585)
