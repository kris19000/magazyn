from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)
DB_FILE = 'magazyn.db'

# Funkcja pomocnicza: tworzy tabelę jeśli nie istnieje
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

# Strona główna - lista produktów z sumą ilości
@app.route('/')
def index():
    init_db()  # upewniamy się, że tabela istnieje
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        SELECT name, SUM(quantity) as total_quantity
        FROM products
        GROUP BY name
        ORDER BY name ASC
    """)
    products = c.fetchall()
    conn.close()
    return render_template('index.html', products=products)

# Dodawanie produktu
@app.route('/add', methods=['POST'])
def add_product():
    name = request.form['name']
    quantity = int(request.form['quantity'])
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO products (name, quantity) VALUES (?, ?)", (name, quantity))
    conn.commit()
    conn.close()
    return redirect('/')

# Uruchomienie serwera
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render wymaga zmiennej P
