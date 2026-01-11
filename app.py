from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Ścieżka do bazy
DB_PATH = "magazyn.db"

# --- Funkcja do inicjalizacji bazy (tylko jeśli nie istnieje) ---
def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE products (
                name TEXT PRIMARY KEY,
                quantity INTEGER NOT NULL
            )
        """)
        conn.commit()
        conn.close()

# --- Strona główna ---
@app.route('/')
def index():
    init_db()  # upewniamy się, że tabela istnieje
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # pobieramy wszystkie produkty
    c.execute("SELECT name, quantity FROM products ORDER BY name")
    products = c.fetchall()
    conn.close()
    return render_template("index.html", products=products)

# --- Dodawanie produktu ---
@app.route('/add', methods=['POST'])
def add_product():
    name = request.form['name'].strip()
    quantity = int(request.form['quantity'])
    if name:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # jeśli produkt istnieje, sumujemy ilości
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

# --- Aktualizacja ilości produktu ---
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

# --- Uruchomienie serwera ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render ustawia port w zmiennej środowiskowej
    app.run(host="0.0.0.0", port=port, debug=True)
