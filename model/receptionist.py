from model.db import db

class receptionist:

    def set_id(self,n):
        self.__id = n
    
    def get_id(self):
        return self.__id
    
    def set_name(self,name):
        self.__name = name
    
    def get_name(self):
        return self.__name

class receptionist_db(db):
    def __init__(self):
        super().__init__()
    
    def add_receptionist(self,rec):
        query = f"INSERT INTO receptionist (cl_id, cl_name, relieve) VALUES ({rec.get_id()}, {rec.get_name()}, 'N');"
        self._mycursor.execute(query)
        self._mydb.commit()
    
    def relieve_recep(self,rec):
        query = f"UPDATE receptionist SET relieve = 'Y' WHERE cl_id = {rec.get_id()};"
        self._mycursor.execute(query)
        self._mydb.commit()
    
    def view_all(self):
        query = f"SELECT cl_name FROM receptionist  WHERE relieve = 'N'"
        self._mycursor.execute(query)
        res = self._mycursor.fetchall()
        l = []
        for i in res:
            r = receptionist()
            r.set_name(i[0])
            l.append(r)
        return l
    
    def view_relieved(self):
        query = f"SELECT cl_name FROM receptionist WHERE relieve = 'Y'"
        self._mycursor.execute(query)
        res = self._mycursor.fetchall()
        l = []
        for i in res:
            r = receptionist()
            r.set_name(i[0])
            l.append(r)
        return l