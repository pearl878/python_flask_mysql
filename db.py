import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="pearl",
        password="dunmininu",
        database="school_db"
    )