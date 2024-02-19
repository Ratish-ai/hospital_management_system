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
    
