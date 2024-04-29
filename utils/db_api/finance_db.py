import sqlite3
import os
from datetime import datetime

def create():
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    print("Подключен к SQLite")

    sqlite_insert_query = ''' CREATE TABLE accounts (
                                    
                                id INTEGER PRIMARY KEY,
                                money INTEGER,
                                name text
                                    );'''
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    sqlite_insert_query = ''' CREATE TABLE category (
                                id INTEGER PRIMARY KEY,
                                name text);
                                '''
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    sqlite_insert_query = ''' CREATE TABLE purchases (
                                id INTEGER PRIMARY KEY,
                                name text,
                                accounts_id integer,
                                category_id integer,
                                money integer,
                                data text,
                                FOREIGN KEY (accounts_id)  REFERENCES accounts (id),
                                FOREIGN KEY (category_id)  REFERENCES category (id));
                                '''
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    sqlite_insert_query = ''' CREATE TABLE income (
                                id INTEGER PRIMARY KEY,
                                name text,
                                accounts_id integer,
                                money integer,
                                data text,
                                FOREIGN KEY (accounts_id)  REFERENCES accounts (id));
                                '''
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    cursor.close()
    insert_new_category('рестораны/кофе')
    insert_new_category('еда дома')
    insert_new_category('импульсивные покупки')
    insert_new_category('подарки')
    insert_new_category('спорт')
    insert_new_category('здоровье')
    insert_new_category('транспорт')
    insert_new_category('связь')
    #стандарные счета
    insert_new_account(0,'наличка')
    insert_new_account(34808,'кредитка')
    insert_new_account(24581,'дебетовая карта')
    insert_new_account(2000,'накопления')


def insert_new_account(money:int,name :str):
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''INSERT INTO accounts (money,name) values({money},"{name}");'''
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    cursor.close()

def insert_new_category(name :str):
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''INSERT INTO category (name) values("{name}");'''
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    cursor.close()

def get_account_from_id(id:int):
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''select name from accounts where id={id}'''
    cursor.execute(sqlite_insert_query)
    a=cursor.fetchall()
    cursor.close()
    return a

def get_all_accounts()->list:
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''select name,id from accounts'''
    cursor.execute(sqlite_insert_query)
    a=cursor.fetchall()
    cursor.close()
    if len(a)==0:
        return []
    return a

def get_all_category()->list:
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''select name,id from category'''
    cursor.execute(sqlite_insert_query)
    a=cursor.fetchall()
    cursor.close()
    if len(a)==0:
        return []
    return a


def insrert_new_income(name:str,accounts_id:int,money:int):
    '''Функция добавляет новый доход в базу данных а так же меняет сумма которая хранится на счета'''
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    data=datetime.now().strftime("%y-%m-%d")
    sqlite_insert_query=f'''INSERT INTO income (name,accounts_id,money,data) values("{name}",{accounts_id},{money},"{data}");'''
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    sqlite_insert_query=f'''UPDATE accounts set money=money+{money} where id={accounts_id} '''
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    cursor.close()

def insert_new_purchases(name:str,accounts_id:int,category_id:int,money:int):
    '''Функция добавляет новую трату в баззу данных а так же меняет сумму которая хранится на счете с которого произошла тратта
    провеки на существование данного счета нет, так как по логике бота до этой функции можно добраться только выбрав счет с которого была трата'''
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    data=datetime.now().strftime("%y-%m-%d")
    sqlite_insert_query=f'''INSERT INTO purchases (name,accounts_id,category_id,money,data) values("{name}",{accounts_id},{category_id},{money},"{data}");'''
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    sqlite_insert_query=f'''UPDATE accounts set money=money-{money} where id={accounts_id} '''
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    cursor.close()

def get_all_purchases(day:int=7)->list:
    '''Функция возвращает все траты во всех категориях за последние дни(задется в параметре)
    каждый элемент массива - кортеж : название траты, категория траты, счет с которого потрачено, cумма, дата
    или возвращает пустой массив'''
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''SELECT p.name,c.name,a.name,p.money,p.data 
            from purchases p  
            left join category c  on c.id=p.category_id  
            left join accounts a  on a.id=p.accounts_id
            where data>=date("now",'-{day} days')'''
    cursor.execute(sqlite_insert_query)
    a=cursor.fetchall()
    if len(a)==0:
        return []
    return a

