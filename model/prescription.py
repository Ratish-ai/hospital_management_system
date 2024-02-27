from model.db import db
from model.medicine import medicine

class prescription:

    def set_pres_id(self,n):
        self.__pr_id = n
    
    def get_pres_id(self):
        return self.__pr_id
    
    def set_date(self,d):
        self.__date = d
    
    def get_date(self):
        return self.__date

class prescription_queue(db):
    
    def __init__(self):
        super().__init__()
    
    def add_to_queue(self,p):
        query = f"INSERT INTO prescription_queue (pr_id,status) VALUES ({p.get_pr_id()}, 'N');"
        self._mycursor.execute(query)
        self._mydb.commit()
    
    def checkout(self,p):
        query = f"UPDATE prescription_queue SET status = 'Y' WHERE pr_id = {p.get_pr_id()}"
        self._mycursor.execute(query)
        self._mydb.commit()
    
    def show_in_queue(self):
        query = f"SELECT pr_id FROM prescription_queue WHERE status = 'N'"
        self._mycursor.execute(query)
        result = self._mycursor.fetchall()
        l = []
        for i in result:
            p = prescription()
            p.set_pres_id(i[0])
            l.append(p)
        return l

class prescription_db(db):

    def __init__(self):
        super().__init__()
    
    def add_pres(self,pat,doc,pres,med):
        query = f"INSERT INTO prescription (pr_id, p_id, d_id, date, med_id, qty) VALUES ({pres.get_pr_id()}, {pat.get_p_id()}, {doc.get_d_id()}, DATE('{pres.get_date()}'), {med.get_med_id()}, {med.get_avl()})"
        self._mycursor.execute(query)
        self._mydb.commit()
    
    def gen_pr_id(self):
        query = f"SELECT MAX(pr_id) FROM prescription"
        self._mycursor.execute(query)
        result = self._mycursor.fetchone()
        p = prescription()
        p.set_pres_id(result[0]+1)
        return p
    
    def get_prescription(self,pat,med):
        query = f"""SELECT m.med_name, pr.qty
                    FROM prescription pr
                    JOIN medicine m ON pr.med_id = m.med_id
                    WHERE pr.p_id = {pat.get_p_id()} AND pr.prescription_date = '{med.get_date()}';
                """
        self._mycursor.execute(query)
        result = self._mycursor.fetchall()
        l = []
        for i in result:
            m = medicine()
            m.set_name(result[0])
            m.set_avl(result[1])
            l.append(m)
        return l

class bill:

    def set_med_name(self,na):
        self.__name = na
    
    def get_med_name(self):
        return self.__name
    
    def set_med_qty(self,n):
        self.__qty = n
    
    def get_med_qty(self):
        return self.__qty
    
    def set_med_cost(self,n):
        self.__cost = n

    def get_med_cost(self):
        return self.__cost

class bill_db(db):

    def __init__(self):
        super().__init__()
    
    def get_bill(self,pr,pat):
        query = f"""SELECT m.med_name, pr.qty, b.cost
                FROM bill b
                JOIN prescription pr ON b.pr_id = pr.pr_id
                JOIN medicine m ON pr.med_id = m.med_id
                JOIN patient p ON pr.p_id = p.p_id
                WHERE p.p_id = {pat.get_p_id()} AND pr.date = '{pr.get_date()}';
                """
        self._mycursor.execute(query)
        result = self._mycursor.fetchall()
        l = []
        for i in result:
            b = bill()
            b.set_med_name(i[0])
            b.set_med_qty(i[1])
            b.set_med_cost(i[2])
            l.append(b)
        return l
    
    def add_bill(self,pr,med):
        query = f"INSERT INTO bill (pr_id, med_id, cost) VALUES ({pr.get_pr_id()}, {med.get_med_id()}, {med.get_rate()})"
        self._mycursor.execute(query)
        self._mydb.commit()