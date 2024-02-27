from model.db import db

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