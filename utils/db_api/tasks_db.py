import sqlite3
import os
import json
from datetime import date, datetime, time, timedelta
#from loader import scheduler
#from utils.tasks_reapeats import send_notification

async def tessttt():
    print('Тест прошел успешно')

def create():
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    print("Подключен к SQLite")

    sqlite_insert_query = ''' CREATE TABLE tasks (
                                    
                                id INTEGER PRIMARY KEY,
                                name text,
                                data text,
                                time text,
                                isComplete int
                                    );'''
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    sqlite_insert_query = ''' CREATE TABLE challenge (
                                id INTEGER PRIMARY KEY,
                                name text,
                                state integer,
                                count_for_day integer
                                );'''
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    sqlite_insert_query = ''' CREATE TABLE every_day_challenge (
                                id INTEGER PRIMARY KEY,
                                challenge_id integer,
                                mas text,
                                date_start text,
                                date_finish text,
                                FOREIGN KEY (challenge_id)  REFERENCES challenge (id));
                                '''
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    sqlite_insert_query = ''' CREATE TABLE repeat_tasks (
                                id INTEGER PRIMARY KEY,
                                name text,
                                repeat_date_next text,
                                repeat_rules text,
                                time text
                                );
                                '''
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    cursor.close()


def add_new_task(name:str,date:datetime=None,time_flag:bool=False):
    '''
    Функция добавляет новую задачу в базу данны, помимо того если задача имеет время(то есть напоминание) и так же эта дата сегодня то она добавляет эту
    задачу в задачи на отправку сообщений
    '''
    if date==None:
        date=datetime.now()
        date=date.strftime("%Y-%m-%d")
        time=None
    else:
        if date.day==datetime.now().day:
            if time_flag:
                pass
                #scheduler.add_job(send_notification,'date',run_date=date,args=(name,))
        a=date.strftime("%Y-%m-%d")
        time=date.strftime("%H-%M") if time_flag else None
        date=a

    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''INSERT INTO tasks (name,data,time,isComplete) values("{name}","{date}","{time}",0);'''
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    cursor.close()
        

def get_task_for_time(days:int=0)->dict:
    """
    Функция возвращает все задачи на определеное количество дней, по умолчанию на сегодня. Возвращает словарь с ключом -дата и со значением - название задачи
    """
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''SELECT name,data,id,time
            from tasks  
            where data{f"=date('now')" if days==0 else f" between date('now') and date('now','{days} days')"} and isComplete=0
            order by data '''
    cursor.execute(sqlite_insert_query)
    a=cursor.fetchall()
    dictt={}
    for i in a:
        if dictt.get(i[1])!=None:
            value=dictt.get(i[1])
            value.append([i[0],i[2],i[3]])
            dictt.update({i[1]:value})
        else:
            dictt.update({i[1]:[[i[0],i[2],i[3]]]})
    if days!=0:
        sqlite_insert_query=f'''SELECT name,repeat_date_next,repeat_rules,time,id
            from repeat_tasks  
            where repeat_date_next<=date('now','{days} days')
             '''
        cursor.execute(sqlite_insert_query)
        a=cursor.fetchall()
        for i in a:
            name,repeat_date_next,repeat_rules,timee,id=i
            date_start=datetime.strptime(repeat_date_next,'%Y-%m-%d')
            dat=date_start
            flag_for_days_of_week=True
            while True:
                if repeat_rules.split()[0]=="once_a_month":
                    dat=dat+timedelta(days=30)
                elif repeat_rules.split()[0]=="days_of_week":
                    if flag_for_days_of_week:
                        flag_for_days_of_week=False
                    else:
                        cur_weekday=dat.weekday()
                        weekday_array=list(map(int,repeat_rules.split()[1].split(',')))
                        weekday_array.sort()
                        next_weekday=None
                        for day in weekday_array:
                            if day>cur_weekday:
                                next_weekday=day
                                break
                        if next_weekday==None:
                            next_weekday=weekday_array[0]
                        dat = dat + timedelta(days=(next_weekday - cur_weekday) % 7)
                elif repeat_rules.split()[0]=="every_day":
                    dat=dat+ timedelta(days=1)
                if dat<date_start+timedelta(days=days):
                   
                    date_start_str=dat.strftime('%Y-%m-%d')
                   
                    if dictt.get(date_start_str)!=None:
                        value=dictt.get(date_start_str)
                        value.append([name,id, timee])
                        dictt.update({date_start_str:value})
                    else:
                        dictt.update({date_start_str:[[name,id, timee]]})
                else:
                    break
    return(dictt)

