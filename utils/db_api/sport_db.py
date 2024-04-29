import sqlite3
import os
from datetime import datetime
import json

def create():
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    print("Подключен к SQLite")

    sqlite_insert_query = ''' CREATE TABLE sport_type (
                                    
                                id INTEGER PRIMARY KEY,
                                name text
                                    );'''
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    sqlite_insert_query = ''' CREATE TABLE workouts (
                                id INTEGER PRIMARY KEY,
                                name text,
                                mas_exsersize_id text
                                );
                                '''
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    sqlite_insert_query = ''' CREATE TABLE exsersize (
                                id INTEGER PRIMARY KEY,
                                name text UNIQUE,
                                type_id integer,
                                last_result text,
                                FOREIGN KEY (type_id)  REFERENCES sport_type (id) );
                                '''
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    sqlite_insert_query = ''' CREATE TABLE history_workout (
                                id INTEGER PRIMARY KEY,
                                data text,
                                tren_id INTEGER,
                                mas_res_exsersize_id text,
                                FOREIGN KEY (tren_id)  REFERENCES workouts (id));
                                '''
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    cursor.close()
    add_new_sport_type('Грудь')
    add_new_sport_type('Спина')
    add_new_sport_type('Руки')
    add_new_sport_type('Ноги')
    add_new_sport_type('Кардио')
    #добавление упражнений 
    add_new_exsersize('Жим штанги',1)
    add_new_exsersize('Разводка',1)
    add_new_exsersize('Нижний блок',2)
    add_new_exsersize('Верхний блок',2)
    add_new_exsersize('Тренажер на квадрицпес',4)
    add_new_exsersize('Тренажер на икры',4)
    add_new_exsersize('Бицепс со штангой',3)
    add_new_exsersize('Канаты на трицепс',3)
    add_new_exsersize('Гребля',5)
    add_new_exsersize('Бег',5)
    add_new_workouts([1,3,5,7],"Первый вид с жимом штанги")
    add_new_workouts([2,4,6,8],"Второй вид с разводкой ")

def add_new_sport_type(name:str):
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''INSERT INTO sport_type (name) values("{name}");'''
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    cursor.close()

def add_new_exsersize(name:str,type_id:int):
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''INSERT INTO exsersize (name,type_id,last_result) values("{name}",{type_id},"Вы еще не делали это упраженение как только, сделаете его в первых раз здесь будет написан ваш пролый результат");'''
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    cursor.close()



def delete_exsersize(name:str):
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''DELETE FROM exsersize where name="{name}";'''
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    cursor.close()

def get_exsersize(type_id:int):
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''SELECT e.name,e.id
            from exsersize e
            where  e.type_id={type_id}'''
    cursor.execute(sqlite_insert_query)
    a=cursor.fetchall()
    cursor.close()
    if len(a)==0:
        return []
    return a

def get_all_exsersize():
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''SELECT e.name,e.id from exsersize e order by e.type_id'''
    cursor.execute(sqlite_insert_query)
    a=cursor.fetchall()
    cursor.close()
    if len(a)==0:
        return []
    return a

def get_sport_type():
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''SELECT name,id from sport_type'''
    cursor.execute(sqlite_insert_query)
    a=cursor.fetchall()
    cursor.close()
    if len(a)==0:
        return []
    return a

def add_new_workouts(mas:list,name:str,):
    mas_str=json.dumps(mas)
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''INSERT INTO workouts (name,mas_exsersize_id) values("{name}","{mas_str}");'''
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    cursor.close()


def get_text_workouts(id:int):
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''SELECT name,mas_exsersize_id from workouts where id={id}'''
    cursor.execute(sqlite_insert_query)
    name,mas=cursor.fetchall()[0]
    mas=json.loads(mas)
    s=f'Тренировка под названием {name}\nСостоит из упражнений:\n'
    k=0
    for q in mas:
        k+=1
        sqlite_insert_query=f'''SELECT name from exsersize where id={int(q)}'''
        cursor.execute(sqlite_insert_query)
        name_of_exsersize=cursor.fetchall()[0][0]
        s+=str(k)+'.'+name_of_exsersize+'\n'
    return s

