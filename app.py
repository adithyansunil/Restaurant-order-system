import oracledb,os
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# ---------- OracleDB Connection ----------
oracledb.init_oracle_client(lib_dir=r"C:\oracle\instantclient_23_8")  # change path if needed

def get_db_connection():
    return oracledb.connect(
        user=os.getenv("DB_USER", "system"),
    password=os.getenv("DB_PASSWORD"),
    dsn=os.getenv("DB_DSN", "localhost/xe")
    )

# ---------- Routes ----------

@app.route("/")
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
            VALUES (:1, :2, :3)
        """, (table_no, item_name, quantity))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("orders"))

    return render_template("place_order.html")


@app.route("/orders")
def orders():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT order_id, table_no, item_name, quantity, status, created_at FROM orders ORDER BY order_id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("orders.html", orders=rows)


@app.route("/kitchen", methods=["GET", "POST"])
def kitchen():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == "POST":
        order_id = request.form["order_id"]
        cur.execute("UPDATE orders SET status='Prepared' WHERE order_id=:id", {"id": order_id})
        conn.commit()

    cur.execute("SELECT order_id, table_no, item_name, quantity, status FROM orders ORDER BY order_id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("kitchen.html", orders=rows)


# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)
