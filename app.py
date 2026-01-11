from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def db():
    return sqlite3.connect("magazyn.db")

@app.route("/")
def index():
    conn = db()
    produkty = conn.execute("SELECT DISTINCT nazwa, ilosc FROM produkty ORDER BY nazwa, ilosc").fetchall()
    conn.close()
    return render_template("index.html", produkty=produkty)

@app.route("/dodaj", methods=["POST"])
def dodaj():
    nazwa = request.form["nazwa"]
    ilosc = request.form["ilosc"]

    conn = db()
    conn.execute(
        "INSERT INTO produkty (nazwa, ilosc) VALUES (?, ?)",
        (nazwa, ilosc)
    )
    conn.commit()
    conn.close()

    return redirect("/")

import os

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)