def get_all_workouts():
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''SELECT name,id from workouts '''
    cursor.execute(sqlite_insert_query)
    cursor.execute(sqlite_insert_query)
    a=cursor.fetchall()
    cursor.close()
    if len(a)==0:
        return []
    return a
def get_workouts(id:int):
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''SELECT mas_exsersize_id from workouts where id={id}'''
    cursor.execute(sqlite_insert_query)
    mas=cursor.fetchall()[0][0]
    mas=json.loads(mas)
    a=[]
    for q in mas:
        sqlite_insert_query=f'''SELECT name from exsersize where id={int(q)}'''
        cursor.execute(sqlite_insert_query)
        name_of_exsersize=cursor.fetchall()[0][0]
        a.append([name_of_exsersize,q])
    cursor.close()
    return a

def last_result_for_excersize(exers_id:int):
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''SELECT last_result from exsersize where id={exers_id}'''
    cursor.execute(sqlite_insert_query)
    a=cursor.fetchall()[0][0]
    cursor.close()
    if len(a)==0:
        return []
    return a

def add_new_tren(id:int,a:list):
    '''
    Функция добавляет новую тренировку в историю ей необходимо передать id тренировки и масив в котором на каждое упражнение будет содержать следущая информация
    масив размером количества подзодов где каждый элемент это строка содержащая следущее "количество повторений|вес"
    Пример такого масива, который необходимо передать в качестве парметра [ ["12|30","12|30","14|30"],......]
    '''
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''INSERT INTO history_workout (data,tren_id,mas_res_exsersize_id) values("{datetime.now().strftime("%y-%m-%d")}",{id},'{json.dumps(a)}');'''
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    listt=get_workouts(id)
    k=0
    for _ in a:
        count=0
        s=''
        for i in _:
            count+=1
            a,b=map(int,i.split('|'))
            string=f'{a} повторений|{b} кг'
            s+=f'Подход №{count} {string}\n'
        if s!='':
            new_s='На прошлой тренировки(на которой деллали данное упражнение) вы сделали следущие подходы:\n'+s
            sqlite_insert_query=f'''UPDATE  exsersize set last_result='{new_s}' where id={listt[k][1]}'''
            cursor.execute(sqlite_insert_query)
        k+=1
    sqlite_connection.commit()
    cursor.close()



def history_of_workout(day:int=7):
    '''
    Функиця внутри написана не очень, но учитывая что тренировок в неделю может быть не больше 14(и то с натяжкой), то проблем не должно быть)))))))
    а так она возвращает готовую строку с информацией о всех тренировках
    '''
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''SELECT w.name, h.tren_id,h.mas_res_exsersize_id,h.data
            from history_workout  h
            left join workouts w on w.id=h.tren_id
            where data>=date("now",'-{day} days')
            order by data desc'''
    cursor.execute(sqlite_insert_query)
    a=cursor.fetchall()
    s=''
    for i in a:
        mas=json.loads(i[2])
        b=get_workouts(int(i[1]))
        k=0
        s+=f'\nНазвание тренировки: {i[0]}\nДата тренировки: {i[3]}\n'
        for q in b:
            f=True
            count=0
            s+=q[0]+'\n'
            for string in mas[k]:
                count+=1
                f=False
                a,b=map(int,string.split('|'))
                string=f'{a} повторений|{b} кг'
                s+=f'Подход №{count} {string}\n'
            if f:
                s+=f'Упражнение не сделано\n'
            k+=1
    return s


if __name__=='__main__':
    '''if  os.path.exists('./all.db'):
        os.remove('./all.db')
    create()
    #добавление стандартных спортивынх типов упражений
    add_new_sport_type('Грудь')
    add_new_sport_type('Спина')
    add_new_sport_type('Руки')
    add_new_sport_type('Ноги')
    add_new_sport_type('Кардио')
    #добавление упражнений 
    add_new_exsersize('Жим штанги',1)
    add_new_exsersize('Разводка',1)
    add_new_exsersize('Нижний блок',2)
    add_new_exsersize('Верхний блок',2)
    add_new_exsersize('Тренажер на квадрицпес',4)
    add_new_exsersize('Тренажер на икры',4)
    add_new_exsersize('Бицепс со штангой',3)
    add_new_exsersize('Канаты на трицепс',3)
    add_new_exsersize('Гребля',5)
    add_new_exsersize('Бег',5)
    add_new_workouts([1,3,5,7],"Первый вид с жимом штанги")
    add_new_workouts([2,4,6,8],"Второй вид с разводкой ")
    #print(get_text_workouts(1))
    #print(get_workouts(1))
    #print(last_result_for_excersize(1))
    #add_new_tren(1,["12|30","12|30"])'''
   


