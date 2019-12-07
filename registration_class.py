# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 14:03:31 2019

@author: Andrei Shtanakov

Реализован класс User, в котором методы регистрации пользователя, 
входа в систему.
На основе этого класса реализован класс Admin с расширенными функциями,
позволяющий менять пароль любому пользователю.

так же реализован скрытый ввод пароля (не все терминалы поддерживают) и
хренение паролей в зашифрованном виде.

"""

"""
def reg(self)
Метод регистрации нового пользователя. Проверяется наличие файла users.json,
в котором сохраняются пары - Пользователь/Пароль. Если файла нет (при первом 
запуске программы, например), то он создается.
Пароль вводится один раз, по идее, нужно добавить повторный ввод пароля
для подтверждения.
Модуль getpass позваляет скрыто вводить пароль, но не все терминалы это
поддерживают. Например терминал в Spyder не поддерживает, и выводит
предупреждение.
"""    


"""
def end_of_try
Метод вывода на печать количетва оставшихся попыток для ввода данных.
Оставшееся количество попыток передается в параметре t.
Максимальное количество - 10 попыток.
"""

"""
def compare_pass
Метод сравнения введенного пользователем пароля с паролем, созраненным в
словаре acount. В качестве параметров передаются имя пользователя и количество
попыток ввода пароля. По умолчанию количество равно 3.
"""
  
"""
def login(self):
Метод входа пользователя в систему.
Если такого имени пользователя не существует, выдается ошибка и
предлагается повторить попытку.
количество неуспешных попыток - 3
"""   
"""
def acounting(self):
Основной метод.
Проверка файла с аккаунтами. Приглашение к регитрации или авторизации.
Вызов фунции регистрации или авторизации.
 
Фаил сохранен в GIT

"""   

import json
import getpass
from pathlib import Path
import base64


path = Path('users.json')
acount = {}  #словарь, в котором содержаться пары Пользователь/Логин
#user = ""


class User(object):
    def __init__(self):
        """Constructor"""
        self.name = ""
        self.__password = ""



    def encode_pass(self, my_password): # Закодировать пароль
        # Encoding the string into bytes
        b = my_password.encode("UTF-8")
        # Base64 Encode the bytes
        e = base64.b64encode(b)
        # Decoding the Base64 bytes to string
        s1 = e.decode("UTF-8")
        # Printing Base64 encoded string
        self.__password = s1

    def decode_pass(self):   # Раскодировать пароль
        b1 = self.__password("UTF-8")
        # Decoding the Base64 bytes
        d = base64.b64decode(b1)
        # Decoding the bytes to string
        s2 = d.decode("UTF-8")
        return(s2)
    

    

    def reg(self):
        registration = True
        while registration:
            self.name = str(input("Введите Имя пользователя (логин): "))
            if acount.get(self.name, False):
                print("Пользователь с таким именем существует. Попробуйте еще.")
            else:
#               скрытый ввод пароля
                b1 = getpass.getpass(prompt="Введите пароль: ")
                self.encode_pass(b1)
                acount[self.name] = self.__password


#               при успешной регистрации словарь с паролями сохраняется в файл
#               в вормате json
                path.write_text(json.dumps(acount), encoding='utf-8')
                print(acount)
                registration = False
        
    
    def end_of_try(self, t = 0):
        trys = True
        if t in range(11):
            if t in [2, 3, 4]:
                print("У Вас осталось " + str(t) + " попытки.")
            elif t in [5, 6, 7, 8, 9, 10]:
                print("У Вас осталось " + str(t) + " попыток.")
            elif t == 1:
                print("У Вас осталась 1 попытка.")
            else:
                print("У Вас не осталось попыток.")
                trys = False
            return(trys)    
        print("Неверный диапазон.")
        return(False)




    def compare_pass(self, n = 3):
        b = n
        my_pass = True
        while my_pass:
#       скрытый ввод пароля

            b1 = getpass.getpass(prompt="Введите пароль: ")
            self.encode_pass(b1)
#            self.__password = getpass.getpass(prompt="Введите пароль: ")
            if self.__password == acount[self.name]:
                return(True)
            else:
                print("Неверный пароль!")
                b -= 1
                my_pass = self.end_of_try(b)
        return(my_pass)
    



    def login(self):
        a = 3
        my_login = True
        my_pass = True
        while my_login:
            self.name = str(input("Введите Имя пользователя: "))
#       Если пользователь существоет, то ...
            if acount.get(self.name, False):
#        Если пользователь существоет, вызывается функция проверки его пароля
                my_pass = self.compare_pass( 3)
                if my_pass:
                    return(True)
                else:
                    my_login = False
            else:
                print("Пользователь с таким именем не существует. Попробуйте еще.")
                a -= 1
                my_login = self.end_of_try(a)
        print("Ошибка входа. Вы исчерпали количество попыток.")
        return(False)



    def acounting(self):
        i = True
        global acount
    # проверка существования файла с аккаунтами пользователей
        try:
            acount = json.loads(path.read_text(encoding='utf-8'))
        except:
            acount = {}
        # если файла нет, то создаем пустой файл 
            path.write_text(json.dumps(acount), encoding='utf-8')
        while i:
            print("У вас есть акаунт?")
            print("r - регистрация")
            print("l - вход")
            print("q - выход")
            r = input("Выберите режим: ")
            if r == 'r':   # Регистрация нового пользователя
                self.reg()
            elif r == 'l':  # авторизация пользователя
                if self.login():
                    print("Hello! "+ self.name)
                    print("Вы вошли в систему.")
                    i = False
                else:
                    return(False)
            elif r == 'q':  # выход
                print("Good By!")
                i = False
                return(False)
            else:
                pass
        return(True)
            
"""
Класс Admin производный от класса User. Добавлена возможность смены пароля 
любому пользователю

"""

        
class Admin(User):

    def __init__(self):
        """Constructor"""
        self.name = ""
        self.__password = ""
        
        
    def encode_user_pass(self, user, password): #кодировка пароля пользователю
        # Encoding the string into bytes
        b = password.encode("UTF-8")
        # Base64 Encode the bytes
        e = base64.b64encode(b)
        # Decoding the Base64 bytes to string
        s1 = e.decode("UTF-8")
        # Printing Base64 encoded string
        acount[user] = s1
        path.write_text(json.dumps(acount), encoding='utf-8')

        
    def change_pass(self, user1):  # замена пароля другому пользователю
        if acount.get(user1, False):
            print("Введите пароль для Пользователя " + user1)
            b1 = getpass.getpass(prompt="Введите пароль для Пользователя ")
            self.encode_user_pass(user1, b1)
            
        else:
            print("Пользователь с именем " + user1 + " не существует.")
        
    


"""
Программа проверки класса так себе. Просто проверял под пользователем
admin возможность смены пароля пользователю user с последующим входом
пользователя user с  новым паролем.

"""
user_test = Admin()
cikl = True
while cikl:
    if cikl == True:
        cikl = user_test.acounting()
        if cikl == True:
            print("Для выхода из системы - q")
            print("Смена пароля другому пользователю - p")
            print("Для повторной регитрации/входа любой ввод")
            r = input("Выберите режим: ")
            if r == 'p':
                user_test.change_pass("user")
                
            if r == 'q':
                cikl = False
        