import sqlite3

conn = sqlite3.connect("magazyn.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS produkty (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nazwa TEXT,
    ilosc INTEGER
)
""")

conn.commit()
conn.close()

print("Baza danych gotowa!")