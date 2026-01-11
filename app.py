from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

DB_PATH = "magazyn.db"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
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


@app.route("/")
def index():
    conn = get_db_connection()
    c = conn.cursor()

    c.execute("""
        SELECT name, SUM(quantity) as quantity
        FROM products
        GROUP BY name
        ORDER BY name
    """)
    products = c.fetchall()

    conn.close()
    return render_template("index.html", products=products)


@app.route("/add", methods=["POST"])
def add_product():
    name = request.form["name"].strip()
    quantity = int(request.form["quantity"])

    if name:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(
            "INSERT INTO products (name, quantity) VALUES (?, ?)",
            (name, quantity)
        )
        conn.commit()
        conn.close()

    return redirect(url_for("index"))


@app.route("/update", methods=["POST"])
def update_product():
    name = request.form["name"]
    quantity = int(request.form["quantity"])

    conn = get_db_connection()
    c = conn.cursor()

    c.execute("DELETE FROM products WHERE name = ?", (name,))
    c.execute(
        "INSERT INTO products (name, quantity) VALUES (?, ?)",
        (name, quantity)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
