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

class user_login:

    def update_pwd(self,pwd):
        self.__pwd = pwd
    
    def get_pwd(self):
        return self.__pwd
    
    def set_u_name(self,name):
        self.__u_name = name
    
    def get_u_name(self):
        return self.__u_name

class user_login_db(db):

    def __init__(self):
        super().__init__()
    
    def check_u_name(self,u_name):
        query = f"SELECT u_name FROM user_login WHERE user_name = '{u_name}';"
        self._mycursor.execute(query)
        res = self._mycursor.fetchone()
        if res[0] is None:
            return False
        self.__u_name = u_name
        return True
    
    def check_pwd(self,pwd):
        query = f"SELECT password FROM user_login WHERE user_name = '{self.__u_name}';"
        self._mycursor.execute(query)
        res = self._mycursor.fetchone()
        if res[0] != pwd:
            return False
        self.get_u_id()
        return True
    
    def get_u_id(self):
        query = f"SELECT user_id FROM user_login WHERE user_name = '{self.__u_name}'"
        self._mycursor.execute(query)
        res = self._mycursor.fetchone()
        self.__u_id = res[0]
    
    def set_pwd(self,new_pwd):
        query = f"UPDATE user_login SET password = '{new_pwd}' WHERE user_id = {self.__u_id};"
        self._mycursor.execute(query)
        self._mydb.commit()
    
    def get_pwd(self):
        query = f"SELECT password FROM user_login WHERE user_id = {self.__u_id};"
        self._mycursor.execute(query)
        result = self._mycursor.fetchone()
        u_t = user_login()
        u_t.update_pwd(result[0])
        return u_t

    def add_login_details(self,id,u_name,pwd):
        query = f"INSERT INTO user_login (user_id, user_name, password) VALUES ({id},'{u_name}','{pwd}')"
        self._mycursor.execute(query)
        self._mydb.commit()
    
class user_role:

    def set_new_id(self,id):
        self.__new_id = id

    def get_new_id(self):
        return self.__new_id
    
    def set_type(self,type):
        self.__type = type

    def get_type(self):
        return self.__type
    
    def set_new_role(self,id,type):
        self.__id = id
        self.__type = type
    
    def get_id(self):
        return self.__id
    
    def get_role(self):
        return self.__id

class user_role_db(db):

    def __init__(self):
        super().__init__()
    
    def get_new_id(self):
        query = f"SELECT MAX(user_id) FROM USER_ROLE;"
        self._mycursor.execute(query)
        res = self._mycursor.fetchone()
        u_t = user_role()
        u_t.set_new_id(res+1)
        return u_t
    
    def get_type(self,u_id):
        query = f"SELECT user_role FROM user_role WHERE user_id = {u_id}"
        self._mycursor.execute(query)
        res = self._mycursor.fetchone()
        u_t = user_role()
        u_t.set_type(res[0])
        return u_t
    
    def set_new_role(self,role):
        query = f"INSERT INTO user_role (user_id, user_role) VALUES({role.get_id()},'{role.get_type()}');"
        self._mycursor.execute(query)
        self._mydb.commit()

class queue:

    def set_queue_length(self,n):
        self.__queue_length = n
    
    def get_queue_length(self):
        return self.__queue_length
    
    def set_p_id(self,n):
        self.__p_id = n
    
    def get_p_id(self):
        return self.__p_id
    
    def set_d_id(self,n):
        self.__d_id = n
    
    def get_d_id(self):
        return self.__d_id

class queue_db(db):

    def __init__(self):
        super().__init__()
    
    def get_persons_in_queue(self,role):
        query = f"SELECT COUNT(p_id) FROM queue WHERE d_id = {role.get_d_id()} AND status = 'N';"
        self._mycursor.execute(query)
        res = self._mycursor.fetchone()[0]
        q = queue()
        q.set_queue_length(res)
        return q
    
    def get_pids_in_queue(self,role):
        query = f"SELECT p_id FROM queue WHERE d_id = {role.get_d_id()} AND status = 'N';"
        self._mycursor.execute(query)
        res = self._mycursor.fetchall()
        l = []
        for i in res:
            q = queue()
            q.set_p_id(i)
            l.append(q)
        return l
    
    def get_d_id(self,u_id):
        query = f"SELECT d_id FROM queue WHERE p_id = {u_id}"
        self._mycursor.execute(query)
        res = self._mycursor.fetchone()[0]
        q = queue()
        q.set_d_id(res)
        return q
    
    def get_cuur_pat(self,role):
        query = f"SELECT p_id FROM queue WHERE d_id = {role.get_d_id()} AND status = 'N' LIMIT 1;"
        self._mycursor.execute(query)
        res = self._mycursor.fetchone()[0]
        q = queue()
        q.set_p_id(res)
        return q
    
    def attend_patient(self,role):
        query = f"UPDATE queue SET status = 'Y' WHERE p_id = {role.get_p_id()};"
        self._mycursor.execute(query)
        self._mydb.commit()
    
    def __generate_tok_no(self):
        query = f"SELECT MAX(t_no) FROM queue;"
        self._mycursor.execute(query)
        res = self._mycursor.fetchone()
        return res[0]+1

    def add_patient(self,role):
        query = f"INSERT INTO queue (t_no, p_id, d_id, status) VALUES({self.__generate_tok_no()}, {role.get_p_id}, {role.get_d_id}, 'N');"
        self._mycursor.execute(query)
        self._mydb.commit()

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
    
class pharmacist:

    def set_id(self,n):
        self.__id = n
    
    def get_id(self):
        return self.__id
    
    def set_name(self,name):
        self.__name = name
    
    def get_name(self):
        return self.__name

class pharmacist_db(db):
    def __init__(self):
        super().__init__()
    
    def add_pharmacist(self,rec):
        query = f"INSERT INTO pharmacist (pm_id, pm_name, relieve) VALUES ({rec.get_id()}, {rec.get_name()}, 'N');"
        self._mycursor.execute(query)
        self._mydb.commit()
    
    def relieve_recep(self,rec):
        query = f"UPDATE pharmacist SET relieve = 'Y' WHERE pm_id = {rec.get_id()};"
        self._mycursor.execute(query)
        self._mydb.commit()
    
    def view_all(self):
        query = f"SELECT pm_name FROM pharmacist WHERE relieve = 'N'"
        self._mycursor.execute(query)
        res = self._mycursor.fetchall()
        l = []
        for i in res:
            r = pharmacist()
            r.set_name(i[0])
            l.append(r)
        return l
    
    def view_relieved(self):
        query = f"SELECT pm_name FROM pharmacist WHERE relieve = 'Y'"
        self._mycursor.execute(query)
        res = self._mycursor.fetchall()
        l = []
        for i in res:
            r = pharmacist()
            r.set_name(i[0])
            l.append(r)
        return l

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