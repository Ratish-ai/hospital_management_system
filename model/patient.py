from db import db

class patient:
    
    def set_p_id(self,n):
        self.__p_id = n
    
    def get_p_id(self):
        return self.__p_id
    
    def set_height(self,n):
        self.__height = n
    
    def get_height(self):
        return self.__height
    
    def set_weight(self,n):
        self.__weight = n
    
    def get_weight(self):
        return self.__weight
    
    def set_ph(self,n):
        self.__ph = n
    
    def get_ph(self):
        return self.__ph
    
    def set_tok_no(self,n):
        self.__tok = n
    
    def get_tok_no(self):
        return self.__tok
    
    def set_name(self,name):
        self.__name = name
    
    def get_name(self):
        return self.__name
    

class patient_db(db):
    
    def __init__(self):
        super().__init__()

    def update_height(self,role):
        query = f"UPDATE patient SET height = {role.get_height()} WHERE p_id = {role.get_p_id()};"
        self._mycursor.execute(query)
        self._mydb.commit()
    
    def update_weight(self,role):
        query = f"UPDATE patient SET weight = {role.get_weight()} WHERE p_id = {role.get_p_id()};"
        self._mycursor.execute(query)
        self._mydb.commit()
    
    def update_mob_no(self,role):
        query = f"UPDATE patient SET mob_no = {role.get_ph()} WHERE p_id = {role.get_p_id()};"
        self._mycursor.execute(query)
        self._mydb.commit()
    
    def add_tok_no(self,role):
        query = f"UPDATE patient SET tok_no = {role.get_tok_no()} WHERE p_id = {role.get_p_id()};"
        self._mycursor.execute(query)
        self._mydb.commit()
    
    def get_patient_details(self,role):
        query = f"SELECT p_name, height, weight FROM patient WHERE p_id = {role.get_p_id()}"
        self._mycursor.execute(query)
        res = self._mycursor.fetchone()
        p = patient()
        p.set_name(res[0])
        p.set_height(res[1])
        p.set_weight(res[2])
        return p
    
    def remove_token(self,role):
        query = f"UPDATE patient SET tok_no = null WHERE p_id = {role.get_p_id()};"
        self._mycursor.execute(query)
        self._mydb.commit()
    
    def find_patient(self,role):
        query = f"SELECT p_id, p_name FROM patient WHERE mob_no = '{role.get_ph}'"
        self._mycursor.execute(query)
        res = self._mycursor.fetchone()
        p = patient()
        p.set_p_id(res[0])
        p.set_name(p[1])
        return p