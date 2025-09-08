import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DB_FILE = "orders.db"

# ---------- Initialize DB ----------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_no INTEGER NOT NULL,
            item_name TEXT NOT NULL,
            quantity INTEGER DEFAULT 1,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

# Run table creation at app startup
init_db()

# ---------- Routes ----------
@app.route("/")
@app.route("/place-order", methods=["GET", "POST"])
def place_order():
    if request.method == "POST":
        table_no = request.form["table_no"]
        item_name = request.form["item_name"]
        quantity = request.form["quantity"]

        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO orders (table_no, item_name, quantity)
            VALUES (?, ?, ?)
        """, (table_no, item_name, quantity))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("orders"))

    return render_template("place_order.html")


@app.route("/orders")
def orders():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT order_id, table_no, item_name, quantity, status, created_at FROM orders ORDER BY order_id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("orders.html", orders=rows)


@app.route("/kitchen", methods=["GET", "POST"])
def kitchen():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    if request.method == "POST":
        order_id = request.form["order_id"]
        cur.execute("UPDATE orders SET status='Prepared' WHERE order_id=?", (order_id,))
        conn.commit()

    cur.execute("SELECT order_id, table_no, item_name, quantity, status FROM orders ORDER BY order_id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("kitchen.html", orders=rows)


# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)
