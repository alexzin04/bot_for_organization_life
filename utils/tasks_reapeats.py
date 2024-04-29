import asyncio
from utils.db_api.tasks_db import get_all_repeat_tasks_today,add_new_task,change_repeat_tasks,get_task_for_time,get_task_from_id
from datetime import datetime,date,time,timedelta
from loader import scheduler,dp
from data.config import ADMINS


def change_db_for_tasks(name,datee,repeat_rules,timee,id):
    dat=datetime(datee.year,datee.month,datee.day,timee.hour,timee.minute) if timee!=None else datee
    add_new_task(name,dat,True if time!=None else False)
    if repeat_rules.split()[0]=="once_a_month":
        datee=dat+timedelta(days=30)
    elif repeat_rules.split()[0]=="days_of_week":
        cur_weekday=datee.weekday()
        weekday_array=list(map(int,repeat_rules.split()[1].split(',')))
        weekday_array.sort()
        next_weekday=None
        for day in weekday_array:
            if day>cur_weekday:
                next_weekday=day
                break
        if next_weekday==None:
            next_weekday=weekday_array[0]
        datee = datee + timedelta(days=(next_weekday - cur_weekday) % 7)
    elif repeat_rules.split()[0]=="every_day":
        datee+=timedelta(days=1)
    change_repeat_tasks(id,datee)
    
async def send_notification(name:str):
    """
    отправляет напоминание о задаче, пока только админам, но пока единственый пользователь я) исправить будет очень просто передать еще один аргумент
    """
    await dp.bot.send_message(chat_id=ADMINS[0],text=f'Напоминание о выполнение задачи:\n{name}')


async def every_day_helper():
    mas=get_all_repeat_tasks_today()
    for i in mas:
        id,name,datee,rules,timee=i
        datee=datetime.strptime(datee,"%Y-%m-%d")
        timee=datetime.strptime(timee,"%H-%M") if timee!='None' else None
        change_db_for_tasks(name,datee,rules,timee,id)
    mas=list(get_task_for_time().values())
    if len(mas)!=0:
        mas=mas[0]
    for i in mas:
        m=get_task_from_id(int(i[1]))
        print(m)
        if m[-1]!='None':
            date=datetime.strptime(m[2]+'-'+m[3],"%Y-%m-%d-%H-%M")
            scheduler.add_job(send_notification,'date',run_date=date,args=(m[1],))
 

            

