import mysql.connector

class db:

    def __init__(self):
        
        self._mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Ratish^2",
            database="bank"
        )

        self._mycursor = self._mydb.cursor()

class admin_db(db):

    def __init__(self):
        super().__init__()

class patient_db(db):
    
    def __init__(self):
        super().__init__()
    
    

class doctor_db(db):

    def __init__(self):
        super().__init__()

class pharmacist_db(db):

    def __init__(self):
        super().__init__()

class receptionist_db(db):

    def __init__(self):
        super().__init__()