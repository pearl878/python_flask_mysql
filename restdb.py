import mysql.connector


def get_connection():

    return mysql.connector.connect(
        host="localhost",
        user="pearl",
        password="dunmininu",  # Enter your MySQL password
        database="restschool",
        port=3306
    )


if __name__ == "__main__":

    try:
        conn = get_connection()

        print("REST School Database Connected Successfully!")

        conn.close()

    except mysql.connector.Error as error:

        print("Database Connection Failed:", error)