from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("magazyn.db")

@app.route("/")
def index():
    db = get_db()
    produkty = db.execute("SELECT * FROM produkty").fetchall()
    db.close()
    return render_template("index.html", produkty=produkty)

@app.route("/dodaj", methods=["POST"])
def dodaj():
    nazwa = request.form["nazwa"]
    ilosc = request.form["ilosc"]

    db = get_db()
    db.execute(
        "INSERT INTO produkty (nazwa, ilosc) VALUES (?, ?)",
        (nazwa, ilosc)
    )
    db.commit()
    db.close()
    return redirect("/")
    
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)




