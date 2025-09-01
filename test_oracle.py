import oracledb

# point to your Instant Client
oracledb.init_oracle_client(lib_dir=r"C:\oracle\instantclient_23_8")

conn = oracledb.connect(
    user="system",              # change if needed
    password="manager",    # put your Oracle password
    dsn="localhost/XE"
)

print("Connected:", conn.version)

cur = conn.cursor()
cur.execute("SELECT * FROM orders")
print(cur.fetchall())

cur.close()
conn.close()