def generate_str_from_dict_task(dictt:dict)->str:
    """
    Функция возвращает строку сообщения полученную из словаря в формате: Дата\n1.Задача\n 2. Задача и т.д.. Дата..
    """
    s='\nЗадачи:\n'
    if len(dictt.items())==0:
        return '\nЗадач нет('
    for i in dictt.items():
        data,mas=i
        s+=data+'\n'
        k=0
        for v in mas:
            q,id,time=v
            k+=1
            s+=f'{k}. {q} Время {time}\n'
    return s

def add_repeat_tasks(name:str,date_start:date,repeat_rules:str,time:time=None):
    """
    Добавление в баззу данных повторяющейся задачи, repeat_rules- once_a_month(раз в месяц),days_of_week дни через запятую(в какие дни недели 0- понельник),every_day(каждый день)
    """
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    if date_start==date.today():
        dat=datetime(date_start.year,date_start.month,date_start.day,time.hour,time.minute) if time!=None else date_start
        add_new_task(name,dat,True if time!=None else False)
        if repeat_rules.split()[0]=="once_a_month":
            date_start=dat+timedelta(days=30)
        elif repeat_rules.split()[0]=="days_of_week":
            cur_weekday=date_start.weekday()
            weekday_array=list(map(int,repeat_rules.split()[1].split(',')))
            weekday_array.sort()
            next_weekday=None
            for day in weekday_array:
                if day>cur_weekday:
                    next_weekday=day
                    break
            if next_weekday==None:
                next_weekday=weekday_array[0]
            date_start = date_start + timedelta(days=(next_weekday - cur_weekday) % 7)
        elif repeat_rules.split()[0]=="every_day":
            date_start+=timedelta(days=1)     
    sqlite_insert_query=f'''INSERT INTO repeat_tasks (name,repeat_date_next,repeat_rules,time) values("{name}","{date_start.strftime("%Y-%m-%d")}","{repeat_rules}","{time.strftime("%H-%M")if time!=None else time}");'''
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    cursor.close()


def get_all_repeat_tasks_today()->list:
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''SELECT id,name,repeat_date_next,repeat_rules,time
            from repeat_tasks  
            where repeat_date_next=date("now") '''
    cursor.execute(sqlite_insert_query)
    a=cursor.fetchall()
    cursor.close()
    return [i for i in a]

def change_repeat_tasks(id:int,new_repeat_date:date):
    '''
    Функция меняет дату следущего вызова повторяющегося таска на новую
    ''' 
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''UPDATE repeat_tasks set repeat_date_next='{new_repeat_date.strftime("%Y-%m-%d")}' where id={id}'''
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    cursor.close()

def get_task_from_id(id:int)->list:
    '''
    Получение данных о задаче по id
    '''
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''SELECT id,name,data,time
            from tasks  
            where id={id} '''
    cursor.execute(sqlite_insert_query)
    a=cursor.fetchall()

    cursor.close()
    return [i for i in a[0]]

def change_status_from_id(id:int):
    '''
    Помечает задачу выполненой по id
    '''
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''UPDATE tasks set isComplete=1 where id={id}'''
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    cursor.close()

