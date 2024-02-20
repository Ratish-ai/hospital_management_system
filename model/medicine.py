from db import db

class medicine:

    def set_med_id(self,id):
        self.__id = id
    
    def get_med_id(self):
        return self.__id
    
    def set_name(self,name):
        self.__name = name
    
    def get_name(self):
        return self.__name
    
    def set_avl(self,n):
        self.__avl = n
    
    def get_avl(self):
        return self.__avl
    
    def set_date(self,d):
        self.__date = d
    
    def get_date(self):
        return self.__date
    
    def set_rate(self,n):
        self.__rate = n
    
    def get_rate(self):
        return self.__rate
    
class medicine_db(db):

    def __init__(self):
        super().__init__()
    
    def update_med(self,med):
        query = f"UPDATE medicine SET avail_qty = {med.get_avl()} WHERE med_id = {med.get_id()};"
        self._mycursor.execute(query)
        self._mydb.commit()
    
    def get_med_id(self,med):
        query = f"SELECT med_id FROM medicine WHERE med_name = '{med.get_name()}'"
        self._mycursor.execute(query)
        result = self._mycursor.fetchone()
        m = medicine()
        m.set_med_id(result[0])
        return m
    
    def add_new_med(self,med):
        query = f"INSERT INTO medicine (med_id, med_name, avail_qty, exp_date, rate) VALUES ({med.get_med_id()}, '{med.get_name()}', {med.get_avl}, '{med.get_date()}', {med.get_rate()});"
        self._mycursor.execute(query)
        self._mydb.commit()
    
    def new_id(self):
        query = f"SELECT MAX(med_id) FROM medicine;"
        self._mycursor.execute(query)
        res = self._mycursor.fetchone()
        m = medicine()
        m.set_med_id(res[0]+1)
        return m
    
    def remove_expired(self,med):
        query = f"UPDATE medicine SET avail_qty = 0 WHERE exp_date < DATE('{med.get_date()}')"
        self._mycursor.execute(query)
        self._mydb.commit()
    
    def update_rate(self,med):
        query = f"UPDATE medicine SET rate = {med.get_rate()} WHERE med_id = {med.get_med_id()})"
        self._mycursor.execute(query)
        self._mydb.commit()
    
    def update_expired(self,med):
        query = f"UPDATE medicine SET exp_date = DATE('{med.get_date()}') WHERE med_id = {med.get_med_id()})"
        self._mycursor.execute(query)
        self._mydb.commit()
    
    def show_all(self,med):
        query = f"SELECT med_id, med_name, avail_qty, rate FROM medicine WHERE exp_date > DATE('{med.get_date()}')"
        self._mycursor.execute(query)
        result = self._mycursor.fetchall()
        l = []
        for i in result:
            m = medicine()
            m.set_med_id(i[0])
            m.set_name(i[1])
            m.set_avl(i[2])
            m.set_rate(i[3])
            l.append(m)
        return l
    
    def show_expired(self,med):
        query = f"SELECT med_id, med_name, avail_qty FROM medicine WHERE exp_date < DATE('{med.get_date()}')"
        self._mycursor.execute(query)
        result = self._mycursor.fetchall()
        l = []
        for i in result:
            m = medicine()
            m.set_med_id(i[0])
            m.set_name(i[1])
            m.set_avl(i[2])
            l.append(m)
        return l
    
    def show_avail(self,med):
        query = f"SELECT med_id, med_name, avail_qty, rate FROM medicine WHERE exp_date > DATE('{med.get_date()}') AND avail_qty > 0"
        self._mycursor.execute(query)
        result = self._mycursor.fetchall()
        l = []
        for i in result:
            m = medicine()
            m.set_med_id(i[0])
            m.set_name(i[1])
            m.set_avl(i[2])
            m.set_rate(i[3])
            l.append(m)
        return l
    
    def show_unavail(self,med):
        query = f"SELECT med_id, med_name FROM medicine WHERE exp_date > DATE('{med.get_date()}') AND avail_qty == 0"
        self._mycursor.execute(query)
        result = self._mycursor.fetchall()
        l = []
        for i in result:
            m = medicine()
            m.set_med_id(i[0])
            m.set_name(i[1])
            l.append(m)
        return l