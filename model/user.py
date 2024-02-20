from db import db

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
