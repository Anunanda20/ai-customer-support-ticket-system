import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

print("Starting connection test...")

try:
    conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=3306,
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    connection_timeout=10,
    use_pure=True
)

    print("✅ DATABASE CONNECTED!")
    print("Connection object:", conn)

except BaseException as e:
    print("❌ CONNECTION ERROR:")
    print(type(e).__name__)
    print(repr(e))

finally:
    print("TEST FINISHED")
    