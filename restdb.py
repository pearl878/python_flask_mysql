import os
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME"),
        port=int(os.environ.get("DB_PORT", 3306))
    )

if __name__ == "__main__":
    try:
        conn = get_connection()
        print("REST School Database Connected Successfully!")
        conn.close()
    except mysql.connector.Error as error:
        print("Database Connection Failed:", error)