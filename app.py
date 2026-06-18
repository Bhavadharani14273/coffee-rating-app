from flask import Flask, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("coffee.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS coffee (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        votes INTEGER DEFAULT 0
    )
    """)

    cur.execute("SELECT COUNT(*) FROM coffee")
    count = cur.fetchone()[0]

    if count == 0:
        coffees = [
            ("Espresso", 0),
            ("Cappuccino", 0),
            ("Latte", 0),
            ("Mocha", 0)
        ]
        cur.executemany(
            "INSERT INTO coffee(name,votes) VALUES(?,?)",
            coffees
        )

    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect("coffee.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM coffee")
    coffees = cur.fetchall()

    conn.close()

    return render_template("index.html", coffees=coffees)

@app.route('/vote/<int:id>')
def vote(id):
    conn = sqlite3.connect("coffee.db")
    cur = conn.cursor()

    cur.execute(
        "UPDATE coffee SET votes = votes + 1 WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for('home'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)