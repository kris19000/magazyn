from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

DB_PATH = "magazyn.db"

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # UWAGA: SQL w triple quotes
        c.execute("""
            CREATE TABLE products (
                name TEXT PRIMARY KEY,
                quantity INTEGER NOT NULL
            )
        """)
        conn.commit()
        conn.close()

@app.route('/')
def index():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name, quantity FROM products ORDER BY name")
    products = c.fetchall()
    conn.close()
    return render_template("index.html", products=products)

@app.route('/add', methods=['POST'])
def add_product():
    name = request.form['name'].strip()
    quantity = int(request.form['quantity'])
    if name:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT quantity FROM products WHERE name = ?", (name,))
        result = c.fetchone()
        if result:
            new_qty = result[0] + quantity
            c.execute("UPDATE products SET quantity = ? WHERE name = ?", (new_qty, name))
        else:
            c.execute("INSERT INTO products (name, quantity) VALUES (?, ?)", (name, quantity))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update_product():
    name = request.form['name']
    quantity = int(request.form['quantity'])
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE products SET quantity = ? WHERE name = ?", (quantity, name))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
