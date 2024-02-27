from model.user import user_login_db

class hospital:
    def __init__(self) -> None:
        self.__login = user_login_db()

    def check_main(self,s):
        try:
            s = int(s)
        except:
            return None
        else:
            return s
    
    def valid_u_name(self,u_name):
        return self.__login.check_u_name(u_name)
    
    def valid_pwd(self, pwd):
        return self.__login.check_pwd(pwd)
    
    def get_u_type(self, u_name):
        pass