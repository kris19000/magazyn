from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Ścieżka do pliku SQLite w katalogu aplikacji
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, 'magazyn.db')

# Tworzymy bazę tylko jeśli plik nie istnieje
def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL
            )
        """)
        conn.commit()
        conn.close()

# Strona główna
@app.route('/')
def index():
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
    return redirect(url_for('index'))

# Uruchomienie serwera
if __name__ == "__main__":
    init_db()  # tworzymy bazę tylko jeśli nie istnieje
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
