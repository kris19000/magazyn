from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def db():
    return sqlite3.connect("magazyn.db")

@app.route("/")
def index():
    conn = db()
    produkty = conn.execute("SELECT * FROM produkty").fetchall()
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

app.run(debug=True)