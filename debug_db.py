import sqlite3

conn = sqlite3.connect('finance.db')
cursor = conn.cursor()

print("=== DATABASE STRUCTURE ===")
cursor.execute("PRAGMA table_info(transactions)")
columns = cursor.fetchall()
for col in columns:
    print(f"Column {col[1]}: {col[2]}")

print("\n=== RECENT TRANSACTIONS ===")
cursor.execute("SELECT * FROM transactions ORDER BY created_at DESC LIMIT 5")
transactions = cursor.fetchall()
for t in transactions:
    print(f"Transaction: {t}")

conn.close()
