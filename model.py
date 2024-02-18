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


class user(db):

    def __init__(self,u_id):
        super().__init__()
        self.__u_id = u_id
    
    def set_pwd(self,new_pwd):
        query = f"UPDATE user_login SET password = '{new_pwd}' WHERE user_id = {self.__u_id};"
        self._mycursor.execute(query)
        self._mydb.commit()
    
    def get_pwd(self):
        query = f"SELECT password FROM user_login WHERE user_id = {self.__u_id};"
        self._mycursor.execute(query)
        result = self._mycursor.fetchone()
        return result[0]


class admin_db(db):

    def __init__(self,u_id):
        super().__init__()
        self.__u_id = u_id
        self.__u = user(self.__u_id)
    
    def update_pwd(self,new_pwd):
        self.__u.set_pwd(new_pwd)
    
    def check_pwd(self,cnf_pwd):
        return cnf_pwd==self.__u.get_pwd()


class patient_db(db):
    
    def __init__(self,u_id):
        super().__init__()
        self.__u_id = u_id
        self.__u = user(self.__u_id)
    
    def get_all_prescription_date(self):
        query = f"SELECT DATE FROM PRESCRIPTION WHERE P_ID = '{self.__u_id}';"
        self._mycursor.execute(query)
        result = self._mycursor.fetchall()
        return result

    def get_prescription(self,date):
        query = f"""SELECT m.med_name, pr.qty
                    FROM prescription pr
                    JOIN medicine m ON pr.med_id = m.med_id
                    WHERE pr.p_id = {self.__u_id} AND pr.prescription_date = '{date}';
                """
        self._mycursor.execute(query)
        result = self._mycursor.fetchall()
        return result
    
    def __get_prescription_id(self,date):
        query = f"SELECT pr_id FROM PRESCRIPTION WHERE P_ID = '{self.__u_id}' AND DATE = '{date}'"
        self._mycursor.execute(query)
        result = self._mycursor.fetchone()
        return result[0]
    
    def get_medicine(self,date):
        pr_id = self.__get_prescription_id(date)
        query = f"INSERT INTO PRESCRIPTION_QUEUE (pr_id, status) VALUES ({pr_id}, 'N')"
        self._mycursor.execute(query)
        self._mydb.commit()
    
    def get_bill(self,date):
        query = f"""SELECT m.med_name, pr.qty, b.cost
                FROM bill b
                JOIN prescription pr ON b.pr_id = pr.pr_id
                JOIN medicine m ON pr.med_id = m.med_id
                JOIN patient p ON pr.p_id = p.p_id
                WHERE p.p_id = {self.__u_id} AND pr.date = '{date}';
                """
        self._mycursor.execute(query)
        result = self._mycursor.fetchall()
        return result
    
    def update_pwd(self,new_pwd):
        self.__u.set_pwd(new_pwd)
    
    def check_pwd(self,cnf_pwd):
        return cnf_pwd==self.__u.get_pwd()


class doctor_db(db):

    def __init__(self,u_id):
        super().__init__()
        self.__u_id = u_id
        self.__u = user(self.__u_id)
    
    def update_pwd(self,new_pwd):
        self.__u.set_pwd(new_pwd)
    
    def check_pwd(self,cnf_pwd):
        return cnf_pwd==self.__u.get_pwd()

class pharmacist_db(db):

    def __init__(self,u_id):
        super().__init__()
        self.__u_id = u_id
        self.__u = user(self.__u_id)
    
    def update_pwd(self,new_pwd):
        self.__u.set_pwd(new_pwd)
    
    def check_pwd(self,cnf_pwd):
        return cnf_pwd==self.__u.get_pwd()


class receptionist_db(db):

    def __init__(self,u_id):
        super().__init__()
        self.__u_id = u_id
        self.__u = user(self.__u_id)
    
    def update_pwd(self,new_pwd):
        self.__u.set_pwd(new_pwd)
    
    def check_pwd(self,cnf_pwd):
        return cnf_pwd==self.__u.get_pwd()
    
    def get_new_patient_id(self):
        query = f"SELECT MAX(user_id) FROM USER_ROLE;"
        self._mycursor.execute(query)
        res = self._mycursor.fetchone()
        return res+1
    
    def add_patient_details(self,id,name,height,weight):
        query = f"INSERT INTO patient (p_id, p_name, height, weight) VALUES({id},'{name}',{height},{weight});"
        self._mycursor.execute(query)
        self._mydb.commit()
    
    def add_role(self,id):
        query = f"INSERT INTO user_role (user_id, user_role) VALUES({id},'patient');"
        self._mycursor.execute(query)
        self._mydb.commit()

    def add_login_details(self,id,u_name,pwd):
        query = f"INSERT INTO user_login (user_id, user_name, password) VALUES ({id},'{u_name}','{pwd}')"
        self._mycursor.execute(query)
        self._mydb.commit()
    
    def view_all_doctors(self):
        query = f"SELECT d_name, specialist, from_time, to_time FROM doctor WHERE relieve = 'N';"
        self._mycursor.execute(query)
        result = self._mycursor.fetchall()
        return result
    
    def view_specialists(self):
        query = f"SELECT DISTINCT(specialist) FROM doctor;"
        self._mycursor.execute(query)
        result = self._mycursor.fetchall()
        return result
    
    def view_doctor_specialists(self,spec):
        query = f"SELECT d_name, specialist, from_time, to_time FROM doctor WHERE relieve = 'N' and specialist = '{spec}';"
        self._mycursor.execute(query)
        result = self._mycursor.fetchall()
        return result
    
    def get_tok_no(self):
        query = f"SELECT MAX(tok_no) FROM queue;"
        self._mycursor.execute(query)
        res = self._mycursor.fetchone()
        return res+1

    def add_patient_to_queue(self,t_no,pid,did):
        query = f"INSERT INTO queue(tok_no, p_id, d_id, status) VALUES ({t_no},{pid},{did},'N');"
        self._mycursor.execute(query)
        self._mydb.commit()
        self.__update_patient(t_no,pid)
    
    def __update_patient(self,t_no,p_id):
        query = f"UPDATE patient SET tok_no = {t_no} WHERE p_id = {p_id};"
        self._mycursor.execute(query)
        self._mydb.commit()
    
    def get_d_id(self,d_name,spec):
        query = f"SELECT d_id FROM doctor WHERE d_name = '{d_name}' AND specialist = '{spec}';"
        self._mycursor.execute(query)
        res = self._mycursor.fetchone()
        return res