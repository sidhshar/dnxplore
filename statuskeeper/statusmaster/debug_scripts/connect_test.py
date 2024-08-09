import mysql.connector
from mysql.connector import Error

from ls import LSDATABASES

def connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host = LSDATABASES['default']['HOST'],
            database = LSDATABASES['default']['NAME'],
            user = LSDATABASES['default']['USER'],
            password = LSDATABASES['default']['PASSWORD'],
            port=3306  # default MySQL port
        )

        if connection.is_connected():
            db_info = connection.get_server_info()
            print("Connected to MySQL database... MySQL Server version on ", db_info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("Your connected to - ", record)

            # Your SQL query here
            # cursor.execute("YOUR QUERY")
            # results = cursor.fetchall()

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

connect_to_mysql()
