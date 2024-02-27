from model.db import db

class doctor:

    def set_d_id(self,n):
        self.__id = n
    
    def get_d_id(self):
        return self.__id
    
    def set_name(self,name):
        self.__name = name
    
    def get_name(self):
        return self.__name
    
    def set_spec(self,sp):
        self.__spl = sp
    
    def get_spec(self):
        return self.__spl
    
    def set_from(self,time):
        self.__from = time
    
    def get_from(self):
        return self.__from
    
    def set_to(self, time):
        self.__to = time
    
    def get_to(self):
        return self.__to
    
class doctor_db(db):

    def __init__(self):
        super().__init__()
    
    def add_doctor(self,role):
        query = f"INSERT INTO doctor (d_id, d_name, specialist, from_time, to_time, relieve) VALUES ({role.get_d_id()}, '{role.get_name()}', '{role.get_spec()}', '{role.get_from()}', '{role.get_to()}', 'N');"
        self._mycursor.execute(query)
        self._mydb.commit()
    
    def relieve(self,role):
        query = f"UPDATE doctor SET relieve = 'Y' WHERE d_id = {role.get_d_id()};"
        self._mycursor.execute(query)
        self._mydb.commit()
    
    def update_spec(self,role):
        query = f"UPDATE doctor SET specialist = '{role.get_spec()}' WHERE d_id = {role.get_d_id()}"
        self._mycursor.execute(query)
        self._mydb.commit()
    
    def update_from(self,role):
        query = f"UPDATE doctor SET from_time = '{role.get_from()}' WHERE d_id = {role.get_d_id()}"
        self._mycursor.execute(query)
        self._mydb.commit()
    
    def update_from(self,role):
        query = f"UPDATE doctor SET to_time = '{role.get_to()}' WHERE d_id = {role.get_d_id()}"
        self._mycursor.execute(query)
        self._mydb.commit()
    
    def view_all(self):
        query = f"SELECT d_id, d_name, specialist, from_time, to_time FROM doctor WHERE relieve = 'N';"
        self._mycursor.execute(query)
        result = self._mycursor.fetchall()
        l = []
        for i in result:
            d = doctor()
            d.set_d_id(i[0])
            d.set_name(i[1])
            d.set_spec(i[2])
            d.set_from(i[3])
            d.set_to(i[4])
            l.append(d)
        return l
    
    def view_spec(self):
        query = f"SELECT DISTINCT(specialist) FROM doctor WHERE relieve = 'N';"
        self._mycursor.execute(query)
        result = self._mycursor.fetchall()
        l = []
        for i in result:
            d = doctor()
            d.set_spec(i[2])
            l.append(d)
        return l
    
    def view_relieve(self):
        query = f"SELECT d_name, specialist FROM doctor WHERE relieve = 'Y';"
        self._mycursor.execute(query)
        result = self._mycursor.fetchall()
        l = []
        for i in result:
            d = doctor()
            d.set_name(i[1])
            d.set_spec(i[2])
            l.append(d)
        return l
    
    def view_by_specialist(self,role):
        query = f"SELECT d_id, d_name, from_time, to_time FROM doctor WHERE relieve = 'N' AND specialist = '{role.get_spec()}';"
        self._mycursor.execute(query)
        result = self._mycursor.fetchall()
        l = []
        for i in result:
            d = doctor()
            d.set_d_id(i[0])
            d.set_name(i[1])
            d.set_from(i[3])
            d.set_to(i[4])
            l.append(d)
        return l