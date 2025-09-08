import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# ------------------ DB Connection ------------------
def get_db_connection():
    conn = sqlite3.connect("orders.db")  # SQLite DB file
    conn.row_factory = sqlite3.Row       # results as dict-like objects
    return conn

# ------------------ Initialize DB ------------------
def init_db():
    conn = get_db_connection()
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
    conn.close()

# ------------------ Routes ------------------

# Place Order Page
@app.route("/", methods=["GET", "POST"])
@app.route("/place-order", methods=["GET", "POST"])
def place_order():
    if request.method == "POST":
        table_no = request.form["table_no"]
        item_name = request.form["item_name"]
        quantity = request.form["quantity"]

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO orders (table_no, item_name, quantity)
            VALUES (?, ?, ?)
        """, (table_no, item_name, quantity))
        conn.commit()
        conn.close()
        return redirect(url_for("orders"))

    return render_template("place_order.html")

# Orders Page
@app.route("/orders")
def orders():
    conn = get_db_connection()
    orders = conn.execute(
        "SELECT * FROM orders ORDER BY order_id"
    ).fetchall()
    conn.close()
    return render_template("orders.html", orders=orders)

# Kitchen Page
@app.route("/kitchen", methods=["GET", "POST"])
def kitchen():
    conn = get_db_connection()
    if request.method == "POST":
        order_id = request.form["order_id"]
        conn.execute("UPDATE orders SET status='Prepared' WHERE order_id=?", (order_id,))
        conn.commit()

    orders = conn.execute(
        "SELECT * FROM orders ORDER BY order_id"
    ).fetchall()
    conn.close()
    return render_template("kitchen.html", orders=orders)

# ------------------ Run App ------------------
if __name__ == "__main__":
    init_db()   # Create table if not exists
    app.run(debug=True)
