from controller.hospital import hospital
from view.admin import admin
from view.doctor import doctor
from view.patient import patient
from view.pharmacist import pharmacist
from view.receptionist import receptionist

class Hospital:

    def __init__(self) -> None:
        print("WELCOME TO THE HOSPITAL!!!\n")
        self.__hospital = hospital()
        self.__main_page()
    
    def __main_page(self):
        print("1. Login\n2. Exit\n")
        n = input("Enter your Choice : ")
        n = self.__hospital.check_main(n)
        if n==1:
            self.__login()
        elif n==2:
            exit()
        else:
            print("Enter the correct option !!!!\n")
            self.__main_page()
    
    def __login(self):
        u_name = input("Enter your user Name : ")
        if self.__hospital.valid_u_name(u_name):
            pwd = input("Enter password : ")
            if self.__hospital.valid_pwd(pwd):
                self.__u_name = u_name
                self.__u_type()
            else:
                print("Wrong Password !!!\n")
                self.__main_page()
        else:
            print("Wrong User Name !!!\n")
            self.__main_page()
    
    def __u_type(self):
        type = self.__hospital.get_u_type(self.__u_name)
        if type==1:
            admin()
        elif type==2:
            doctor()
        elif type==3:
            receptionist()
        elif type==4:
            pharmacist()
        else:
            patient()
    
    def __del__(self):
        print("------------ THANK YOU ------------")

if __name__=='__main__':
    Hospital()