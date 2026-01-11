from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Katalog na dane (Render / lokalnie)
DATA_DIR = os.environ.get("DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
os.makedirs(DATA_DIR, exist_ok=True)
DB_FILE = os.path.join(DATA_DIR, "magazyn.db")

# Inicjalizacja bazy – ZAWSZE bezpieczna
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Strona główna – UNIKALNE PRODUKTY + SUMA
@app.route("/")
def index():
    init_db()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        SELECT name, SUM(quantity) AS total_quantity
        FROM products
        GROUP BY name
        ORDER BY name
    """)
    products = c.fetchall()
    conn.close()
    return render_template("index.html", products=products)

# Dodawanie produktu
@app.route("/add", methods=["POST"])
def add_product():
    name = request.form["name"].strip()
    quantity = int(request.form["quantity"])

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "INSERT INTO products (name, quantity) VALUES (?, ?)",
        (name, quantity)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("index"))

# Start aplikacji
if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