def get_category_purchases(category_id:int,day:int):
    '''Функция возвращает все траты в выбраной категории за последние дни(задется в параметре)
    каждый элемент массива - кортеж : название траты, категория траты, счет с которого потрачено, cумма, дата
    или возвращает пустой массив'''
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''SELECT p.name,c.name,a.name,p.money,p.data 
            from purchases p  
            left join category c  on c.id=p.category_id  
            left join accounts a  on a.id=p.accounts_id
            where data>=date("now",'-{day} days') and p.category_id={category_id}
            '''
    cursor.execute(sqlite_insert_query)
    a=cursor.fetchall()
    cursor.close()
    if len(a)==0:
        return []
    return a

def get_account_purchases(account_id:int,day:int):
    '''Функция возвращает все траты с выбранного счета за последние дни(задется в параметре)
    каждый элемент массива - кортеж : название траты, категория траты, счет с которого потрачено, cумма, дата
    или возвращает пустой массив'''
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''SELECT p.name,c.name,a.name,p.money,p.data 
            from purchases p  
            left join category c  on c.id=p.category_id 
            left join accounts a  on a.id=p.accounts_id 
            where data>=date("now",'-{day} days') and p.accounts_id={account_id}
            '''
    cursor.execute(sqlite_insert_query)
    a=cursor.fetchall()
    cursor.close()
    if len(a)==0:
        return []
    return a

def get_account_category_purchases(category_id:int,account_id:int,day:int):
    '''Функция возвращает все траты с выбранного счета и по выбранной категории за последние дни(задется в параметре)
    каждый элемент массива - кортеж : название траты, категория траты, счет с которого потрачено, cумма, дата
    или возвращает пустой массив'''
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''SELECT p.name,c.name,a.name,p.money,p.data 
            from purchases p  
            left join category c  on c.id=p.category_id  
            left join accounts a  on a.id=p.accounts_id
            where data>=date("now",'-{day} days') 
            and p.accounts_id={account_id} 
            and p.category_id={category_id}'''
    cursor.execute(sqlite_insert_query)
    a=cursor.fetchall()
    cursor.close()
    if len(a)==0:
        return []
    return a


def get_money_from_accounts()->str:
    '''Функция возваращет строку в которой указаны все счета и все суммы на них в формате Название счета\nСумма на нем и так далее'''
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''select money,name from accounts'''
    cursor.execute(sqlite_insert_query)
    a=cursor.fetchall()
    cursor.close()
    if len(a)==0:
        return 'У вас нет счетов'
    s='Остаток на ваших счетах\n\n'
    k=0
    for i in a:
        k+=1
        money,name=i
        s+=f'Счет №{k}\n{name}\nОстаток на счете: {money}\n'
    return s

def transfer_from_account_to_account(account_id_1:int,account_id_2:int,money:int):
    '''Функция переводить деньги со одного счета на другой (c account_id_1 на account_id_2) '''
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''UPDATE accounts set money=money-{money} where id={account_id_1} '''
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    sqlite_insert_query=f'''UPDATE accounts set money=money+{money} where id={account_id_2} '''
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    cursor.close()

def change_account_money(id:int, money:int):
    """
    Функция менят количество денег на счете
    """
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''UPDATE accounts set money={money} where id={id} '''
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    cursor.close()

def delete_account(id:int):
    """
    Функция удаляет счет по его id
    """
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''DELETE  from accounts where id={id} '''
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    cursor.close()

if __name__=='__main__':
    if  os.path.exists('./all.db'):
        os.remove('./all.db')

  


  
