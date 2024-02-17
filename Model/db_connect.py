import mysql.connector

class db:

    def __init__(self):
        self._mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Ratish^2",
            database="hospital"
        )

        self._mycursor = self._mydb.cursor()