def get_all_every_day_challenge()->list:
    '''
    Возвращает список из всех ежедневных челенджей которые идут сейчас
    '''
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''SELECT ev.id,ch.name,ev.mas
            from every_day_challenge ev  
             left join challenge ch on ch.id=ev.challenge_id
            where  date('now') between ev.date_start and ev.date_finish'''
    cursor.execute(sqlite_insert_query)
    a=cursor.fetchall()
    print(a)
    cursor.close()
    return [i for i in a]

def add_new_every_day_challenge(name:str,date_start:date,count_for_day:int,days_finish:int=14):
    '''
    Функция добавляет новый ежедневный вызов, создает новую строчку в challenge и добавляет его в every day challenge
    '''
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''insert into  challenge (name,state,count_for_day) values('{name}',0,{count_for_day}) '''
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    id=cursor.lastrowid
    mas=[0 for i in range(0,days_finish)]
    mas_str=json.dumps(mas)
    sqlite_insert_query=f'''insert into  every_day_challenge (challenge_id,mas,date_start,date_finish) values({id},'{mas_str}','{date_start.strftime('%Y-%m-%d')}','{(date_start+timedelta(days=days_finish)).strftime('%Y-%m-%d')}') '''
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    cursor.close()

def change_mas_for_every_day_challenge(id:int,count:int):
    '''
    Функиця добавляет нужное число повторений в массив вызова
    '''
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''SELECT mas,date_start
            from every_day_challenge  
            where id={id} '''
    cursor.execute(sqlite_insert_query)
    a=cursor.fetchall()
    if(len(a)!=0):
        mas,date_start=a[0]
        mas=json.loads(mas)
        date_start=datetime.strptime(date_start,"%Y-%m-%d")
        day=(datetime.now()-date_start).days
        if day>=0:
            mas[day]+=count
        mas_str=json.dumps(mas)
    sqlite_insert_query=f'''UPDATE every_day_challenge set mas='{mas_str}' where id={id}'''
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    cursor.close()

def create_str_from_id_for_every_day_challenge(id:int):
    '''
    Функция создает строчку из подробной информацией о ежедневном вызове
    '''
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''SELECT ev.mas,ev.date_start,ev.date_finish,ch.name,ch.count_for_day
            from every_day_challenge  ev
            left join challenge ch on ch.id=ev.challenge_id
            where ev.id={id} '''
    cursor.execute(sqlite_insert_query)
    a=cursor.fetchall()
    if len(a)==0:
        return 'Что-то случилось и данного вызова нет((((('
    mas,date_start,date_finish,name,count_for_day=a[0]
    s=f'''Данный вызов идет с {date_start} до {date_finish}\nНазвание: {name}\nКоличество повторений за день: {count_for_day}\nРаспредление по дням на данный момент\n{', '.join(str(x) for x in json.loads(mas))}\nХотите добавить новые повторения?'''
    return s

def get_inforamtion_about_challenge_today(id:int)->tuple:
    '''
    Фукнция возвращает общее количество повторений, которые нужно выполнить за день и то сколько уже сделано в формате (кол-во сделаных/всего)
    '''
    sqlite_connection = sqlite3.connect('all.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query=f'''SELECT ev.mas,ev.date_start,ch.count_for_day
            from every_day_challenge  ev
            left join challenge ch on ch.id=ev.challenge_id
            where ev.id={id} '''
    cursor.execute(sqlite_insert_query)
    a=cursor.fetchall()
    if len(a)==0:
        return 0,0
    mas,date_start,count_for_day=a[0]
    mas=json.loads(mas)
    date_start=datetime.strptime(date_start,"%Y-%m-%d")
    day=(datetime.now()-date_start).days
    count=0
    if day>=0:
        count=mas[day]
    return count,count_for_day

if '__main__'==__name__:
    #if  os.path.exists('./all.db'):
    #    os.remove('./all.db')
    #create()
    pass
    #add_new_task('проверка',datetime(2024,4,27))
    add_new_task('проверка time',datetime(2024,4,27,16,45),True)
    #generate_str_from_dict_task(get_task_for_time(7))
    #print(generate_str_from_dict_task( get_task_for_time(1)))
    #get_task_from_id(1)
    #add_repeat_tasks('Test_1',date(2024,4,21),"every_day",time(14,00))
    #add_repeat_tasks('Test_2',date(2024,4,21),"once_a_month",time(15,00))
    #add_repeat_tasks('Test_3',date(2024,4,21),"days_of_week 1,2,6",time(14,00))
    #print(get_all_repeat_tasks_today())
    #add_new_every_day_challenge('Скакалка',date(2024,4,20),1000)
    #change_mas_for_every_day_challenge(1,100)
    #print(create_str_from_id_for_every_day_challenge(1))